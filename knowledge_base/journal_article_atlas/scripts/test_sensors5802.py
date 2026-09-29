import unittest
from audit_sensors5802 import audit


class PrintedCellTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit()

    def test_correlation_mean(self):
        self.assertAlmostEqual(self.result["table3_equal_query_mean"],87.84)
        self.assertNotEqual(self.result["table3_equal_query_mean"],self.result["table3_prose_mean"])

    def test_negative_transfer_not_hidden(self):
        contrasts = self.result["table5_contrasts"]
        self.assertEqual(len(contrasts),15)
        self.assertEqual(self.result["table5_wins"],13)
        self.assertEqual([(x["query"],x["fraction"]) for x in contrasts if not x["nearest_better"]],[("QLD03",0.1),("QLD03",0.2)])

    def test_improvement_and_tradeoff(self):
        self.assertTrue(self.result["table6_all_random_metrics_improve"])
        self.assertTrue(self.result["table7_rmse_worsens"])
        self.assertTrue(self.result["table7_mape_improves"])

    def test_scope_not_promoted(self):
        self.assertTrue(self.result["not_raw_data_replication"])
        self.assertFalse(self.result["human_calibrated"])


if __name__ == "__main__":
    unittest.main()
