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
def resolve(x):
 p=Path(x);return HERE/p if (HERE/p).exists() else ROOT/p
def main():
 p=HERE/"PROTOCOL_FREEZE_V2_DRAFT.json";f=json.loads(p.read_text(encoding="utf-8"));expected=f.pop("freeze_content_sha256");assert canon(f)==expected;f["freeze_content_sha256"]=expected
 assert f["status"]=="READY_AWAITING_REAUDIT" and f["pre_score"]["automatic_primary_order_insensitive_n"]==66 and f["pre_score"]["order_hold_n"]==114
 for x in f["frozen_files"]:q=resolve(x["path"]);assert sha(q)==x["sha256"] and q.stat().st_size==x["bytes"]
 sm=json.loads((HERE/"states_v2b/STAGE_A_STATE_MANIFEST.json").read_text());rm=json.loads((HERE/"states_v2b_rerun/STAGE_A_STATE_MANIFEST.json").read_text());a={x["state"]:(x["state_sha256"],x["trace_sha256"]) for x in sm["states"]};b={x["state"]:(x["state_sha256"],x["trace_sha256"]) for x in rm["states"]};assert a==b and len(a)==18
 for x in sm["states"]:assert sha(HERE/"states_v2b"/x["state_path"])==x["state_sha256"] and sha(HERE/"traces_v2b"/x["trace_path"])==x["trace_sha256"]
 c=json.loads((HERE/"pre_score_v2b/PRE_SCORE_GOLD_COVERAGE.json").read_text());assert c["coverage"]["changed_union_n"]==180 and c["coverage"]["all_empty_nonempty_in_at_least_two_states"]
 assert not (HERE/"INDEPENDENT_REAUDIT_V2.json").exists();assert not (HERE/"formal_v2_results").exists()
 print("V2_FREEZE_VERIFY PASS",expected)
if __name__=="__main__":main()
