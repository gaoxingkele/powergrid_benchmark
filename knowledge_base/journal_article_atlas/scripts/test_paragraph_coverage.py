import copy
import json
import unittest
from audit_paragraph_coverage import RULES, audit

class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rules=json.loads(RULES.read_text(encoding='utf8'))['papers']

    def test_first_two_complete_third_is_not(self):
        for pid,cfg in self.rules.items():
            result=audit(pid,cfg)
            self.assertEqual(result['text_partition_complete'],pid!='p_61e82cc0ce8ee029')
            self.assertEqual(sum(result['counts'].values()),result['total_lines'])

    def test_deleted_abstract_cannot_pass(self):
        pid='p_71fe4f1acd7e01c5'
        cfg=copy.deepcopy(self.rules[pid])
        cfg['block_rules']=[r for r in cfg['block_rules'] if r[3]!='abstract']
        result=audit(pid,cfg)
        self.assertFalse(result['text_partition_complete'])
        self.assertEqual(result['counts']['unassigned'],12)

    def test_duplicate_classification_cannot_pass(self):
        pid='p_654ca5ab287c1e14'
        cfg=copy.deepcopy(self.rules[pid])
        cfg['block_rules'].append(cfg['block_rules'][0])
        result=audit(pid,cfg)
        self.assertFalse(result['text_partition_complete'])
        self.assertTrue(result['duplicates'])

    def test_changed_pdf_hash_cannot_pass(self):
        pid='p_71fe4f1acd7e01c5'
        cfg=copy.deepcopy(self.rules[pid])
        cfg['source_sha256']='0'*64
        with self.assertRaises(ValueError):
            audit(pid,cfg)

if __name__=='__main__':
    unittest.main()
