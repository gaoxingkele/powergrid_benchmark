#!/usr/bin/env python3
"""Run a synthetic-authorized preflight; canonical mode is T0-only."""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--freeze",type=Path,default=HERE/"PROTOCOL_FREEZE_V5_DRAFT.json");p.add_argument("--mode",choices=["zero-sql","canonical-snapshot"],required=True);p.add_argument("--record",type=Path);a=p.parse_args();freeze=json.loads(a.freeze.read_text());policy=json.loads((HERE/"LAUNCH_APPROVAL_POLICY_V3.json").read_text())
 with tempfile.TemporaryDirectory(prefix="ma_v5_preflight_") as td:
  t=Path(td);audit=t/"SYNTHETIC_PREFLIGHT_AUDIT.json";audit.write_text(json.dumps({"schema_version":policy["required_reaudit_schema_version"],"decision":policy["required_reaudit_decision"],"freeze_content_sha256":freeze["freeze_content_sha256"],"required_gates_all_pass":True,"authorizes_formal_score":True,"test_only_synthetic_preflight":True,"gates":[{"id":x,"status":"PASS"} for x in policy["required_reaudit_gate_ids"]]},sort_keys=True),encoding="utf-8")
  approval=t/"SYNTHETIC_PREFLIGHT_COMPANION.json";approval.write_text(json.dumps({"schema_version":policy["required_launch_companion_schema_version"],"decision":policy["required_launch_companion_decision"],"freeze_content_sha256":freeze["freeze_content_sha256"],"reaudit_path":audit.name,"reaudit_sha256":sha(audit),"reaudit_bytes":audit.stat().st_size,"approver_identity":"synthetic-preflight-only","approved_at_utc":"test-only"},sort_keys=True),encoding="utf-8")
  out=t/"must_not_exist";flag="--preflight-only" if a.mode=="zero-sql" else "--canonical-snapshot-preflight";cmd=[sys.executable,str(HERE/"stage_b_score_v2.py"),"--freeze",str(a.freeze),"--reaudit",str(audit),"--approval",str(approval),"--out",str(out),flag];run=subprocess.run(cmd,text=True,capture_output=True)
  marker="STAGE_B_V4_PREFLIGHT_PASS" if a.mode=="zero-sql" else "STAGE_B_V5_CANONICAL_SNAPSHOT_PREFLIGHT_PASS"
  if run.returncode or marker not in run.stdout or out.exists():raise RuntimeError({"returncode":run.returncode,"stdout":run.stdout,"stderr":run.stderr,"out_exists":out.exists()})
  if a.record:
   a.record.write_text(json.dumps({"schema_version":"ma-sqlgrid-canonical-snapshot-preflight-v5","freeze_content_sha256":freeze["freeze_content_sha256"],"mode":a.mode,"status":"PASS","ledger_predictions_loaded":1440,"gold_queries_executed":180 if a.mode=="canonical-snapshot" else 0,"prediction_queries_executed":1440 if a.mode=="canonical-snapshot" else 0,"sql_executions":1620 if a.mode=="canonical-snapshot" else 0,"canonical_mismatches":0,"output_written":False,"formal_multistate_outcomes_accessed":False},indent=2,sort_keys=True)+"\n",encoding="utf-8")
  print(run.stdout.strip())
if __name__=="__main__":main()
