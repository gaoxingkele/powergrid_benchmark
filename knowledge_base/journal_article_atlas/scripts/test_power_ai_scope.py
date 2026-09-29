"""Regression tests for scope evidence gates, not scientific outcome correctness."""
import copy
import unittest
from finalize_power_ai_scope import merge, read, OUT, ROOT

class ScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=read(OUT/'scope_records.json')
    def test_complete(self):
        ids=[r['paper_id'] for r in self.rows]
        expected=[r['paper_id'] for r in read(ROOT/'outputs/corpus_manifest.json')['articles']]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),set(expected))
    def test_no_full_calibration_promotion(self):
        for r in self.rows:
            self.assertFalse(r['full_semantic_calibration'])
            self.assertIsNone(r['difficulty_profile'])
            self.assertEqual(r['object_counts_status'],'automatic_candidate')
    def test_source_warning_fails_closed(self):
        r=next(r for r in self.rows if r['paper_id']=='p_ab728f9c94d0f7ca')
        self.assertEqual(r['scope_status'],'requires_review')
        self.assertFalse(r['core_scope_eligible'])
    def test_version_conflicts_isolated(self):
        for pid in ['p_09c8eed2bb3f2e28','p_cfabc8737fb852fe']:
            r=next(r for r in self.rows if r['paper_id']==pid)
            self.assertFalse(r['venue_profile_eligible'])
            self.assertFalse(r['journal_core_candidate'])
    def test_title_fix_not_venue_conflict(self):
        r=next(r for r in self.rows if r['paper_id']=='p_9c09ca32bb944981')
        self.assertNotEqual(r['title'],r['manifest_title'])
        self.assertTrue(r['venue_profile_eligible'])
    def test_ai_auxiliary_explicit(self):
        r=next(r for r in self.rows if r['paper_id']=='p_d2e16e5d3f9b1b3f')
        self.assertEqual(r['ai_role'],'auxiliary')
    def test_non_power_load_excluded(self):
        r=next(r for r in self.rows if r['paper_id']=='p_cf3631ac60ffb811')
        self.assertEqual(r['decision'],'out_of_scope')
    def test_invalid_ids_rejected(self):
        with self.assertRaises(ValueError):
            merge({'articles':[]},[('bad',[{'paper_id':'bad'}])],{'records':[]},{})

if __name__=='__main__':
    unittest.main()
