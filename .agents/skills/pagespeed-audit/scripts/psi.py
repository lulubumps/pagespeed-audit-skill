#!/usr/bin/env python3
"""PageSpeed Insights helper: fetch (API v5), summarize and compare.

Standard library only. Subcommands:

  psi.py fetch URL [--strategy mobile|desktop|both] [--locale en] [--out DIR] [--raw] [--json]
  psi.py summarize FILE.json [FILE.json ...] [--json]
  psi.py compare BEFORE.json AFTER.json [--json]

The API key, when needed, is read from PAGESPEED_API_KEY (or PSI_API_KEY) and
sent in the X-Goog-Api-Key header so it never appears in a URL, a saved file
or an error message.
"""
import argparse
import ipaddress
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

API = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
KEY_ENVS = ("PAGESPEED_API_KEY", "PSI_API_KEY")

SENSITIVE_PARAM = re.compile(
    r"^(access_token|id_token|token|secret|session|sessionid|sid|password|passwd|pwd|auth|"
    r"apikey|api_key|key|signature|sig|jwt)$|token|secret|passw",
    re.I,
)
SENSITIVE_FRAGMENT = re.compile(r"(token|secret|passw|auth|key|session|jwt)=", re.I)
INTERNAL_SUFFIXES = (".local", ".internal", ".lan", ".home", ".corp", ".intranet", ".localhost")
INTERSTITIAL_PATH = re.compile(r"/(login|log-in|signin|sign-in|captcha|consent|blocked|challenge|cdn-cgi)(/|$|\?)", re.I)

METRIC_AUDITS = {
    "FCP": "first-contentful-paint",
    "LCP": "largest-contentful-paint",
    "TBT": "total-blocking-time",
    "CLS": "cumulative-layout-shift",
    "SI": "speed-index",
}
NOT_FINDINGS = set(METRIC_AUDITS.values()) | {
    "metrics", "diagnostics", "network-requests", "network-rtt", "network-server-latency",
    "main-thread-tasks", "resource-summary", "screenshot-thumbnails", "final-screenshot",
    "full-page-screenshot", "script-treemap-data", "performance-budget", "timing-budget",
    "largest-contentful-paint-element", "layout-shift-elements", "lcp-lazy-loaded",
    "interactive", "max-potential-fid",
}
SKIP_MODES = {"notApplicable", "manual", "error", "informative"}
CRUX_FIELDS = (
    ("LARGEST_CONTENTFUL_PAINT_MS", "LCP", 1),
    ("INTERACTION_TO_NEXT_PAINT", "INP", 1),
    ("CUMULATIVE_LAYOUT_SHIFT_SCORE", "CLS", 100),  # API reports CLS x100
    ("FIRST_CONTENTFUL_PAINT_MS", "FCP", 1),
    ("EXPERIMENTAL_TIME_TO_FIRST_BYTE", "TTFB", 1),
)


# --------------------------------------------------------------------------- URL
def validate_url(url):
    """Return the URL if it is safe to send to Google, else raise ValueError."""
    p = urllib.parse.urlsplit(url.strip())
    if p.scheme not in ("http", "https"):
        raise ValueError("Only public http(s) URLs are supported.")
    host = (p.hostname or "").lower()
    if not host:
        raise ValueError("The URL has no host.")
    if p.username or p.password:
        raise ValueError("The URL contains credentials; use a clean public URL.")
    if host == "localhost" or host.endswith(INTERNAL_SUFFIXES):
        raise ValueError("Internal hosts cannot be measured by PageSpeed Insights.")
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
        if "." not in host:
            raise ValueError("Single-label hosts are not public; use a fully qualified domain.")
    if ip and (ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_reserved):
        raise ValueError("Private or reserved IP addresses cannot be measured.")
    for name, _ in urllib.parse.parse_qsl(p.query, keep_blank_values=True):
        if SENSITIVE_PARAM.search(name):
            raise ValueError(f"Query parameter '{name}' looks like a secret; use a clean equivalent URL.")
    if p.fragment and SENSITIVE_FRAGMENT.search(p.fragment):
        raise ValueError("The URL fragment looks like it carries a secret.")
    return url.strip()


# ------------------------------------------------------------------------- fetch
def api_key():
    for name in KEY_ENVS:
        if os.environ.get(name):
            return os.environ[name]
    return None


def redact(text, key):
    return text.replace(key, "[REDACTED]") if key and text else text


def fetch_one(url, strategy, locale="en", timeout=120, retries=2):
    key = api_key()
    query = urllib.parse.urlencode(
        [("url", url), ("strategy", strategy), ("category", "performance"), ("locale", locale)]
    )
    headers = {"Accept": "application/json", "User-Agent": "pagespeed-audit-skill/2"}
    if key:
        headers["X-Goog-Api-Key"] = key
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(f"{API}?{query}", headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            body = redact(e.read().decode("utf-8", "replace"), key)
            try:
                msg = json.loads(body).get("error", {}).get("message", body[:300])
            except ValueError:
                msg = body[:300]
            last = f"HTTP {e.code}: {msg}"
            if e.code not in (429, 500, 502, 503, 504):
                break
            if e.code == 429 and not key:
                last += " (anonymous quota exhausted; set PAGESPEED_API_KEY or supply an exported report)"
        except (urllib.error.URLError, TimeoutError) as e:
            last = redact(str(getattr(e, "reason", e)), key)
        if attempt < retries:
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"PSI request failed for {strategy}: {last}")


def slim(data):
    """Drop heavy screenshot payloads that are useless for diagnosis."""
    lh = data.get("lighthouseResult") or {}
    lh.pop("fullPageScreenshot", None)
    for aid in ("screenshot-thumbnails", "final-screenshot", "full-page-screenshot", "script-treemap-data"):
        a = (lh.get("audits") or {}).get(aid)
        if a:
            a.pop("details", None)
    return data


# --------------------------------------------------------------------- summarize
def _num(x, nd=2):
    return None if x is None else round(x, nd)


def field_block(exp, default_scope):
    if not exp:
        return None
    metrics = exp.get("metrics") or {}
    found = {}
    for key, label, scale in CRUX_FIELDS:
        m = metrics.get(key)
        if m and m.get("percentile") is not None:
            found[label] = {"p75": _num(m["percentile"] / scale, 3), "category": m.get("category")}
    scope = "origin (fallback)" if exp.get("origin_fallback") else default_scope
    return {"scope": scope, "target": exp.get("id"), "overall": exp.get("overall_category"),
            "available": bool(found), "metrics": found}


def lcp_element(audits):
    items = ((audits.get("largest-contentful-paint-element") or {}).get("details") or {}).get("items") or []
    info = {}
    for table in items:
        if not (isinstance(table, dict) and table.get("type") == "table"):
            continue
        for row in table.get("items") or []:
            if not isinstance(row, dict):
                continue
            node = row.get("node")
            if node and "selector" not in info:
                info["selector"] = node.get("selector")
                info["snippet"] = (node.get("snippet") or "")[:160]
            if "phase" in row:
                info.setdefault("phases_ms", {})[row["phase"]] = _num(row.get("timing"), 0)
    return info or None


def findings(audits, limit=8):
    rows = []
    for aid, a in audits.items():
        if aid in NOT_FINDINGS or a.get("scoreDisplayMode") in SKIP_MODES:
            continue
        details = a.get("details") or {}
        if details.get("type") in ("debugdata", "screenshot", "filmstrip"):
            continue
        ms = details.get("overallSavingsMs") or 0
        ms = max([ms] + [v for v in (a.get("metricSavings") or {}).values() if isinstance(v, (int, float))])
        by = details.get("overallSavingsBytes") or 0
        score = a.get("score")
        if ms > 0 or by > 0 or (score is not None and score < 0.9):
            rows.append({"id": aid, "title": a.get("title"), "display": a.get("displayValue"),
                         "est_savings_ms": _num(ms, 0) or None, "est_savings_bytes": _num(by, 0) or None,
                         "score": score})
    rows.sort(key=lambda r: (-(r["est_savings_ms"] or 0), -(r["est_savings_bytes"] or 0), r["score"] if r["score"] is not None else 1))
    return rows[:limit]


def _norm(u):
    p = urllib.parse.urlsplit(u or "")
    return (p.scheme.lower(), (p.hostname or "").lower(), p.path.rstrip("/"), p.query)


def summarize(data, source=""):
    lh = data.get("lighthouseResult") or {}
    audits = lh.get("audits") or {}
    cfg = lh.get("configSettings") or {}
    score = ((lh.get("categories") or {}).get("performance") or {}).get("score")
    lab = {"score": None if score is None else round(score * 100)}
    for label, aid in METRIC_AUDITS.items():
        a = audits.get(aid) or {}
        lab[label] = {"value": _num(a.get("numericValue"), 3), "display": a.get("displayValue")} if a else None
    requested = lh.get("requestedUrl") or data.get("id")
    final = lh.get("finalDisplayedUrl") or lh.get("finalUrl")
    flags = []
    if lh.get("runtimeError"):
        e = lh["runtimeError"]
        flags.append(f"Lighthouse runtime error: {e.get('code')} - {e.get('message')}")
    if score is None:
        flags.append("No performance score was produced; treat the lab run as failed.")
    if requested and final and _norm(requested) != _norm(final):
        flags.append(f"Final URL differs from requested URL ({requested} -> {final}); confirm it is the intended page.")
    if final and INTERSTITIAL_PATH.search(final):
        flags.append("Final URL looks like a login, consent or challenge page; the score may not describe the target page.")
    warnings = lh.get("runWarnings") or []
    if warnings:
        flags.append(f"{len(warnings)} Lighthouse run warning(s); read them before trusting the score.")
    return {
        "source": source,
        "analysis_utc": data.get("analysisUTCTimestamp") or lh.get("fetchTime"),
        "requested_url": requested,
        "final_url": final,
        "device": cfg.get("formFactor"),
        "lighthouse_version": lh.get("lighthouseVersion"),
        "lab": lab,
        "field": {"page": field_block(data.get("loadingExperience"), "page"),
                  "origin": field_block(data.get("originLoadingExperience"), "origin")},
        "lcp_element": lcp_element(audits),
        "findings": findings(audits),
        "warnings": warnings,
        "flags": flags,
    }


def fmt_ms(v):
    if v is None:
        return "unavailable"
    return f"{v / 1000:.1f} s" if v >= 1000 else f"{v:.0f} ms"


def to_markdown(s):
    L = []
    L.append(f"### {s['device'] or 'unknown device'} - {s['final_url'] or s['requested_url']}")
    L.append(f"Captured {s['analysis_utc']} | Lighthouse {s['lighthouse_version']} | source: {s['source'] or 'n/a'}")
    for f in s["flags"]:
        L.append(f"- FLAG: {f}")
    lab = s["lab"]
    L.append("\n**Lab (Lighthouse)**\n")
    L.append("| Score | FCP | LCP | TBT | CLS | Speed Index |\n| --- | --- | --- | --- | --- | --- |")
    cells = [str(lab["score"]) if lab["score"] is not None else "unavailable"]
    for k in ("FCP", "LCP", "TBT"):
        cells.append(fmt_ms(lab[k]["value"]) if lab[k] else "unavailable")
    cells.append(f"{lab['CLS']['value']:.3f}" if lab["CLS"] and lab["CLS"]["value"] is not None else "unavailable")
    cells.append(fmt_ms(lab["SI"]["value"]) if lab["SI"] else "unavailable")
    L.append("| " + " | ".join(cells) + " |")
    L.append("\n**Field (CrUX, p75)**\n")
    L.append("| Scope | LCP | INP | CLS | Assessment |\n| --- | --- | --- | --- | --- |")
    page_fb = s["field"]["page"]
    page_is_origin = bool(page_fb and page_fb["scope"].startswith("origin"))
    for key in ("page", "origin"):
        if key == "origin" and page_is_origin:
            continue  # same data as the page row; do not present it twice
        fb = s["field"][key]
        if not fb or not fb["available"]:
            L.append(f"| {key} | unavailable | unavailable | unavailable | no data |")
            continue
        m = fb["metrics"]
        c = lambda n, fn: (f"{fn(m[n]['p75'])} ({m[n]['category']})" if n in m else "unavailable")
        L.append(f"| {fb['scope']} | {c('LCP', fmt_ms)} | {c('INP', fmt_ms)} | {c('CLS', lambda v: f'{v:.2f}')} | {fb['overall'] or 'not supplied'} |")
    if s["lcp_element"]:
        e = s["lcp_element"]
        L.append(f"\n**LCP element:** `{e.get('selector')}`" + (" - phases: " + ", ".join(f"{k} {v:.0f} ms" for k, v in e["phases_ms"].items() if v is not None) if e.get("phases_ms") else ""))
    if s["findings"]:
        L.append("\n**Top lab findings** (estimates overlap; never add them together)\n")
        L.append("| Audit | Detail | Est. time | Est. bytes |\n| --- | --- | --- | --- |")
        for r in s["findings"]:
            by = f"{r['est_savings_bytes'] / 1024:.0f} KiB" if r["est_savings_bytes"] else "-"
            L.append(f"| `{r['id']}` | {r['display'] or r['title']} | {fmt_ms(r['est_savings_ms']) if r['est_savings_ms'] else '-'} | {by} |")
    return "\n".join(L)


# ----------------------------------------------------------------------- compare
def compare(before, after):
    caveats = []
    for field, label in (("device", "device"), ("lighthouse_version", "Lighthouse version")):
        if before[field] != after[field]:
            caveats.append(f"{label} differs: {before[field]} vs {after[field]}")
    if _norm(before["final_url"]) != _norm(after["final_url"]):
        caveats.append(f"Final URL differs: {before['final_url']} vs {after['final_url']}")
    caveats.append("Single runs vary; prefer the median of three comparable runs per version and device.")
    rows = []
    b, a = before["lab"], after["lab"]
    if b["score"] is not None and a["score"] is not None:
        rows.append(("Score", b["score"], a["score"], a["score"] - b["score"]))
    for k in ("FCP", "LCP", "TBT", "CLS", "SI"):
        bv, av = (b[k] or {}).get("value"), (a[k] or {}).get("value")
        if bv is not None and av is not None:
            rows.append((k, bv, av, round(av - bv, 3)))
    return {"caveats": caveats, "rows": rows}


def compare_markdown(c, b, a):
    L = [f"### Before ({b['analysis_utc']}) vs after ({a['analysis_utc']})"]
    L += [f"- CAVEAT: {x}" for x in c["caveats"]]
    L.append("\n| Metric | Before | After | Change |\n| --- | --- | --- | --- |")
    for name, bv, av, d in c["rows"]:
        if name in ("Score", "CLS"):
            L.append(f"| {name} | {bv} | {av} | {d:+} |")
        else:
            L.append(f"| {name} | {fmt_ms(bv)} | {fmt_ms(av)} | {d / 1000:+.2f} s |")
    L.append("\nLab only. Field (CrUX) needs the rolling 28-day window to reflect a deployment.")
    return "\n".join(L)


# --------------------------------------------------------------------------- CLI
def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch")
    f.add_argument("url")
    f.add_argument("--strategy", choices=("mobile", "desktop", "both"), default="both")
    f.add_argument("--locale", default="en")
    f.add_argument("--out", default="psi-reports")
    f.add_argument("--raw", action="store_true", help="keep screenshot payloads in saved JSON")
    f.add_argument("--json", action="store_true")
    s = sub.add_parser("summarize")
    s.add_argument("files", nargs="+")
    s.add_argument("--json", action="store_true")
    c = sub.add_parser("compare")
    c.add_argument("before")
    c.add_argument("after")
    c.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    if args.cmd == "fetch":
        try:
            url = validate_url(args.url)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
        host = re.sub(r"[^a-z0-9]+", "-", (urllib.parse.urlsplit(url).hostname or "site").lower()).strip("-")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        summaries, failed = [], []
        for strat in (("mobile", "desktop") if args.strategy == "both" else (args.strategy,)):
            try:
                data = fetch_one(url, strat, args.locale)
            except RuntimeError as e:
                failed.append(str(e))
                continue
            path = out / f"psi-{host}-{strat}-{stamp}.json"
            path.write_text(json.dumps(data if args.raw else slim(data), ensure_ascii=False), encoding="utf-8")
            summaries.append(summarize(data, str(path)))
        _emit(summaries, args.json)
        for msg in failed:
            print(f"error: {msg}", file=sys.stderr)
        return 1 if failed else 0

    if args.cmd == "summarize":
        summaries = [summarize(load(p), p) for p in args.files]
        _emit(summaries, args.json)
        return 0

    b, a = summarize(load(args.before), args.before), summarize(load(args.after), args.after)
    res = compare(b, a)
    print(json.dumps(res, indent=2) if args.json else compare_markdown(res, b, a))
    return 0


def _emit(summaries, as_json):
    if as_json:
        print(json.dumps(summaries, indent=2, ensure_ascii=False))
    else:
        print("\n\n".join(to_markdown(s) for s in summaries))


if __name__ == "__main__":
    sys.exit(main())
