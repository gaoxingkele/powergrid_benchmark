#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def canon(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
def main():
 f=json.loads((HERE/"PROTOCOL_FREEZE_V5_DRAFT.json").read_text());expected=f.pop("freeze_content_sha256");assert canon(f)==expected;f["freeze_content_sha256"]=expected;assert f["status"]=="READY_AWAITING_V5_REAUDIT"
 for x in f["frozen_files"]:p=ROOT/x["path"];assert sha(p)==x["sha256"] and p.stat().st_size==x["bytes"]
 c=f["canonical_snapshot_preflight_contract"];assert (c["gold_queries"],c["prediction_queries"],c["sql_executions"],c["canonical_mismatches_required"],c["output_written"])==(180,1440,1620,0,False)
 report=HERE/"CANONICAL_SNAPSHOT_PREFLIGHT_V5_REPORT.json"
 if report.exists():r=json.loads(report.read_text());assert r["freeze_content_sha256"]==expected and r["status"]=="PASS" and r["sql_executions"]==1620 and r["canonical_mismatches"]==0 and not r["output_written"]
 assert not (HERE/"formal_v5_results").exists();print("V5_FREEZE_VERIFY PASS",expected)
if __name__=="__main__":main()
