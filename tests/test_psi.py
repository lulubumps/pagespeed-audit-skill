import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / ".agents/skills/pagespeed-audit/scripts"))
import psi  # noqa: E402

FX = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FX / name).read_text())


class Summarize(unittest.TestCase):
    def setUp(self):
        self.s = psi.summarize(load("psi-sample-mobile-before.json"), "before")

    def test_score_is_scaled_to_100(self):
        self.assertEqual(self.s["lab"]["score"], 42)

    def test_lab_metrics_keep_units(self):
        self.assertEqual(self.s["lab"]["LCP"]["value"], 5600)
        self.assertEqual(self.s["lab"]["TBT"]["value"], 780)

    def test_crux_cls_is_unscaled_and_labelled_origin_fallback(self):
        page = self.s["field"]["page"]
        self.assertEqual(page["scope"], "origin (fallback)")
        self.assertEqual(page["metrics"]["CLS"]["p75"], 0.07)
        self.assertEqual(page["metrics"]["LCP"]["p75"], 3900)

    def test_findings_sorted_and_exclude_metrics_and_not_applicable(self):
        ids = [f["id"] for f in self.s["findings"]]
        self.assertEqual(ids[0], "render-blocking-resources")
        self.assertNotIn("largest-contentful-paint", ids)
        self.assertNotIn("redirects", ids)
        self.assertNotIn("viewport", ids)

    def test_lcp_element_and_phases(self):
        e = self.s["lcp_element"]
        self.assertEqual(e["selector"], "div.hero > img.wp-post-image")
        self.assertEqual(e["phases_ms"]["Load Delay"], 2400)

    def test_clean_run_has_no_flags(self):
        self.assertEqual(self.s["flags"], [])

    def test_blocked_run_is_flagged_and_field_unavailable(self):
        s = psi.summarize(load("psi-sample-mobile-blocked.json"))
        joined = " ".join(s["flags"])
        self.assertIn("runtime error", joined)
        self.assertIn("No performance score", joined)
        self.assertIn("challenge", joined)
        self.assertFalse(s["field"]["page"]["available"])
        self.assertIn("unavailable", psi.to_markdown(s))

    def test_origin_fallback_row_is_not_duplicated(self):
        md = psi.to_markdown(self.s)
        self.assertEqual(md.count("| origin (fallback) |"), 1)
        self.assertNotIn("| origin |", md)

    def test_markdown_renders(self):
        md = psi.to_markdown(self.s)
        self.assertIn("**Lab (Lighthouse)**", md)
        self.assertIn("origin (fallback)", md)


class Compare(unittest.TestCase):
    def test_deltas_and_caveats(self):
        b = psi.summarize(load("psi-sample-mobile-before.json"))
        a = psi.summarize(load("psi-sample-mobile-after.json"))
        res = psi.compare(b, a)
        score = next(r for r in res["rows"] if r[0] == "Score")
        self.assertEqual(score[3], 29)
        self.assertTrue(any("median of three" in c for c in res["caveats"]))

    def test_version_mismatch_is_reported(self):
        b = psi.summarize(load("psi-sample-mobile-before.json"))
        data = load("psi-sample-mobile-after.json")
        data["lighthouseResult"]["lighthouseVersion"] = "13.0.0"
        res = psi.compare(b, psi.summarize(data))
        self.assertTrue(any("Lighthouse version differs" in c for c in res["caveats"]))


class UrlValidation(unittest.TestCase):
    def test_accepts_public_urls(self):
        for u in ("https://example.com/", "http://example.com/blog?page=2", "https://sub.example.cl/a/b"):
            self.assertEqual(psi.validate_url(u), u)

    def test_rejects_unsafe_urls(self):
        bad = [
            "ftp://example.com", "https://user:pw@example.com/", "http://localhost:8080/",
            "http://192.168.1.10/", "http://127.0.0.1/", "https://intranet/", "https://app.internal/",
            "https://example.com/?token=abc", "https://example.com/?api_key=zzz",
            "https://example.com/#access_token=abc", "javascript:alert(1)",
        ]
        for u in bad:
            with self.assertRaises(ValueError, msg=u):
                psi.validate_url(u)

    def test_key_is_redacted(self):
        self.assertEqual(psi.redact("bad key SECRET123 here", "SECRET123"), "bad key [REDACTED] here")


class Slim(unittest.TestCase):
    def test_drops_screenshots(self):
        d = {"lighthouseResult": {"fullPageScreenshot": {"x": 1}, "audits": {"final-screenshot": {"details": {"data": "..."}}}}}
        out = psi.slim(d)
        self.assertNotIn("fullPageScreenshot", out["lighthouseResult"])
        self.assertNotIn("details", out["lighthouseResult"]["audits"]["final-screenshot"])


class AgentParity(unittest.TestCase):
    """Codex (.toml) and Claude Code (.md) subagents must carry the same instructions."""

    ROLES = ("psi-field", "psi-lab", "psi-implementation", "psi-review")

    def test_instructions_match(self):
        import re
        for role in self.ROLES:
            md = (ROOT / f".claude/agents/{role}.md").read_text()
            toml = (ROOT / f".codex/agents/{role}.toml").read_text()
            md_body = re.sub(r"\s+", " ", md.split("---\n", 2)[2]).strip()
            m = re.search(r'developer_instructions = """\n(.*?)\n"""', toml, re.S)
            self.assertIsNotNone(m, role)
            self.assertEqual(re.sub(r"\s+", " ", m.group(1)).strip(), md_body, role)
            self.assertIn('sandbox_mode = "read-only"', toml)
            self.assertIn("tools: Read, Grep, Glob", md)

    def test_claude_skill_is_the_shared_skill(self):
        link = ROOT / ".claude/skills/pagespeed-audit"
        self.assertEqual(link.resolve(), (ROOT / ".agents/skills/pagespeed-audit").resolve())


if __name__ == "__main__":
    unittest.main()
