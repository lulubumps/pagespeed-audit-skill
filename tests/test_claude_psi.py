import importlib.util
import json
import re
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


psi = _load("claude_psi", ".claude/pagespeed/scripts/psi.py")
builder = _load("build_claude_zip", "tools/build_claude_zip.py")

NEW_ROLES = ("psi-scope", "psi-cms", "psi-third-party", "psi-regression")
ALL_ROLES = ("psi-field", "psi-lab", "psi-implementation", "psi-review") + NEW_ROLES


def load(name):
    return json.loads((ROOT / "tests/fixtures" / name).read_text())


def norm(text):
    return re.sub(r"\s+", " ", text).strip()


class ClaudeFullAudit(unittest.TestCase):
    def test_findings_cover_later_audits_and_report_pending_checks(self):
        data = load("psi-sample-mobile-before.json")
        lighthouse = data["lighthouseResult"]
        issues = [f"contrast-{index}" for index in range(12)]
        lighthouse["audits"].update({k: {"title": k, "scoreDisplayMode": "numeric", "score": 0.95} for k in issues})
        lighthouse["audits"]["manual-check"] = {"scoreDisplayMode": "manual"}
        lighthouse["audits"]["audit-error"] = {"scoreDisplayMode": "error"}
        lighthouse["categories"]["accessibility"] = {
            "score": 0.95, "auditRefs": [{"id": k} for k in issues + ["manual-check", "audit-error"]]
        }
        summary = psi.summarize(data)
        rows = {item["id"]: item for item in summary["findings"]}
        for key in issues:
            self.assertEqual(rows[key]["categories"], ["accessibility"])
            self.assertIn(key, psi.to_markdown(summary))
        self.assertNotIn("manual-check", rows)
        self.assertNotIn("audit-error", rows)
        self.assertEqual({x["status"] for x in summary["pending_checks"]}, {"manual", "error"})
        self.assertEqual(summary["missing_categories"], ["best-practices", "seo"])

    def test_script_requests_all_four_categories(self):
        self.assertEqual(psi.PSI_CATEGORIES, ("performance", "accessibility", "best-practices", "seo"))


class ClaudeAgents(unittest.TestCase):
    def test_all_eight_agents_are_read_only_claude_subagents(self):
        for role in ALL_ROLES:
            with self.subTest(role=role):
                md = (ROOT / ".claude/agents" / f"{role}.md").read_text()
                self.assertIn(f"name: {role}\n", md)
                self.assertIn("tools: Read, Grep, Glob", md)
                self.assertNotIn("Bash", md.split("---")[1])
                self.assertIn("description: ", md)

    def test_new_agents_match_codex_instructions(self):
        for role in NEW_ROLES:
            with self.subTest(role=role):
                md = (ROOT / ".claude/agents" / f"{role}.md").read_text()
                toml = (ROOT / ".codex/agents" / f"{role}.toml").read_text()
                body = norm(md.split("---\n", 2)[2])
                m = re.search(r'developer_instructions = """\n(.*?)\n"""', toml, re.S)
                self.assertIsNotNone(m)
                self.assertEqual(norm(m.group(1)), body)


class ClaudeMemoryFile(unittest.TestCase):
    def test_claude_md_links_resolve(self):
        text = (ROOT / "CLAUDE.md").read_text()
        links = re.findall(r"\]\((\.claude/[^)]+)\)", text)
        self.assertGreaterEqual(len(links), 3)
        for link in links:
            self.assertTrue((ROOT / link).is_file(), link)
        for role in NEW_ROLES:
            self.assertIn(role, text)


class FullZip(unittest.TestCase):
    def _names_and_text(self, full):
        with tempfile.TemporaryDirectory() as tmp:
            out = builder.build(full, Path(tmp) / "x.zip")
            with zipfile.ZipFile(out) as z:
                return set(z.namelist()), {n: z.read(n).decode("utf-8", "ignore") for n in z.namelist()}

    def test_default_zip_is_unchanged_baseline(self):
        names, _ = self._names_and_text(False)
        self.assertEqual(names, {
            "pagespeed-audit/SKILL.md", "pagespeed-audit/scripts/psi.py",
            *{f"pagespeed-audit/references/{n}.md" for n in ("diagnostics", "measurement", "report", "roles", "thresholds")},
        })

    def test_full_zip_bundles_extension_with_package_paths(self):
        names, text = self._names_and_text(True)
        for n in ("report", "measurement", "roles", "diagnostics"):
            self.assertIn(f"pagespeed-audit/references/full-audit/{n}.md", names)
        self.assertIn("pagespeed-audit/scripts/psi_full.py", names)
        self.assertIn("Full audit mode", text["pagespeed-audit/SKILL.md"])
        added = [p for p in text if "/full-audit/" in p or p.endswith("psi_full.py")]
        self.assertEqual(len(added), 5)
        for path in added:
            self.assertNotIn(".claude/", text[path], path)
        self.assertNotIn(".claude/", text["pagespeed-audit/SKILL.md"].split("## Full audit mode")[1])
        # every relative link in the packaged SKILL.md must exist in the package
        for link in re.findall(r"\]\((references/[^)]+)\)", text["pagespeed-audit/SKILL.md"]):
            self.assertIn(f"pagespeed-audit/{link}", names, link)
        self.assertIn("scripts/psi_full.py", text["pagespeed-audit/references/full-audit/measurement.md"])


if __name__ == "__main__":
    unittest.main()
