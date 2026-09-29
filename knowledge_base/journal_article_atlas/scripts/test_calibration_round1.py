"""Validate round boundaries and provenance; not a semantic gold-standard test."""
import json
import unittest
from pathlib import Path
from atlas import validate_observation

ROOT = Path(__file__).resolve().parents[1] / 'calibration/2026-09-13_round1'

def read(name):
    return json.loads((ROOT / name).read_text(encoding='utf8'))

class CalibrationTests(unittest.TestCase):
    def test_observation_scope(self):
        observations = read('source_screened_observations.json')
        self.assertEqual(len(observations), 42)
        for obs in observations:
            validate_observation(obs)
            self.assertIn(obs['field_id'], {'paper.topic', 'paper.relevance', 'paper.pages'})

    def test_no_unsupported_journal_means(self):
        profiles = read('cohort_profiles.json')
        self.assertEqual(sum(p['source_screened_n'] for p in profiles), 14)
        for p in profiles:
            self.assertIsNone(p['journal_mean'])
            self.assertIsNone(p['difficulty_profile'])
            self.assertEqual(p['full_annotation_n'], 0)

    def test_mixed_task_separation(self):
        records = {r['paper_id']: r for r in read('reviewed_records.json')}
        self.assertEqual(records['p_5908282d0c137859']['task'], 'traffic_proxy_plus_electric_load')
        self.assertEqual(records['p_e2822d4e02526031']['task'], 'multi_energy_load_forecasting')
        self.assertNotEqual(records['p_5908282d0c137859']['task'], 'electric_load_forecasting')

    def test_no_silent_parser_replacement(self):
        for r in read('reviewed_records.json'):
            for key in ('v0_metrics', 'v1_metrics', 'v2_metrics', 'source_sha256', 'source_path'):
                self.assertIn(key, r)
            self.assertEqual(len(r['source_sha256']), 64)
        self.assertEqual(len(read('parser_disagreements.json')), 8)

if __name__ == '__main__':
    unittest.main()
