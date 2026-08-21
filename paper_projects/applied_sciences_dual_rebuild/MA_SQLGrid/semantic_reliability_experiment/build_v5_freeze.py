#!/usr/bin/env python3
import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def rec(p):p=Path(p);return {"path":p.relative_to(ROOT).as_posix(),"sha256":sha(p),"bytes":p.stat().st_size}
def main():
 v4p=HERE/"PROTOCOL_FREEZE_V4_DRAFT.json";v4=json.loads(v4p.read_text());f={k:v for k,v in v4.items() if k not in {"freeze_content_sha256","frozen_at_utc","frozen_files","schema_version","status"}};f.update({"schema_version":"ma-sqlgrid-semantic-reliability-freeze-v5","status":"READY_AWAITING_V5_REAUDIT","frozen_at_utc":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),"v4_parent_freeze":rec(v4p),"v4_parent_content_sha256":v4["freeze_content_sha256"],"v4_t0_incident":rec(HERE/"V4_T0_PREFLIGHT_INCIDENT.json"),"sql_safety_v5":{"scalar_replace_function_allowed":True,"replace_into_rejected":True,"with_prefix_replace_into_rejected":True},"canonical_snapshot_preflight_contract":{"required_for_reaudit":True,"state":"T0_snapshot","gold_queries":180,"prediction_queries":1440,"sql_executions":1620,"canonical_mismatches_required":0,"output_written":False,"other_states_opened":0,"report_schema":"ma-sqlgrid-canonical-snapshot-preflight-v5"}})
 paths={x["path"] for x in v4["frozen_files"]};extra=["PROTOCOL_V5.md","V5_PRE_SCORE_REPORT.md","V4_T0_PREFLIGHT_INCIDENT.json","run_stage_b_preflight_v5.py","tests/test_v5_safety_preflight.py","build_v5_freeze.py","verify_v5_freeze.py"]
 paths.update(f"paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/semantic_reliability_experiment/{x}" for x in extra);f["frozen_files"]=[rec(ROOT/p) for p in sorted(paths)];f["freeze_content_sha256"]=canon(f);(HERE/"PROTOCOL_FREEZE_V5_DRAFT.json").write_text(json.dumps(f,indent=2,sort_keys=True)+"\n",encoding="utf-8");print("READY_AWAITING_V5_REAUDIT",f["freeze_content_sha256"])
if __name__=="__main__":main()
