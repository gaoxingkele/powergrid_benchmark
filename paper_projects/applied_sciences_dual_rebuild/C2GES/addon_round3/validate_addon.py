"""Independent recomputation validator for the prospective Round-3 add-on."""
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]
W4=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"; W3=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500"; RUNS=HERE/"runs"
SEEDS=[2026,2027,2028,2029,2030]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def source(s): return (W3 if s==2026 else W4/f"seed_{s}")/"label_blind/predictions.jsonl"

def main():
 checks=[]
 def check(n,ok,e): checks.append({"name":n,"passed":bool(ok),"evidence":e})
 protocol=sha(HERE/"ADDON_PROTOCOL_FREEZE.md"); result=json.loads((HERE/"results.json").read_text()); check("protocol binding",result["protocol_sha256"]==protocol,protocol)
 v=defaultdict(dict); docs={}
 for seed in SEEDS:
  with source(seed).open(encoding="utf-8") as f:
   for line in f:
    r=json.loads(line); arm={"full":"full","no_graph":"no_local","bm25":"bm25","query_only":"query_only","sbert":"dense"}.get(r["mode"])
    if arm and (arm in {"full","no_local"} or seed==2026): v[(arm,int(r["k"]))][(r["qid"],seed if arm in {"full","no_local"} else 0)]=r["f1"]; docs[r["qid"]]=r["underlying_document_id"]
 for arm in ["true_no_floor","true_no_role"]:
  for seed in SEEDS:
   with (RUNS/arm/f"seed_{seed}/predictions.jsonl").open(encoding="utf-8") as f:
    for line in f:
     r=json.loads(line)
     if r["mode"]=="full": v[(arm,int(r["k"]))][(r["qid"],seed)]=r["f1"]; docs[r["qid"]]=r["underlying_document_id"]
 with (RUNS/"cross_encoder_prospective/predictions.jsonl").open(encoding="utf-8") as f:
  for line in f:
   r=json.loads(line); v[("cross_encoder",int(r["k"]))][(r["qid"],0)]=r["f1"]; docs[r["qid"]]=r["underlying_document_id"]
 def claims(arm,k):
  d=v[(arm,k)]; return {q:float(np.mean([x for (qq,s),x in d.items() if qq==q])) for q in sorted({q for q,s in d})}
 dif=[]
 for row in result["cells"]: dif.append(abs(row["mean_f1"]-np.mean(list(claims(row["arm"],row["k"]).values()))))
 check("independent 32-cell point recomputation",max(dif)<1e-12,max(dif))
 cd=[]
 for ix,row in enumerate(result["contrasts"]):
  arm=row["contrast"][:-5]; a,b=claims(arm,3),claims("full",3); by=defaultdict(list)
  for q in sorted(set(a)&set(b)): by[docs[q]].append(a[q]-b[q])
  names=sorted(by); ds=np.asarray([sum(by[d]) for d in names]); dn=np.asarray([len(by[d]) for d in names]); point=ds.sum()/dn.sum()
  take=np.random.default_rng(20260805+ix).integers(0,len(names),size=(10000,len(names))); sim=ds[take].sum(1)/dn[take].sum(1); lo,hi=np.quantile(sim,[.025,.975]); cd += [abs(point-row["mean_difference"]),abs(lo-row["doc_ci_low"]),abs(hi-row["doc_ci_high"])]
 check("independent claim-weighted contrast intervals",max(cd)<1e-12,max(cd))
 inv=json.loads((HERE/"inventory.json").read_text()); check("16 complete indexed sources",inv["complete"] and len(inv["sources"])==16,len(inv["sources"]))
 check("ten trained run success records",all(json.loads((RUNS/a/f"seed_{s}/resource_usage.json").read_text())["status"]=="success" for a in ["true_no_floor","true_no_role"] for s in SEEDS),10)
 check("cross-encoder success",json.loads((RUNS/"cross_encoder_prospective/resource_usage.json").read_text())["status"]=="success","success")
 check("seven-arm Holm family",len(result["contrasts"])==7 and all(r["holm_p"]+1e-15>=r["cluster_signflip_p"] for r in result["contrasts"]),7)
 man=json.loads((HERE/"artifact_manifest.json").read_text()); bad=[n for n,x in man["artifacts"].items() if not (HERE/n).is_file() or sha(HERE/n)!=x["sha256"]]; check("artifact hashes",not bad,bad)
 out={"protocol_sha256":protocol,"passed":all(x["passed"] for x in checks),"checks":checks}; (HERE/"validation.json").write_text(json.dumps(out,indent=2)+"\n")
 if not out["passed"]: raise SystemExit(1)
if __name__=="__main__": main()
