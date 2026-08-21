import hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class V4FreezeContractTests(unittest.TestCase):
 def test_v4_keys_and_exact_partition(self):
  p=ROOT/"PROTOCOL_FREEZE_V4_DRAFT.json"
  if not p.exists():self.skipTest("v4 freeze not built")
  f=json.loads(p.read_text());
  for key in ["freeze_content_sha256","canonical_v2_binding","order_adjudication","prediction_bindings","stage_a","pre_score"]:self.assertIn(key,f)
  self.assertIn("order_checklist_jsonl",f["pre_score"]);self.assertEqual(len(f["prediction_bindings"]),2);self.assertEqual((len(f["stage_a"]["semantic_suite_states"]),len(f["stage_a"]["physical_order_diagnostic_states"])),(15,3))
 def test_valid_synthetic_authorization_preflight_writes_no_output(self):
  p=ROOT/"PROTOCOL_FREEZE_V4_DRAFT.json"
  if not p.exists():self.skipTest("v4 freeze not built")
  f=json.loads(p.read_text());bound=next(x["sha256"] for x in f["frozen_files"] if x["path"].endswith("stage_b_score_v2.py"));current=hashlib.sha256((ROOT/"stage_b_score_v2.py").read_bytes()).hexdigest()
  if current!=bound:self.skipTest("v4 parent is immutable; current runner is versioned v5")
  r=subprocess.run([sys.executable,str(ROOT/"run_stage_b_preflight_v4.py"),"--freeze",str(p)],text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr);self.assertIn("sql_executions=0 output_written=0",r.stdout)
 def test_invalid_gate_fails_closed_without_output(self):
  p=ROOT/"PROTOCOL_FREEZE_V4_DRAFT.json"
  if not p.exists():self.skipTest("v4 freeze not built")
  with tempfile.TemporaryDirectory(prefix="ma_v4_invalid_") as td:
   out=Path(td)/"out";r=subprocess.run([sys.executable,str(ROOT/"stage_b_score_v2.py"),"--freeze",str(p),"--reaudit",str(ROOT/"INDEPENDENT_V2_REAUDIT.json"),"--approval",str(ROOT/"LAUNCH_APPROVAL_COMPANION.template.json"),"--out",str(out),"--preflight-only"],text=True,capture_output=True);self.assertNotEqual(r.returncode,0);self.assertFalse(out.exists())
if __name__=="__main__":unittest.main()
