"""Aggregate the frozen Round-3 add-on family after all prospective runs finish."""
from __future__ import annotations
import csv, hashlib, itertools, json
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]
W4=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"; W3=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500"
RUNS=HERE/"runs"; SEEDS=[2026,2027,2028,2029,2030]; KS=[1,3,5,10]
ARMS=["full","bm25","query_only","dense","no_local","true_no_floor","true_no_role","cross_encoder"]
DISPLAY={"full":"Full","bm25":"BM25","query_only":"Query-only","dense":"Dense/SBERT","no_local":"No-local","true_no_floor":"True no-floor","true_no_role":"True no-role","cross_encoder":"Cross-encoder"}

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def source(seed): return (W3 if seed==2026 else W4/f"seed_{seed}")/"label_blind/predictions.jsonl"
def holm(ps):
 order=sorted(range(len(ps)),key=lambda i:ps[i]); out=[0.]*len(ps); run=0.
 for rank,i in enumerate(order): run=max(run,min(1.,(len(ps)-rank)*ps[i])); out[i]=run
 return out
def exact(values):
 x=np.asarray(values); obs=abs(x.mean()); return float(np.mean([abs(np.mean(x*np.asarray(s)))>=obs-1e-15 for s in itertools.product((-1.,1.),repeat=len(x))]))
def write_csv(p,rows):
 with p.open("w",newline="",encoding="utf-8") as f: w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def main():
 protocol=sha(HERE/"ADDON_PROTOCOL_FREEZE.md"); inventory=[]; values=defaultdict(dict); docs={}
    # Existing arms: seeded full/no-local, deterministic baselines read once.
 for seed in SEEDS:
  p=source(seed); inventory.append({"kind":"existing","seed":seed,"path":str(p.relative_to(REPO)),"sha256":sha(p),"rows":sum(1 for _ in p.open("rb"))})
  with p.open(encoding="utf-8") as f:
   for line in f:
    r=json.loads(line); mode=r["mode"]
    arm={"full":"full","no_graph":"no_local","bm25":"bm25","query_only":"query_only","sbert":"dense"}.get(mode)
    if arm and (arm in {"full","no_local"} or seed==2026): values[(arm,int(r["k"]))][(r["qid"],seed if arm in {"full","no_local"} else 0)]=float(r["f1"]); docs[r["qid"]]=r["underlying_document_id"]
 for arch in ["true_no_floor","true_no_role"]:
  for seed in SEEDS:
   p=RUNS/arch/f"seed_{seed}/predictions.jsonl"; ru=p.parent/"resource_usage.json"
   if not p.is_file() or json.loads(ru.read_text())["status"]!="success": raise RuntimeError(f"incomplete frozen run {arch}:{seed}")
   inventory.append({"kind":"prospective","seed":seed,"arm":arch,"path":str(p.relative_to(REPO)),"sha256":sha(p),"rows":sum(1 for _ in p.open("rb"))})
   with p.open(encoding="utf-8") as f:
    for line in f:
     r=json.loads(line)
     if r["mode"]=="full": values[(arch,int(r["k"]))][(r["qid"],seed)]=float(r["f1"]); docs[r["qid"]]=r["underlying_document_id"]
 p=RUNS/"cross_encoder_prospective/predictions.jsonl"; ru=p.parent/"resource_usage.json"
 if not p.is_file() or json.loads(ru.read_text())["status"]!="success": raise RuntimeError("incomplete cross-encoder run")
 inventory.append({"kind":"prospective","arm":"cross_encoder","path":str(p.relative_to(REPO)),"sha256":sha(p),"rows":sum(1 for _ in p.open("rb"))})
 with p.open(encoding="utf-8") as f:
  for line in f:
   r=json.loads(line); values[("cross_encoder",int(r["k"]))][(r["qid"],0)]=float(r["f1"]); docs[r["qid"]]=r["underlying_document_id"]
 (HERE/"inventory.json").write_text(json.dumps({"protocol_sha256":protocol,"complete":len(inventory)==16,"sources":inventory},indent=2)+"\n")

 def claim_values(arm,k):
  d=values[(arm,k)]; qids=sorted({q for q,_ in d}); return {q:float(np.mean([v for (qq,s),v in d.items() if qq==q])) for q in qids}
 cells=[]
 for arm in ARMS:
  for k in KS:
   cv=claim_values(arm,k); seeded=arm in {"full","no_local","true_no_floor","true_no_role"}
   seedmeans=[]
   if seeded:
    d=values[(arm,k)]; seedmeans=[np.mean([v for (q,s),v in d.items() if s==seed]) for seed in SEEDS]
   cells.append({"protocol_sha256":protocol,"arm":arm,"k":k,"n_claims":len(cv),"mean_f1":np.mean(list(cv.values())),"seed_sd_f1":np.std(seedmeans,ddof=1) if seeded else 0.0})
 write_csv(HERE/"cell_summary.csv",cells)
 contrasts=[]
 for ix,arm in enumerate([a for a in ARMS if a!="full"]):
  a,b=claim_values(arm,3),claim_values("full",3); qids=sorted(set(a)&set(b)); delta={q:a[q]-b[q] for q in qids}; bydoc=defaultdict(list)
  for q in qids: bydoc[docs[q]].append(delta[q])
  dnames=sorted(bydoc); dsum=np.asarray([sum(bydoc[d]) for d in dnames]); dn=np.asarray([len(bydoc[d]) for d in dnames]); obs=float(dsum.sum()/dn.sum())
  rng=np.random.default_rng(20260805+ix); take=rng.integers(0,len(dnames),size=(10000,len(dnames))); boot=dsum[take].sum(1)/dn[take].sum(1); lo,hi=np.quantile(boot,[.025,.975])
  rng=np.random.default_rng(20261805+ix); extreme=0; done=0
  for _ in range(100):
   signs=rng.choice((-1.,1.),size=(1000,len(dnames))); sim=(signs*dsum).sum(1)/dn.sum(); extreme+=int(np.sum(np.abs(sim)>=abs(obs)-1e-15)); done+=1000
  seedp=""
  if arm in {"true_no_floor","true_no_role"}:
   dif=[]
   for seed in SEEDS:
    va=values[(arm,3)]; vb=values[("full",3)]; dif.append(np.mean([v for (q,s),v in va.items() if s==seed])-np.mean([v for (q,s),v in vb.items() if s==seed]))
   seedp=exact(dif)
  contrasts.append({"protocol_sha256":protocol,"contrast":f"{arm}-full","mean_difference":obs,"doc_ci_low":float(lo),"doc_ci_high":float(hi),"cluster_signflip_p":extreme/done,"holm_p":None,"exact_seed_signflip_p":seedp})
 for r,p in zip(contrasts,holm([r["cluster_signflip_p"] for r in contrasts])): r["holm_p"]=p
 write_csv(HERE/"primary_contrasts.csv",contrasts); (HERE/"results.json").write_text(json.dumps({"protocol_sha256":protocol,"cells":cells,"contrasts":contrasts},indent=2)+"\n")
 tex=[f"% protocol SHA-256 {protocol}","\\begin{tabular}{lrrrr}","\\toprule","Arm vs full & $\\Delta$ F1 & 95\\% cluster CI & raw $p$ & Holm $p$ \\\\","\\midrule"]
 for r in contrasts: tex.append(f"{DISPLAY[r['contrast'][:-5]].replace('-','--')} & {r['mean_difference']:+.4f} & [{r['doc_ci_low']:+.4f}, {r['doc_ci_high']:+.4f}] & {r['cluster_signflip_p']:.4f} & {r['holm_p']:.4f} \\\\")
 tex += ["\\bottomrule","\\end{tabular}"]; (HERE/"table_primary.tex").write_text("\n".join(tex)+"\n")
 plt.style.use("seaborn-v0_8-whitegrid"); marks=["o","s","^","D","v","P","X","<"]
 fig,ax=plt.subplots(figsize=(7.4,4.7))
 for i,arm in enumerate(ARMS): ax.plot(KS,[next(r["mean_f1"] for r in cells if r["arm"]==arm and r["k"]==k) for k in KS],marker=marks[i],linestyle=["-","--","-.",":"][i%4],label=DISPLAY[arm])
 ax.set(xlabel="Evidence budget K",ylabel="Macro evidence F1",title="Prospective Round-3 add-on family"); ax.legend(ncol=2,fontsize=8); fig.tight_layout()
 for ext in ["pdf","svg"]: fig.savefig(HERE/f"fig_addon_budget.{ext}")
 fig.savefig(HERE/"fig_addon_budget.png",dpi=450); plt.close(fig)
 fig,ax=plt.subplots(figsize=(7.1,4.4)); y=np.arange(len(contrasts)); x=np.asarray([r["mean_difference"] for r in contrasts]); ax.errorbar(x,y,xerr=[x-np.asarray([r["doc_ci_low"] for r in contrasts]),np.asarray([r["doc_ci_high"] for r in contrasts])-x],fmt="o",capsize=3); ax.axvline(0,color="black",lw=1); ax.set_yticks(y,[DISPLAY[r["contrast"][:-5]] for r in contrasts]); ax.set(xlabel="F1 difference from full",title="Label-blind K=3 prospective add-on contrasts"); fig.tight_layout()
 for ext in ["pdf","svg"]: fig.savefig(HERE/f"fig_addon_forest.{ext}")
 fig.savefig(HERE/"fig_addon_forest.png",dpi=450); plt.close(fig)
 runtime=[]
 for arch in ["true_no_floor","true_no_role"]:
  for seed in SEEDS:
   d=json.loads((RUNS/arch/f"seed_{seed}/resource_usage.json").read_text()); runtime.append({"arm":arch,"seed":seed,"wall_seconds":d["wall_seconds"],"peak_rss_bytes":d["sampled_peak_rss_bytes"],"boundary":"complete learned CPU process"})
 d=json.loads((RUNS/"cross_encoder_prospective/resource_usage.json").read_text()); runtime.append({"arm":"cross_encoder","seed":"","wall_seconds":d["wall_seconds"],"peak_rss_bytes":d["sampled_peak_rss_bytes"],"boundary":"model load + complete test scoring/top-K"}); write_csv(HERE/"runtime.csv",runtime)
 manifest={"protocol_sha256":protocol,"artifacts":{}}
 for p in sorted(HERE.iterdir()):
  if p.is_file() and p.name not in {"artifact_manifest.json","validation.json"}: manifest["artifacts"][p.name]={"sha256":sha(p),"bytes":p.stat().st_size}
 (HERE/"artifact_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")

if __name__=="__main__": main()
