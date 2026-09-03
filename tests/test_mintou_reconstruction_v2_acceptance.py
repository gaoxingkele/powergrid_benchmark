from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "mintou" / "harness_reconstruction_v2_acceptance.py"
SPEC = importlib.util.spec_from_file_location("harness_reconstruction_v2_acceptance", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class ReconstructionV2AcceptanceTests(unittest.TestCase):
    def test_four_locked_titles_are_unique_and_nonempty(self) -> None:
        titles = [meta["title"] for meta in MODULE.PROJECTS.values()]
        self.assertEqual(len(titles), 4)
        self.assertEqual(len(set(titles)), 4)
        self.assertTrue(all(title.strip() == title and title for title in titles))

    def test_each_project_has_complete_claim_id_contract(self) -> None:
        for meta in MODULE.PROJECTS.values():
            prefix = meta["paper_id"] + "-C"
            self.assertEqual(len(meta["claim_ids"]), 8)
            self.assertTrue(all(item.startswith(prefix) for item in meta["claim_ids"]))

    def test_phase_chain_is_monotonic(self) -> None:
        previous = ()
        for phase in MODULE.PHASES:
            current = MODULE.CHECKS[phase]
            self.assertEqual(current[: len(previous)], previous)
            self.assertGreaterEqual(len(current), len(previous))
            previous = current

    def test_release_gate_includes_all_prior_checks(self) -> None:
        self.assertEqual(MODULE.CHECKS["release"][-1], MODULE.check_release)
        self.assertIn(MODULE.check_final_integrity, MODULE.CHECKS["release"])
        self.assertIn(MODULE.check_evidence, MODULE.CHECKS["release"])


if __name__ == "__main__":
    unittest.main()
