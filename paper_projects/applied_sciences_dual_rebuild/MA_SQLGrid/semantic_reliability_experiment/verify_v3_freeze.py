#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def main():
 p=HERE/"PROTOCOL_FREEZE_V3_DRAFT.json";f=json.loads(p.read_text());expected=f.pop("freeze_content_sha256");assert canon(f)==expected;f["freeze_content_sha256"]=expected;assert f["status"]=="READY_AWAITING_V3_REAUDIT"
 assert f["stage_a"]["states_total"]==18 and f["stage_a"]["semantic_state_n"]==15 and f["stage_a"]["physical_state_n"]==3
 assert f["denominators"]=={"atomic_rows":25920,"primary_semantic_state_rows":7920,"order_hold_diagnostic_rows":16416,"prediction_rows":1440,"primary_predictions":528,"order_hold_predictions":912,"questions":180,"automatic_primary_questions":66,"order_hold_questions":114}
 for x in f["frozen_files"]:q=ROOT/x["path"];assert sha(q)==x["sha256"] and q.stat().st_size==x["bytes"]
 chain={k:ROOT/v["path"] for k,v in f["order_adjudication"]["artifacts"].items()}
 for k,q in chain.items():x=f["order_adjudication"]["artifacts"][k];assert sha(q)==x["sha256"] and q.stat().st_size==x["bytes"]
 ad=json.loads(chain["adjudication"].read_text());assert ad["inputs"]["reviewer_a_json_sha256"]==sha(chain["reviewer_a"]) and ad["inputs"]["reviewer_b_json_sha256"]==sha(chain["reviewer_b"]);assert ad["agreement"]["held_ids"]==114
 for k in ["freeze_and_method","canonical_rows_v2"]:x=f["canonical_v2_binding"][k];q=ROOT/x["path"];assert sha(q)==x["sha256"] and q.stat().st_size==x["bytes"]
 assert not (HERE/"formal_v3_results").exists() and not (HERE/"INDEPENDENT_V3_REAUDIT.json").exists() and not (HERE/"LAUNCH_APPROVAL_COMPANION.json").exists()
 print("V3_FREEZE_VERIFY PASS",expected)
if __name__=="__main__":main()
