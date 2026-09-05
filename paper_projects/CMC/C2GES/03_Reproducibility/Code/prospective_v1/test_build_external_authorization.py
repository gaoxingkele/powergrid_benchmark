from __future__ import annotations

import argparse
import json
import tempfile
import unittest
from pathlib import Path

from build_external_authorization import build


class ExternalAuthorizationBuilderTests(unittest.TestCase):
    def test_draft_protocol_refuses_before_private_dataset_access(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            config = root / "config.json"
            external = root / "external.json"
            factorial = root / "factorial.json"
            tuning = root / "tuning.json"
            config.write_text(json.dumps({"status": "DRAFT_NOT_FROZEN", "mode": "EXTERNAL_CONFIRMATORY_ONE_ATTEMPT"}), encoding="utf-8")
            external.write_text(json.dumps({"protocol_status": "DRAFT_NOT_FROZEN"}), encoding="utf-8")
            factorial.write_text(json.dumps({"protocol_status": "DRAFT_NOT_FROZEN"}), encoding="utf-8")
            tuning.write_text(json.dumps({"status": "DRAFT_NOT_FROZEN"}), encoding="utf-8")
            missing_dataset = root / "must_not_be_opened.jsonl"
            args = argparse.Namespace(
                config=config, external_protocol=external, factorial_protocol=factorial,
                tuning_decision=tuning, tuning_grid=root / "missing-grid.csv",
                inventory=root / "missing-inventory.csv",
                seen_exclusion_registry=root / "missing-exclusions.csv",
                layout_candidate_audit=root / "missing-layout.csv", layout_audit_summary=root / "missing-layout.json",
                ablation_registry=root / "missing-ablation.json", dataset=missing_dataset,
                model_snapshot=root / "missing-model", output_dir=root / "out",
                attempt_registry=root / "attempt.json", authorization_output=root / "authorization.json",
                run_id="formal-test", operator="unit-test", administrator_confirms_no_content_review=False,
            )
            with self.assertRaises((RuntimeError, ValueError)):
                build(args)
            self.assertFalse(args.authorization_output.exists())
            self.assertFalse(args.attempt_registry.exists())


if __name__ == "__main__":
    unittest.main()
