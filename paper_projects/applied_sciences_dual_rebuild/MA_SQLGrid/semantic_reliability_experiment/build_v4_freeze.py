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
 v3p=HERE/"PROTOCOL_FREEZE_V3_DRAFT.json";v2p=HERE/"PROTOCOL_FREEZE_V2_DRAFT.json";v3=json.loads(v3p.read_text());v2=json.loads(v2p.read_text());f={k:v for k,v in v3.items() if k not in {"freeze_content_sha256","frozen_at_utc","frozen_files","schema_version","status"}}
 f.update({"schema_version":"ma-sqlgrid-semantic-reliability-freeze-v4","status":"READY_AWAITING_V4_REAUDIT","frozen_at_utc":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),"prediction_bindings":v2["prediction_bindings"],"pre_score":v2["pre_score"],"v3_parent_freeze":rec(v3p),"v3_parent_content_sha256":v3["freeze_content_sha256"],"v3_preflight_incident":rec(HERE/"V3_PREFLIGHT_INCIDENT.json"),"stage_b_freeze_key_contract":{"top_level":["freeze_content_sha256","canonical_v2_binding","order_adjudication","prediction_bindings","stage_a","pre_score"],"canonical_v2_binding":["freeze_and_method","canonical_rows_v2"],"stage_a":["state_directory","manifest_content_sha256","semantic_suite_states","physical_order_diagnostic_states"],"pre_score":["order_checklist_jsonl"],"prediction_binding_each":["predictions","manifest"],"tested":True},"preflight_contract":{"authorization_to_order_load":True,"canonical_live_identity":True,"ledger_rows":1440,"states":18,"order_rows":114,"sql_executions":0,"output_written":False}})
 paths={x["path"] for x in v3["frozen_files"]};extra=["PROTOCOL_V4.md","V4_PRE_SCORE_REPORT.md","V3_PREFLIGHT_INCIDENT.json","run_stage_b_preflight_v4.py","build_v4_freeze.py","verify_v4_freeze.py","tests/test_v4_freeze_contract.py"]
 paths.update(f"paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/semantic_reliability_experiment/{x}" for x in extra);f["frozen_files"]=[rec(ROOT/p) for p in sorted(paths)]
 f["freeze_content_sha256"]=canon(f);(HERE/"PROTOCOL_FREEZE_V4_DRAFT.json").write_text(json.dumps(f,indent=2,sort_keys=True)+"\n",encoding="utf-8");print("READY_AWAITING_V4_REAUDIT",f["freeze_content_sha256"])
if __name__=="__main__":main()
