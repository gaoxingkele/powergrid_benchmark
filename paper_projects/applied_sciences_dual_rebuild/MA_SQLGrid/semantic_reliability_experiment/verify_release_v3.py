#!/usr/bin/env python3
import argparse,csv,hashlib,json
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for c in iter(lambda:f.read(1<<20),b""):h.update(c)
 return h.hexdigest()
def nlines(p):
 with Path(p).open(encoding="utf-8") as f:return sum(1 for x in f if x.strip())
def main():
 p=argparse.ArgumentParser();p.add_argument("--manifest",type=Path,required=True);a=p.parse_args();m=json.loads(a.manifest.read_text());inv=m["invariants"]
 for x in m["artifacts"]:q=Path(x["path"]);assert sha(q)==x["sha256"] and q.stat().st_size==x["bytes"]
 paths={Path(x["path"]).name:Path(x["path"]) for x in m["artifacts"]};assert nlines(paths["atomic_scores.jsonl"])==inv["atomic_rows"]==25920;assert nlines(paths["suite_outcomes.jsonl"])==inv["suite_rows"]==1440
 suite=[json.loads(x) for x in paths["suite_outcomes.jsonl"].read_text().splitlines() if x.strip()];assert sum(r["automatic_primary_eligible"] for r in suite)==528;assert sum(r["order_hold"] for r in suite)==912
 stats=list(csv.DictReader(paths["clustered_contrasts.csv"].open(encoding="utf-8-sig")));assert len(stats)==9 and all(int(r["holm_family_size"])==9 for r in stats)
 ssha=sha(paths["clustered_contrasts.csv"]);assert f"source_sha256={ssha}" in paths["clustered_contrasts.tex"].read_text();assert f"source_sha256={ssha}" in paths["semantic_suite_effects.svg"].read_text();summary=json.loads(paths["ANALYSIS_SUMMARY.json"].read_text());assert summary["atomic_rows"]==25920 and summary["primary_semantic_state_rows"]==7920 and summary["order_hold_diagnostic_rows"]==16416;print("RELEASE_V3_VERIFY PASS")
if __name__=="__main__":main()
