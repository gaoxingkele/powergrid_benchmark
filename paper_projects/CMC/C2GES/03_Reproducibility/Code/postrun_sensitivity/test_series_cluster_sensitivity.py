import importlib.util
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("series_cluster", HERE / "series_cluster_sensitivity.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MOD)


class SeriesClusterTests(unittest.TestCase):
    def test_signflip_two_positive_values(self):
        self.assertEqual(MOD.exact_signflip([1.0, 1.0]), (0.5, 2, 4))

    def test_holm_known_values(self):
        self.assertEqual(MOD.holm([0.01, 0.04, 0.03, 0.2]), [0.04, 0.09, 0.09, 0.2])

    def test_frozen_public_analysis_shape(self):
        import json
        payload = json.loads(MOD.DEFAULT_INPUT.read_text(encoding="utf-8"))
        results = MOD.analyze(payload, MOD.load_series(MOD.DEFAULT_METADATA))
        self.assertEqual(len(results), 6)
        self.assertTrue(all(row["n_reports"] == 15 for row in results))
        self.assertTrue(all(row["n_series"] == 10 for row in results))
        self.assertTrue(all(row["enumerated_assignments"] == 1024 for row in results))


if __name__ == "__main__":
    unittest.main()
