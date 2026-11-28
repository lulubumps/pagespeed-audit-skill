import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("codex_psi", ROOT / ".codex/pagespeed/scripts/psi.py")
psi = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(psi)


def load(name):
    return json.loads((ROOT / "tests/fixtures" / name).read_text())


class CodexAudit(unittest.TestCase):
    def test_findings_cover_later_audits_and_report_pending_checks(self):
        data = load("psi-sample-mobile-before.json")
        lighthouse = data["lighthouseResult"]
        issues = [f"contrast-{index}" for index in range(12)]
        lighthouse["audits"].update({
            key: {"title": key, "scoreDisplayMode": "numeric", "score": 0.95} for key in issues
        })
        lighthouse["audits"]["manual-check"] = {"scoreDisplayMode": "manual"}
        lighthouse["audits"]["audit-error"] = {"scoreDisplayMode": "error"}
        lighthouse["categories"]["accessibility"] = {
            "score": 0.95, "auditRefs": [{"id": key} for key in issues + ["manual-check", "audit-error"]]
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

    def test_codex_roles_are_read_only(self):
        for role in ("psi-scope", "psi-cms", "psi-third-party", "psi-regression"):
            with self.subTest(role=role):
                path = ROOT / ".codex/agents" / f"{role}.toml"
                config = path.read_text()
                self.assertIn(f'name = "{role}"', config)
                self.assertIn('sandbox_mode = "read-only"', config)
