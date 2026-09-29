import json
import unittest
from audit_tla11252 import CASE, audit, implied_variance, common_intersection


class MetricAuditTests(unittest.TestCase):
    def test_shared_target_identity(self):
        self.assertTrue(common_intersection([implied_variance(.5, .1), implied_variance(.75, .05)]))

    def test_rounding_tolerance(self):
        self.assertTrue(common_intersection([implied_variance(.5, .1), implied_variance(.5, .1004)]))

    def test_printed_tables(self):
        result = audit(json.loads(CASE.read_text(encoding='utf-8')))
        self.assertEqual(set(result['tables']), {'2', '3'})
        for table in result['tables'].values():
            self.assertFalse(table['common_variance_possible_with_rounding'])
        self.assertAlmostEqual(result['tables']['2']['implied_target_variances']['SVR']['point'], .145/1.853)

    def test_invalid_domain(self):
        with self.assertRaises(ValueError):
            implied_variance(1, .1)


if __name__ == '__main__':
    unittest.main()
