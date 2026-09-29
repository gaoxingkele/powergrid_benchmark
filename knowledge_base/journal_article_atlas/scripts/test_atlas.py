import unittest
from pathlib import Path
import json
import sqlite3
from atlas import ROOT, EQ, CAPTION, infer_venue, percentile, validate_observation, summaries
from definitions import fields

class Tests(unittest.TestCase):
    def test_unique_fields(self):
        ids=[r['field_id'] for r in fields()]
        self.assertEqual(len(ids),len(set(ids)))
        for name in ['paper.ablation_count','paragraph.role_primary','section.core_logic','difficulty.statistics','conclusion.limits']:
            self.assertIn(name,ids)
    def test_count_definition_not_max(self):
        labels={EQ.fullmatch(x)[1] for x in ['(1)','(3)','(3)','(3a)'] if EQ.fullmatch(x)}
        self.assertEqual(len(labels),3)
        self.assertIsNone(EQ.fullmatch('Equation (99) is used.'))
    def test_caption_boundary(self):
        self.assertIsNotNone(CAPTION.match('Figure 2. Architecture'))
        self.assertIsNone(CAPTION.match('See Figure 2 for the results.'))
    def test_venue(self):
        self.assertEqual(infer_venue(Path('x.pdf'),'10.3390/en17010123'),'Energies')
        self.assertEqual(infer_venue(Path('IEEE Access/a.pdf'),'10.1109/ACCESS.2024.1234567'),'IEEE Access')
    def test_missing_not_zero(self):
        obs=dict(entity_id='p',field_id='paper.ablation_count',value=0,status='not_assessed',evidence=[],method='test',annotator=None,version='0.1')
        with self.assertRaises(ValueError): validate_observation(obs)
        obs['value']=None; self.assertTrue(validate_observation(obs))
    def test_evidence_required(self):
        obs=dict(entity_id='p',field_id='paper.pages',value=4,status='verified',evidence=[],method='test',annotator='test',version='0.1')
        with self.assertRaises(ValueError): validate_observation(obs)
    def test_wrong_type(self):
        obs=dict(entity_id='p',field_id='paper.pages',value='four',status='automatic_candidate',evidence=[{'source_sha256':'a'*64,'locator':{}}],method='test',annotator=None,version='0.1')
        with self.assertRaises(ValueError): validate_observation(obs)
    def test_example_observations(self):
        example=json.loads((ROOT/'examples/applsci_partial_case.json').read_text(encoding='utf-8'))
        for obs in example['observations']: self.assertTrue(validate_observation(obs))
    def test_source_required(self):
        obs=dict(entity_id='p',field_id='paper.pages',value=3,status='verified',evidence=[{}],method='test',annotator=None,version='0.1')
        with self.assertRaises(ValueError): validate_observation(obs)
    def test_quantile(self): self.assertEqual(percentile([1,2,3,4],.5),2.5)
    def test_no_profile_promotion(self):
        rows=[{'venue':'X','relevance_candidate':'uncertain','article_type_candidate':'unclassified','metrics':{'x':None}}, {'venue':'X','relevance_candidate':'uncertain','article_type_candidate':'unclassified','metrics':{'x':4}}]
        s=summaries(rows)[0]
        self.assertEqual(s['metrics']['x']['n_valid_candidates'],1)
        self.assertEqual(s['metrics']['x']['mean'],4)
        self.assertIsNone(s['verified_profile'])
    def test_generated_foreign_keys(self):
        path=ROOT/'outputs/atlas.sqlite'
        if not path.exists(): self.skipTest('run atlas.py first')
        with sqlite3.connect(path) as db:
            self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(),[])
            self.assertEqual(db.execute("SELECT count(*) FROM observation WHERE status='verified'").fetchone()[0],0)
    def test_skill_query_fails_closed(self):
        if not (ROOT/'outputs/atlas.sqlite').exists(): self.skipTest('run atlas.py first')
        from query_atlas import query
        result=query('Energies')
        self.assertEqual(result['observations'],[])
        self.assertEqual(result['calibration_status'],'NOT_CALIBRATED')
        self.assertIsNone(result['acceptance_threshold'])

if __name__=='__main__': unittest.main(verbosity=2)
