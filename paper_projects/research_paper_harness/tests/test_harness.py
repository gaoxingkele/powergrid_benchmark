import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "harness.py"
SPEC = importlib.util.spec_from_file_location("research_paper_harness", MODULE_PATH)
HARNESS = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = HARNESS
SPEC.loader.exec_module(HARNESS)


def minimal_profile() -> dict:
    return {
        "schema_version": "1.0",
        "portfolio_id": "test",
        "workspace_root": ".",
        "authority": {
            "canonical_roots": ["canonical"],
            "legacy_roots": ["legacy"],
            "incident_roots": [],
            "required_paths": ["paper.md"],
            "expected_hashes": [],
        },
        "papers": [
            {
                "id": "p1",
                "title": "Test",
                "target": "Journal",
                "manuscript": "paper.md",
                "pdf": "paper.pdf",
                "evidence_root": "evidence",
            }
        ],
        "stages": [
            {
                "id": "intake",
                "title": "Intake",
                "depends_on": [],
                "status": "complete",
                "gate": "files exist",
                "artifacts": ["paper.md"],
                "commands": [],
                "auto_safe": False,
            }
        ],
        "manifest_paths": ["paper.md", "paper.pdf"],
        "hard_rules": [],
        "manual_gates": [],
    }


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "canonical").mkdir()
        (self.root / "legacy").mkdir()
        (self.root / "evidence").mkdir()
        (self.root / "paper.md").write_text("paper", encoding="utf-8")
        (self.root / "paper.pdf").write_bytes(b"%PDF-test")

    def tearDown(self):
        self.temp.cleanup()

    def test_minimal_profile_passes(self):
        issues = HARNESS.audit_profile(minimal_profile(), self.root)
        self.assertFalse([issue for issue in issues if issue.level == "ERROR"])

    def test_hash_mismatch_is_detected(self):
        profile = minimal_profile()
        profile["authority"]["expected_hashes"] = [{"path": "paper.md", "sha256": "0" * 64}]
        issues = HARNESS.audit_profile(profile, self.root)
        self.assertIn("HASH_MISMATCH", {issue.code for issue in issues})

    def test_cycle_is_detected(self):
        profile = minimal_profile()
        profile["stages"].append(
            {
                "id": "write",
                "title": "Write",
                "depends_on": ["intake"],
                "status": "complete",
                "gate": "done",
                "artifacts": [],
                "commands": [],
                "auto_safe": False,
            }
        )
        profile["stages"][0]["depends_on"] = ["write"]
        issues = HARNESS.audit_profile(profile, self.root)
        self.assertIn("STAGE_CYCLE", {issue.code for issue in issues})

    def test_authority_overlap_is_detected(self):
        profile = minimal_profile()
        profile["authority"]["legacy_roots"] = ["canonical/old"]
        (self.root / "canonical" / "old").mkdir()
        issues = HARNESS.audit_profile(profile, self.root)
        self.assertIn("AUTHORITY_OVERLAP", {issue.code for issue in issues})

    def test_manifest_hashes_files(self):
        manifest = HARNESS.build_manifest(minimal_profile(), self.root)
        self.assertEqual(manifest["entries"][0]["type"], "file")
        self.assertEqual(len(manifest["entries"][0]["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
