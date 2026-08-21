import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location("stageb",ROOT/"stage_b_score_v2.py");stageb=importlib.util.module_from_spec(spec);spec.loader.exec_module(stageb)
class V5SafetyTests(unittest.TestCase):
 def test_scalar_replace_is_allowed(self):
  self.assertTrue(stageb.clean_sql("SELECT REPLACE('TX-001','-','')")[0]);self.assertTrue(stageb.clean_sql("SELECT DISTINCT REPLACE(asset_name, '-', '') FROM assets")[0])
 def test_replace_into_is_rejected_including_with_prefix(self):
  self.assertFalse(stageb.clean_sql("REPLACE INTO assets(asset_id) VALUES (1)")[0]);self.assertFalse(stageb.clean_sql("WITH x AS (SELECT 1) REPLACE INTO assets(asset_id) SELECT * FROM x")[0])
 def test_v5_freeze_contract_and_t0_preflight(self):
  freeze=ROOT/"PROTOCOL_FREEZE_V5_DRAFT.json"
  if not freeze.exists():self.skipTest("v5 freeze not built")
  f=json.loads(freeze.read_text());self.assertTrue(f["canonical_snapshot_preflight_contract"]["required_for_reaudit"]);self.assertEqual(f["canonical_snapshot_preflight_contract"]["sql_executions"],1620)
  with tempfile.TemporaryDirectory(prefix="v5_test_") as td:
   rec=Path(td)/"report.json";r=subprocess.run([sys.executable,str(ROOT/"run_stage_b_preflight_v5.py"),"--freeze",str(freeze),"--mode","canonical-snapshot","--record",str(rec)],text=True,capture_output=True);self.assertEqual(r.returncode,0,r.stderr);d=json.loads(rec.read_text());self.assertEqual((d["sql_executions"],d["canonical_mismatches"],d["output_written"]),(1620,0,False))
if __name__=="__main__":unittest.main()
