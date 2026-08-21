import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("signflip", HERE / "exact_signflip_sensitivity.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class ExactSignFlipTests(unittest.TestCase):
    def test_all_positive_two_values(self):
        p, extreme, total = MOD.exact_signflip_p([1.0, 1.0])
        self.assertEqual(total, 4)
        self.assertEqual(extreme, 2)
        self.assertEqual(p, 0.5)

    def test_zero_differences_are_enumerated(self):
        p, extreme, total = MOD.exact_signflip_p([0.0, 0.0, 0.0])
        self.assertEqual((p, extreme, total), (1.0, 8, 8))

    def test_holm_known_vector_and_monotonicity(self):
        raw = [0.01, 0.04, 0.03, 0.20]
        got = MOD.holm_adjust(raw)
        self.assertEqual(got, [0.04, 0.09, 0.09, 0.20])
        ordered = sorted(zip(raw, got))
        self.assertTrue(all(a[1] <= b[1] for a, b in zip(ordered, ordered[1:])))

    def test_frozen_ledger_shape_and_expected_values(self):
        pred = HERE.parent / "formal_runs_v0_3_1" / "c2ges_v031_formal_20260808" / "predictions.jsonl"
        ledger = MOD.load_ledger(pred)
        self.assertEqual(len(ledger), 210)
        rows = MOD.compute(ledger)
        self.assertEqual(len(rows), 6)
        expected_p = [
            0.436767578125, 0.00030517578125, 0.0001220703125,
            0.20068359375, 0.006591796875, 0.0096435546875,
        ]
        self.assertEqual([r["exact_two_sided_signflip_p"] for r in rows], expected_p)
        self.assertTrue(all(r["enumerated_assignments"] == 32768 for r in rows))
        self.assertEqual(rows[0]["sign_counts"], {"positive": 7, "negative": 7, "tie": 1})
        self.assertEqual(rows[3]["sign_counts"], {"positive": 6, "negative": 8, "tie": 1})

    def test_duplicate_key_fails_closed(self):
        row = {"doc_id": "d", "budget": 5, "condition": "x", "metrics": {"rougeL_f1": 0.1}}
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "x.jsonl"
            p.write_text(json.dumps(row) + "\n" + json.dumps(row) + "\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                MOD.load_ledger(p)


if __name__ == "__main__":
    unittest.main()
