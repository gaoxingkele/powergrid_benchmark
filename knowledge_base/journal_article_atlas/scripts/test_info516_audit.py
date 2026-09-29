import unittest
from audit_info516_printed_values import audit, holm


class Tests(unittest.TestCase):
    def test_holm_monotone(self):
        self.assertEqual(holm({"a":.01,"b":.03,"c":.04}), {"a":.03,"b":.06,"c":.06})

    def test_holm_bound(self):
        self.assertTrue(all(0<=p<=1 for p in holm({"a":.8,"b":.9}).values()))

    def test_published_cells_audit(self):
        result = audit()
        self.assertAlmostEqual(result["monthly_results"]["LSTM"]["equal_month_mean"], 1.8316666666666666)
        self.assertTrue(result["monthly_results"]["LSTM"]["exceeds_two_stage_2decimal_rounding_allowance"])
        self.assertTrue(result["not_raw_data_replication"])
        self.assertEqual(result["split_arithmetic"]["implied_train_rows"], 78983)
        self.assertEqual(result["split_arithmetic"]["implied_test_rows"], 8665)


if __name__ == "__main__":
    unittest.main()
