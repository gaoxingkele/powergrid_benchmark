import importlib.util, json, math, sqlite3, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import comparison_v2 as cmp

class V2DesignTests(unittest.TestCase):
    def test_float_pairwise_boundary(self):
        self.assertTrue(cmp.value_equal(0.49e-6,0.51e-6))
        self.assertFalse(cmp.value_equal(0.0,2.0e-6))
        self.assertFalse(cmp.value_equal(float("inf"),float("inf")))
        self.assertFalse(cmp.value_equal(float("nan"),float("nan")))

    def test_duplicate_preserving_bipartite_multiset(self):
        gold=[("x",0.0),("x",0.9e-6),("x",5.0)]
        pred=[("x",0.4e-6),("x",0.5e-6),("x",5.0)]
        self.assertTrue(cmp.rows_equal(pred,gold,ordered=False))
        self.assertFalse(cmp.rows_equal(pred[:-1],gold,ordered=False))
        self.assertFalse(cmp.rows_equal([("x",0.4e-6)]*3,gold,ordered=False))

    def test_order_null_numeric_affinity_and_headers(self):
        self.assertFalse(cmp.rows_equal([(2,),(1,)],[(1,),(2,)],ordered=True))
        self.assertTrue(cmp.rows_equal([(1,None)],[(1.0,None)],ordered=True))
        self.assertFalse(cmp.rows_equal([(1,None)],[(1.0,"None")],ordered=True))
        d=cmp.header_diagnostics(["wrong_alias"],["asset_count"],["asset_count"])
        self.assertFalse(d["prediction_vs_gold_header_match"])
        self.assertEqual(cmp.COLUMN_POLICY,"headers_are_diagnostic_only_denotation_is_primary")

    def test_stage_a_has_no_benchmark_or_ledger_cli(self):
        text=(ROOT/"stage_a_generate_states.py").read_text(encoding="utf-8").lower()
        for forbidden in ["--questions","--predictions","--scores","questions.jsonl","predictions.jsonl","scores.jsonl"]:
            self.assertNotIn(forbidden,text)

    def test_two_clean_stage_a_runs_match(self):
        a=json.loads((ROOT/"states_v2b/STAGE_A_STATE_MANIFEST.json").read_text())
        b=json.loads((ROOT/"states_v2b_rerun/STAGE_A_STATE_MANIFEST.json").read_text())
        aa={x["state"]:(x["state_sha256"],x["trace_sha256"]) for x in a["states"]}
        bb={x["state"]:(x["state_sha256"],x["trace_sha256"]) for x in b["states"]}
        self.assertEqual(aa,bb);self.assertEqual(len(aa),18)
        self.assertTrue(all(x["integrity_check"]==["ok"] and x["foreign_key_violations"]==0 for x in a["states"]))

    def test_gold_only_coverage_and_order_denominators(self):
        r=json.loads((ROOT/"pre_score_v2b/PRE_SCORE_GOLD_COVERAGE.json").read_text())
        self.assertEqual(r["coverage"]["changed_union_n"],180)
        self.assertTrue(r["coverage"]["all_empty_nonempty_in_at_least_two_states"])
        self.assertEqual(r["denominators"]["order_sensitive"],114)
        self.assertEqual(r["denominators"]["top_k"],18)
        self.assertEqual(r["order_tie"]["machine_eligible_n"]+r["order_tie"]["hold_n"],114)

    def test_independent_order_consensus_forces_all_114_to_hold(self):
        a=json.loads((ROOT.parent/"semantic_order_review/reviewer_a.json").read_text(encoding="utf-8"))
        b=json.loads((ROOT.parent/"semantic_order_review/reviewer_b.json").read_text(encoding="utf-8"))
        self.assertEqual(a["summary"]["verdict_counts"]["TOTAL_ORDER_VALID"],0)
        self.assertEqual(b["summary"]["verdict_counts"]["TOTAL_ORDER_VALID"],0)
        self.assertEqual(a["summary"]["reviewed_order_sensitive_count"],114)
        self.assertEqual(b["summary"]["reviewed"],114)

if __name__=="__main__":unittest.main()
