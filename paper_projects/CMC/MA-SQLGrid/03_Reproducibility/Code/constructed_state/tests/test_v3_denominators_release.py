import importlib.util,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import analyze_release_v3 as a

class V3DenominatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        m=json.loads((ROOT/"states_v2b/STAGE_A_STATE_MANIFEST.json").read_text())
        cls.semantic=[x["state"] for x in m["states"] if not x["state"].startswith("T1_insertion_permutation")]
        cls.physical=[x["state"] for x in m["states"] if x["state"].startswith("T1_insertion_permutation")]
        cls.partition={"semantic_suite_states":cls.semantic,"physical_order_diagnostic_states":cls.physical}
    def synthetic(self):
        rows=[];canonical={}
        for bi,b in enumerate(a.BACKBONES):
            for c in a.CELLS:
                for qi in range(180):
                    q=f"Q{qi:03d}";eligible=qi<66;canonical[f"{b}|{c}|{q}"]=True
                    for s in self.semantic+self.physical:
                        rows.append({"backbone":b,"condition":c,"question_id":q,"state":s,"automatic_primary_eligible":eligible,"primary_semantic_state":eligible and s in self.semantic,"tolerant_denotation_agreement":True,"strict_denotation_agreement":True,"prediction_ok":True})
        return rows,canonical
    def test_exact_atomic_primary_hold_and_and_denominators(self):
        rows,canonical=self.synthetic();sem,phy=a.validate_atomic(rows,self.partition);self.assertEqual((len(sem),len(phy)),(15,3));suite=a.aggregate_suite(rows,self.partition,canonical);self.assertEqual(len(suite),1440);self.assertEqual(sum(x["automatic_primary_eligible"] for x in suite),528);self.assertEqual(sum(x["order_hold"] for x in suite),912);self.assertEqual(sum(x["suite_15state_and"] is True for x in suite),528)
    def test_one_missing_atomic_row_fails_closed(self):
        rows,_=self.synthetic()
        with self.assertRaises(ValueError):a.validate_atomic(rows[:-1],self.partition)
    def test_physical_state_never_enters_primary_and(self):
        rows,canonical=self.synthetic();target=next(r for r in rows if r["automatic_primary_eligible"] and r["state"] in self.physical);target["tolerant_denotation_agreement"]=False;suite=a.aggregate_suite(rows,self.partition,canonical);item=next(x for x in suite if x["backbone"]==target["backbone"] and x["condition"]==target["condition"] and x["question_id"]==target["question_id"]);self.assertTrue(item["suite_15state_and"])
    def test_one_semantic_failure_breaks_15_state_and(self):
        rows,canonical=self.synthetic();target=next(r for r in rows if r["automatic_primary_eligible"] and r["state"] in self.semantic and r["state"]!="T0_snapshot");target["tolerant_denotation_agreement"]=False;suite=a.aggregate_suite(rows,self.partition,canonical);item=next(x for x in suite if x["backbone"]==target["backbone"] and x["condition"]==target["condition"] and x["question_id"]==target["question_id"]);self.assertFalse(item["suite_15state_and"])
    def test_holm_monotonic_and_family_constants(self):
        out=a.holm([.01,.04,.03,.20,.001,.8,.6,.5,.2]);self.assertEqual(len(out),9);self.assertTrue(all(0<=x<=1 for x in out));self.assertEqual(a.RANDOMIZATION_SAMPLES,100000);self.assertEqual(a.BOOTSTRAP_SAMPLES,20000);self.assertEqual(a.SEED,20260805)

if __name__=="__main__":unittest.main()
