#!/usr/bin/env python3
import argparse,hashlib,json
from datetime import datetime,timezone
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument("--run-dir",type=Path,required=True);p.add_argument("--analysis-dir",type=Path,required=True);p.add_argument("--freeze",type=Path,required=True);p.add_argument("--out",type=Path,required=True);a=p.parse_args();files=[a.run_dir/"atomic_scores.jsonl",a.run_dir/"RUN_SUMMARY.json",a.analysis_dir/"suite_outcomes.jsonl",a.analysis_dir/"suite_outcomes.csv",a.analysis_dir/"clustered_contrasts.csv",a.analysis_dir/"clustered_contrasts.tex",a.analysis_dir/"semantic_suite_effects.svg",a.analysis_dir/"ANALYSIS_SUMMARY.json",a.freeze];arts=[{"path":str(x.resolve()),"sha256":sha(x),"bytes":x.stat().st_size} for x in files];summary=json.loads((a.analysis_dir/"ANALYSIS_SUMMARY.json").read_text());m={"schema_version":"ma-sqlgrid-semantic-release-v3","created_at_utc":datetime.now(timezone.utc).isoformat().replace('+00:00','Z'),"freeze_content_sha256":summary["freeze_content_sha256"],"invariants":{"atomic_rows":25920,"primary_semantic_state_rows":7920,"order_hold_diagnostic_rows":16416,"suite_rows":1440,"primary_predictions":528,"order_hold_predictions":912,"semantic_states":15,"physical_diagnostic_states":3,"contrast_holm_family":9},"lineage":summary["lineage"],"artifacts":arts};a.out.write_text(json.dumps(m,indent=2,sort_keys=True)+"\n",encoding="utf-8");print("RELEASE_MANIFEST_V3",len(arts))
if __name__=="__main__":main()
