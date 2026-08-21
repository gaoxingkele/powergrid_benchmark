#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def main():
 f=json.loads((HERE/"PROTOCOL_FREEZE_V4_DRAFT.json").read_text());expected=f.pop("freeze_content_sha256");assert canon(f)==expected;f["freeze_content_sha256"]=expected;assert f["status"]=="READY_AWAITING_V4_REAUDIT"
 for key in f["stage_b_freeze_key_contract"]["top_level"]:assert key in f
 for key in f["stage_b_freeze_key_contract"]["canonical_v2_binding"]:assert key in f["canonical_v2_binding"]
 for key in f["stage_b_freeze_key_contract"]["stage_a"]:assert key in f["stage_a"]
 for key in f["stage_b_freeze_key_contract"]["pre_score"]:assert key in f["pre_score"]
 for d in f["prediction_bindings"].values():
  for key in f["stage_b_freeze_key_contract"]["prediction_binding_each"]:assert key in d
 for x in f["frozen_files"]:p=ROOT/x["path"];assert sha(p)==x["sha256"] and p.stat().st_size==x["bytes"]
 assert f["stage_a"]["states_total"]==18 and len(f["stage_a"]["semantic_suite_states"])==15 and len(f["stage_a"]["physical_order_diagnostic_states"])==3
 assert not (HERE/"formal_v4_results").exists();print("V4_FREEZE_VERIFY PASS",expected)
if __name__=="__main__":main()
