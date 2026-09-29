import itertools
import unittest
from audit_tfe_factorial import factorial_contrasts, make_report


class FactorialTests(unittest.TestCase):
    def test_known_polynomial(self):
        configs = {str(c): c for c in itertools.product((0, 1), repeat=3)}
        # y=2+3a+5b+7c+11ab+13abc; exact finite differences known.
        rows = {name: [2+3*a+5*b+7*c+11*a*b+13*a*b*c]
                for name, (a,b,c) in configs.items()}
        result = factorial_contrasts(configs, rows, ['a','b','c'], ['y'])
        contrasts = {tuple(r['factors']): r['finite_difference']['y']
                     for r in result['averaged_finite_differences']}
        self.assertEqual(contrasts[('a','b','c')], 13)
        self.assertEqual(contrasts[('a','b')], 17.5)
        self.assertEqual(contrasts[('a',)], 11.75)
        self.assertEqual(len(result['conditional_effects']), 12)

    def test_missing_or_duplicate_cell_rejected(self):
        for configs in ({'x':[0], 'y':[0]}, {'x':[0]}):
            with self.assertRaises(ValueError):
                factorial_contrasts(configs, {n:[1] for n in configs}, ['a'], ['y'])

    def test_published_negative_effect_preserved(self):
        report = make_report()
        pair = next(r for r in report['conditional_effects'] if r['off']=='M1' and r['on']=='M4')
        self.assertEqual(pair['on_minus_off']['MAPE'], .175)
        self.assertEqual(pair['on_minus_off']['RMSE'], -14.155)


if __name__ == '__main__':
    unittest.main()
