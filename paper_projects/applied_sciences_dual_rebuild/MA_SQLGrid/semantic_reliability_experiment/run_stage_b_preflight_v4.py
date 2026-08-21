#!/usr/bin/env python3
"""Test-only synthetic authorization preflight; never executes candidate SQL."""
import argparse,hashlib,json,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--freeze",type=Path,default=HERE/"PROTOCOL_FREEZE_V4_DRAFT.json");a=p.parse_args();freeze=json.loads(a.freeze.read_text());policy=json.loads((HERE/"LAUNCH_APPROVAL_POLICY_V3.json").read_text());
 with tempfile.TemporaryDirectory(prefix="ma_v4_preflight_") as td:
  t=Path(td);audit=t/"SYNTHETIC_PREFLIGHT_AUDIT.json";gates=[{"id":x,"status":"PASS"} for x in policy["required_reaudit_gate_ids"]];audit.write_text(json.dumps({"schema_version":policy["required_reaudit_schema_version"],"decision":policy["required_reaudit_decision"],"freeze_content_sha256":freeze["freeze_content_sha256"],"required_gates_all_pass":True,"authorizes_formal_score":True,"test_only_synthetic_preflight":True,"gates":gates},sort_keys=True),encoding="utf-8")
  approval=t/"SYNTHETIC_PREFLIGHT_COMPANION.json";approval.write_text(json.dumps({"schema_version":policy["required_launch_companion_schema_version"],"decision":policy["required_launch_companion_decision"],"freeze_content_sha256":freeze["freeze_content_sha256"],"reaudit_path":audit.name,"reaudit_sha256":sha(audit),"reaudit_bytes":audit.stat().st_size,"approver_identity":"synthetic-preflight-only","approved_at_utc":"test-only"},sort_keys=True),encoding="utf-8")
  out=t/"must_not_exist";cmd=[sys.executable,str(HERE/"stage_b_score_v2.py"),"--freeze",str(a.freeze),"--reaudit",str(audit),"--approval",str(approval),"--out",str(out),"--preflight-only"];run=subprocess.run(cmd,text=True,capture_output=True)
  if run.returncode or "STAGE_B_V4_PREFLIGHT_PASS" not in run.stdout or out.exists():raise RuntimeError({"returncode":run.returncode,"stdout":run.stdout,"stderr":run.stderr,"out_exists":out.exists()})
  print(run.stdout.strip())
if __name__=="__main__":main()
