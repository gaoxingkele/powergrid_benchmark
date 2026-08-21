"""Independent structural and numerical validator for exploratory-v3."""
import csv, hashlib, json
from collections import defaultdict
from pathlib import Path
import numpy as np

HERE=Path(__file__).resolve().parent; REPO=HERE.parents[3]
W4=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"
W3=REPO/"paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500"
SEEDS=[2026,2027,2028,2029,2030]; ROLES=["label_blind","predicted","oracle"]

def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def main():
 checks=[]
 def check(name,ok,evidence): checks.append({"name":name,"passed":bool(ok),"evidence":evidence})
 protocol=sha(HERE/"PROTOCOL_FREEZE.md")
 inv=json.loads((HERE/"inventory.json").read_text())
 check("protocol hash propagates to inventory",inv["protocol_sha256"]==protocol,inv["protocol_sha256"])
 check("15 complete source ledgers",len(inv["runs"])==15 and all(r["complete"] for r in inv["runs"]),len(inv["runs"]))
 check("810000 frozen rows",sum(r["rows"] for r in inv["runs"])==810000,sum(r["rows"] for r in inv["runs"]))
 with (HERE/"cell_summary.csv").open(encoding="utf-8") as f: cells=list(csv.DictReader(f))
 check("108 unique finite-grid cells",len(cells)==108 and len({(r["role"],r["mode"],r["k"]) for r in cells})==108,len(cells))
 check("all cells bind protocol",all(r["protocol_sha256"]==protocol for r in cells),protocol)
 # Independent raw-ledger recomputation of all F1 means.
 sums=defaultdict(float); ns=defaultdict(int); dsums=defaultdict(lambda:np.zeros(3)); dns=defaultdict(int)
 for seed in SEEDS:
  for role in ROLES:
   p=(W3 if seed==2026 else W4/f"seed_{seed}")/role/"predictions.jsonl"
   with p.open(encoding="utf-8") as f:
    for line in f:
     r=json.loads(line); key=(role,r["mode"],str(r["k"])); sums[key]+=float(r["f1"]); ns[key]+=1
     dk=(role,r["mode"],str(r["k"]),r["underlying_document_id"]); dsums[dk]+=np.asarray([r["precision"],r["recall"],r["f1"]]); dns[dk]+=1
 diffs=[]
 for r in cells:
  key=(r["role"],r["mode"],r["k"]); diffs.append(abs(float(r["mean_f1"])-sums[key]/ns[key]))
 check("independent all-cell F1 recomputation",max(diffs)<1e-12,max(diffs))
 # Independently reproduce every claim-weighted document-bootstrap cell interval.
 rng=np.random.default_rng(20260805); ci_diffs=[]
 for role in ["label_blind","predicted","oracle"]:
  for mode in ["bm25","full","lead_k","lexcue","no_graph","no_role","query_only","sbert","tfidf"]:
   for k in [1,3,5,10]:
    row=next(r for r in cells if (r["role"],r["mode"],r["k"])==(role,mode,str(k)))
    docs=sorted(d for rr,mm,kk,d in dsums if (rr,mm,kk)==(role,mode,str(k)))
    w=np.asarray([dns[(role,mode,str(k),d)] for d in docs],float)
    vals=np.asarray([dsums[(role,mode,str(k),d)]/dns[(role,mode,str(k),d)] for d in docs])
    for j,m in enumerate(["precision","recall","f1"]):
     take=rng.integers(0,len(docs),size=(2000,len(docs)))
     sim=(vals[take,j]*w[take]).sum(axis=1)/w[take].sum(axis=1); lo,hi=np.quantile(sim,[.025,.975])
     ci_diffs.extend([abs(lo-float(row[f"doc_ci_low_{m}"])),abs(hi-float(row[f"doc_ci_high_{m}"]))])
 check("independent claim-weighted interval recomputation",max(ci_diffs)<1e-12,max(ci_diffs))
 with (HERE/"contrasts_all.csv").open(encoding="utf-8") as f: cons=list(csv.DictReader(f))
 fam={x:sum(r["family"]==x for r in cons) for x in ["F1","F2","F3"]}
 check("frozen multiplicity-family sizes",fam=={"F1":24,"F2":81,"F3":54},fam)
 check("exact five-seed p grid",all(abs(float(r["exact_seed_signflip_p"])*32-round(float(r["exact_seed_signflip_p"])*32))<1e-12 for r in cons),"multiples of 1/32")
 check("Holm dominates raw p",all(float(r["holm_p"])+1e-15>=float(r["exact_seed_signflip_p"]) for r in cons),"all contrasts")
 figs=[HERE/f"fig_budget_{r}.pdf" for r in ROLES]+[HERE/"fig_primary_forest.pdf"]
 check("four publication figures",all(p.is_file() and p.stat().st_size>1000 for p in figs),[p.name for p in figs])
 man=json.loads((HERE/"artifact_manifest.json").read_text())
 bad=[n for n,v in man["artifacts"].items() if n!="validation.json" and (not (HERE/n).is_file() or sha(HERE/n)!=v["sha256"])]
 check("artifact manifest hashes",not bad,bad)
 check("missing modern/no-floor modes explicit",man["missing_by_design"]==["new cross-encoder","no-floor ablation"],man["missing_by_design"])
 out={"protocol_sha256":protocol,"passed":all(c["passed"] for c in checks),"checks":checks}
 (HERE/"validation.json").write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 if not out["passed"]: raise SystemExit(1)

if __name__=="__main__": main()
