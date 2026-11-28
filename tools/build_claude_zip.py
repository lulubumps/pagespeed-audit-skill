#!/usr/bin/env python3
"""Build the skill ZIP for upload to Claude.ai (Skills).

  python3 tools/build_claude_zip.py          -> dist/pagespeed-audit.zip
  python3 tools/build_claude_zip.py --full   -> dist/pagespeed-audit-full.zip

The default package contains only what Claude needs: SKILL.md, references/ and
scripts/. Codex-only files (agents/openai.yaml, assets/) are left out.

--full also bundles the Claude full-audit extension from .claude/pagespeed/
(all four Lighthouse categories, CMS and regression guidance) as
references/full-audit/ and scripts/psi_full.py, and appends a short "Full audit
mode" section to the packaged SKILL.md. Paths are rewritten for the package.
"""
import argparse
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".agents/skills/pagespeed-audit"
EXT = ROOT / ".claude/pagespeed"
INCLUDE = ("SKILL.md", "references", "scripts")
EXT_REFS = ("report", "measurement", "roles", "diagnostics")

FULL_SECTION = """
## Full audit mode (all four Lighthouse categories)

Use this mode when the user asks for a complete audit, CMS-specific recommendations or before-and-after verification. It extends the workflow above; every rule above still applies.

- **Report:** follow [the complete report format](references/full-audit/report.md): a short prioritized summary, then every evidenced finding across performance, accessibility, best practices and SEO, keeping audit IDs and marking manual checks, errors and coverage gaps.
- **Measurement:** `python3 scripts/psi_full.py fetch <url> --strategy both --out psi-reports` requests all four categories. Use `summarize` and `compare` on existing reports. Read [the measurement rules](references/full-audit/measurement.md).
- **Roles and platforms:** read [the role workflow](references/full-audit/roles.md) and [platform diagnostics](references/full-audit/diagnostics.md). Here there are no project subagents, so run scope, field, lab, CMS, third-party, implementation, regression and review yourself in sequence, as the role workflow describes.
"""


def rewrite(text):
    """Adapt extension text from repository paths to package paths."""
    text = text.replace(" When this audit is packaged for Claude.ai, the same script is `scripts/psi_full.py`.", "")
    text = text.replace(
        "Use installed Claude Code project agents (`.claude/agents/psi-*.md`) when supported. "
        "Subagents cannot spawn other subagents, so the coordinator runs every step. "
        "Run the roles in sequence yourself when delegation is unavailable, as in Claude.ai.",
        "This package has no project subagents, so run the roles in sequence yourself and keep each role's output separate.",
    )
    text = text.replace(".claude/pagespeed/scripts/psi.py", "scripts/psi_full.py")
    return text.replace(".claude/pagespeed/references/", "references/full-audit/")


def build(full=False, out=None):
    out = Path(out) if out else ROOT / "dist" / ("pagespeed-audit-full.zip" if full else "pagespeed-audit.zip")
    out.parent.mkdir(parents=True, exist_ok=True)
    pkg = Path("pagespeed-audit")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUDE:
            base = SRC / item
            for f in sorted([base] if base.is_file() else base.rglob("*")):
                if not f.is_file() or "__pycache__" in f.parts:
                    continue
                arc = pkg / f.relative_to(SRC)
                if full and item == "SKILL.md":
                    z.writestr(str(arc), f.read_text(encoding="utf-8").rstrip("\n") + "\n" + FULL_SECTION)
                else:
                    z.write(f, arc)
        if full:
            for name in EXT_REFS:
                text = (EXT / "references" / f"{name}.md").read_text(encoding="utf-8")
                z.writestr(str(pkg / "references/full-audit" / f"{name}.md"), rewrite(text))
            z.write(EXT / "scripts/psi.py", pkg / "scripts/psi_full.py")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--full", action="store_true", help="include the full-audit extension")
    ap.add_argument("--out", help="output path (default: dist/...)")
    args = ap.parse_args()
    path = build(args.full, args.out)
    try:
        print(f"wrote {path.relative_to(ROOT)}")
    except ValueError:
        print(f"wrote {path}")
