import unittest

import numpy as np

from scripts.mintou.build_statistical_audit_v2 import exact_signflip_p, paired_sign_balance


class ExactSignFlipTests(unittest.TestCase):
    def test_all_positive_ten_pairs_has_two_extreme_assignments(self) -> None:
        delta = np.arange(1.0, 11.0)
        self.assertEqual(exact_signflip_p(delta), 2 / (2**10))

    def test_zero_observed_mean_has_unit_p_value(self) -> None:
        self.assertEqual(exact_signflip_p(np.array([1.0, -1.0])), 1.0)

    def test_sign_balance_is_not_rank_weighted(self) -> None:
        self.assertEqual(paired_sign_balance(np.array([100.0, -1.0, -2.0])), -1 / 3)

    def test_sign_balance_ignores_zero_differences(self) -> None:
        self.assertEqual(paired_sign_balance(np.array([0.0, 2.0, -1.0, 3.0])), 1 / 3)


if __name__ == "__main__":
    unittest.main()
