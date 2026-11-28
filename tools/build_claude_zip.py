#!/usr/bin/env python3
"""Build dist/pagespeed-audit.zip for upload to Claude.ai (Skills).

Contains only what Claude needs: SKILL.md, references/ and scripts/.
Codex-only files (agents/openai.yaml, assets/) are left out.
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / ".agents/skills/pagespeed-audit"
OUT = ROOT / "dist/pagespeed-audit.zip"
INCLUDE = ("SKILL.md", "references", "scripts")

OUT.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for item in INCLUDE:
        base = SRC / item
        for f in sorted([base] if base.is_file() else base.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts:
                z.write(f, Path("pagespeed-audit") / f.relative_to(SRC))
print(f"wrote {OUT.relative_to(ROOT)}")
