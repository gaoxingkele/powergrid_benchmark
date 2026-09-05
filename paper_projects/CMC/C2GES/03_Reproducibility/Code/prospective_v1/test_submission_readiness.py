from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from submission_readiness import evaluate


class SubmissionReadinessTests(unittest.TestCase):
    def test_current_protocol_snapshot_is_rejected(self) -> None:
        root = Path(__file__).resolve().parents[3]
        result = evaluate(root)
        self.assertEqual(result["status"], "NOT_READY")
        codes = {row["code"] for row in result["findings"]}
        self.assertIn("E1_PROTOCOL_NOT_FROZEN", codes)
        self.assertIn("E1_RUN_MANIFEST_INVALID", codes)
        self.assertIn("MANUSCRIPT_NOT_BACKFILLED", codes)
        self.assertIn("FINAL_EVIDENCE_LOCK_MISSING_OR_INVALID", codes)

    def test_marker_only_fixture_fails_closed_without_exception(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "C2GES_RELEASE_MARKER.json").write_text("{}\n", encoding="utf-8")
            result = evaluate(root)
            self.assertFalse(result["submission_ready"])
            self.assertGreater(result["finding_count"], 10)

    def test_invalid_final_lock_hash_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "C2GES_RELEASE_MARKER.json").write_text("{}\n", encoding="utf-8")
            lock = root / "03_Reproducibility/Data/submission_final/SUBMISSION_EVIDENCE_LOCK.json"
            lock.parent.mkdir(parents=True)
            lock.write_text(json.dumps({"status": "SUBMISSION_FINAL", "sha256": {"missing.txt": "0" * 64}}), encoding="utf-8")
            result = evaluate(root)
            codes = {row["code"] for row in result["findings"]}
            self.assertIn("FINAL_EVIDENCE_FILE_MISSING", codes)
            self.assertIn("FINAL_EVIDENCE_HASHES_INCOMPLETE", codes)


if __name__ == "__main__":
    unittest.main()
