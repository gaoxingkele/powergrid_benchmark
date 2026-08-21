"""Build the finite, hash-bound C2GES exploratory-v3 comparison package."""
from __future__ import annotations

import csv, hashlib, itertools, json, math
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
W4 = REPO / "paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed"
W3 = REPO / "paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500"
SEEDS = [2026, 2027, 2028, 2029, 2030]
ROLES = ["label_blind", "predicted", "oracle"]
MODES = ["bm25", "full", "lead_k", "lexcue", "no_graph", "no_role", "query_only", "sbert", "tfidf"]
KS = [1, 3, 5, 10]
METRICS = ["precision", "recall", "f1"]
ROLE_DIR = {"label_blind": "label_blind", "predicted": "predicted", "oracle": "oracle"}

def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""): h.update(chunk)
    return h.hexdigest()

def source(seed, role):
    base = W3 if seed == 2026 else W4 / f"seed_{seed}"
    return base / ROLE_DIR[role] / "predictions.jsonl"

def holm(ps):
    order = sorted(range(len(ps)), key=lambda i: ps[i]); out = [0.0] * len(ps); running = 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(ps)-rank)*ps[i])); out[i] = running
    return out

def exact_seed_flip(values):
    x = np.asarray(values, float); obs = abs(x.mean()); vals = []
    for signs in itertools.product((-1.0, 1.0), repeat=len(x)): vals.append(abs(np.mean(x*np.asarray(signs))))
    return float(np.mean(np.asarray(vals) >= obs - 1e-15))

def cluster_ci(doc_values, doc_counts, rng, draws=2000):
    """Resample documents, then pool every claim/seed observation in sampled clusters."""
    x = np.asarray(doc_values, float); w = np.asarray(doc_counts, float); n = len(x)
    take = rng.integers(0, n, size=(draws, n))
    sims = (x[take] * w[take]).sum(axis=1) / w[take].sum(axis=1)
    return [float(v) for v in np.quantile(sims, [0.025, 0.975])]

def write_csv(path, rows, fields):
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)

def main():
    protocol_sha = sha(HERE / "PROTOCOL_FREEZE.md")
    inventory = {"protocol_sha256": protocol_sha, "expected_runs": 15, "runs": [], "complete": True}
    paths = []
    # Completeness is resolved from path existence, line counts and hashes before parsing outcomes.
    for seed in SEEDS:
        for role in ROLES:
            p = source(seed, role); exists = p.is_file(); lines = sum(1 for _ in p.open("rb")) if exists else 0
            rec = {"seed": seed, "role": role, "path": str(p.relative_to(REPO)), "exists": exists,
                   "rows": lines, "expected_rows": 54000, "sha256": sha(p) if exists else None}
            rec["complete"] = exists and lines == 54000; inventory["complete"] &= rec["complete"]
            inventory["runs"].append(rec); paths.append((seed, role, p))
    (HERE / "inventory.json").write_text(json.dumps(inventory, indent=2)+"\n", encoding="utf-8")
    if not inventory["complete"]: raise RuntimeError("Frozen inventory is incomplete; outcomes were not aggregated")

    sums = defaultdict(lambda: np.zeros(3)); counts = defaultdict(int)
    dsums = defaultdict(lambda: np.zeros(3)); dcounts = defaultdict(int)
    seen = defaultdict(set)
    for seed, role, p in paths:
        with p.open(encoding="utf-8") as f:
            for line in f:
                r = json.loads(line); mode, k, doc = r["mode"], int(r["k"]), r["underlying_document_id"]
                if mode not in MODES or k not in KS: raise ValueError(f"Unexpected cell {mode}, K={k}")
                v = np.asarray([r[m] for m in METRICS], float)
                ck = (role, seed, mode, k); dk = (role, mode, k, doc)
                sums[ck] += v; counts[ck] += 1; dsums[dk] += v; dcounts[dk] += 1; seen[(seed, role)].add((mode, k))
    if any(len(x) != 36 for x in seen.values()): raise RuntimeError("Not all 36 mode/K cells occur in each run")

    rng = np.random.default_rng(20260805)
    cells = []
    for role in ROLES:
      for mode in MODES:
       for k in KS:
        seed_means = np.asarray([sums[(role,s,mode,k)]/counts[(role,s,mode,k)] for s in SEEDS])
        docs = sorted(d for rr,mm,kk,d in dsums if (rr,mm,kk)==(role,mode,k))
        docmeans = np.asarray([dsums[(role,mode,k,d)]/dcounts[(role,mode,k,d)] for d in docs])
        rec = {"protocol_sha256": protocol_sha, "role": role, "mode": mode, "k": k, "n_seeds": 5, "n_documents": len(docs)}
        for j,m in enumerate(METRICS):
            rec[f"mean_{m}"] = float(seed_means[:,j].mean()); rec[f"seed_sd_{m}"] = float(seed_means[:,j].std(ddof=1))
            doccounts=np.asarray([dcounts[(role,mode,k,d)] for d in docs])
            lo,hi = cluster_ci(docmeans[:,j], doccounts, rng); rec[f"doc_ci_low_{m}"]=lo; rec[f"doc_ci_high_{m}"]=hi
            rec[f"seed_min_{m}"]=float(seed_means[:,j].min()); rec[f"seed_max_{m}"]=float(seed_means[:,j].max())
        cells.append(rec)

    cell_fields = list(cells[0]); write_csv(HERE/"cell_summary.csv", cells, cell_fields)
    (HERE/"cell_summary.json").write_text(json.dumps({"protocol_sha256":protocol_sha,"rows":cells},indent=2)+"\n",encoding="utf-8")

    def cell_seed(role, mode, k, metric):
        j=METRICS.index(metric); return [float((sums[(role,s,mode,k)]/counts[(role,s,mode,k)])[j]) for s in SEEDS]
    def cell_docs(role, mode, k, metric):
        j=METRICS.index(metric); docs=sorted(d for rr,mm,kk,d in dsums if (rr,mm,kk)==(role,mode,k))
        return {d:float((dsums[(role,mode,k,d)]/dcounts[(role,mode,k,d)])[j]) for d in docs}
    specs=[]
    for metric in METRICS:
        for mode in [m for m in MODES if m!="full"]: specs.append(("F1",metric,"label_blind",mode,3,"label_blind","full",3))
        for mode in MODES:
            for k in [1,5,10]: specs.append(("F2",metric,"label_blind",mode,k,"label_blind",mode,3))
        for mode in MODES:
            for role in ["predicted","oracle"]: specs.append(("F3",metric,role,mode,3,"label_blind",mode,3))
    contrasts=[]
    for ix,(fam,metric,ra,ma,ka,rb,mb,kb) in enumerate(specs):
        seed_diff=np.asarray(cell_seed(ra,ma,ka,metric))-np.asarray(cell_seed(rb,mb,kb,metric))
        da,db=cell_docs(ra,ma,ka,metric),cell_docs(rb,mb,kb,metric); docs=sorted(set(da)&set(db)); dd=[da[d]-db[d] for d in docs]
        weights=[dcounts[(ra,ma,ka,d)] for d in docs]
        lo,hi=cluster_ci(dd,weights,np.random.default_rng(20260805+ix))
        contrasts.append({"protocol_sha256":protocol_sha,"family":fam,"metric":metric,"contrast":f"{ra}:{ma}:K{ka} - {rb}:{mb}:K{kb}","mean_difference":float(seed_diff.mean()),"doc_ci_low":lo,"doc_ci_high":hi,"exact_seed_signflip_p":exact_seed_flip(seed_diff),"holm_p":None})
    for fam in ["F1","F2","F3"]:
      for metric in METRICS:
        inds=[i for i,r in enumerate(contrasts) if r["family"]==fam and r["metric"]==metric]; adj=holm([contrasts[i]["exact_seed_signflip_p"] for i in inds])
        for i,p in zip(inds,adj): contrasts[i]["holm_p"]=p
    con_fields=list(contrasts[0]); write_csv(HERE/"contrasts_all.csv",contrasts,con_fields)
    (HERE/"contrasts_all.json").write_text(json.dumps({"protocol_sha256":protocol_sha,"rows":contrasts},indent=2)+"\n",encoding="utf-8")

    primary=[r for r in contrasts if r["family"]=="F1" and r["metric"]=="f1"]
    write_csv(HERE/"primary_editorial_contrasts.csv",primary,con_fields)
    tex=["% Hash-bound exploratory-v3 table; protocol SHA-256: "+protocol_sha,"\\begin{tabular}{lrrrr}","\\toprule","Mode vs full & $\\Delta$ F1 & 95\\% doc. CI & exact seed $p$ & Holm $p$ \\\\","\\midrule"]
    for r in primary:
        label=r["contrast"].split(" - ")[0].split(":")[1].replace("_","\\_")
        tex.append(f"{label} & {r['mean_difference']:+.4f} & [{r['doc_ci_low']:+.4f}, {r['doc_ci_high']:+.4f}] & {r['exact_seed_signflip_p']:.4f} & {r['holm_p']:.4f} \\\\")
    tex += ["\\bottomrule","\\end{tabular}"]
    (HERE/"table_primary_editorial.tex").write_text("\n".join(tex)+"\n",encoding="utf-8")

    # Four finite-family publication figures.
    def cell(role,mode,k): return next(r for r in cells if r["role"]==role and r["mode"]==mode and r["k"]==k)
    plt.style.use("seaborn-v0_8-whitegrid")
    display={"bm25":"BM25","full":"Full","lead_k":"Lead-K","lexcue":"LexCue","no_graph":"No-local","no_role":"No-role","query_only":"Query-only","sbert":"SBERT","tfidf":"TF-IDF"}
    markers=["o","s","^","D","v","P","X","<",">"]; styles=["-","--","-.",":","-","--","-.",":","-"]
    for role in ROLES:
        fig,ax=plt.subplots(figsize=(7.2,4.5))
        for i,mode in enumerate(MODES): ax.plot(KS,[cell(role,mode,k)["mean_f1"] for k in KS],marker=markers[i],linestyle=styles[i],label=display[mode])
        ax.set(xlabel="Evidence budget K",ylabel="Macro evidence F1",title=f"Finite extraction family: {role.replace('_','-')}"); ax.legend(ncol=3,fontsize=7); fig.tight_layout(); fig.savefig(HERE/f"fig_budget_{role}.pdf"); fig.savefig(HERE/f"fig_budget_{role}.png",dpi=450); fig.savefig(HERE/f"fig_budget_{role}.svg"); plt.close(fig)
    fig,ax=plt.subplots(figsize=(7.2,4.8)); y=np.arange(len(primary)); x=[r["mean_difference"] for r in primary]
    forest_modes=[m for m in MODES if m!="full"]
    ax.errorbar(x,y,xerr=[[x[i]-primary[i]["doc_ci_low"] for i in range(len(x))],[primary[i]["doc_ci_high"]-x[i] for i in range(len(x))]],fmt="o",capsize=3); ax.axvline(0,color="black",lw=1); ax.set_yticks(y,[display[m] for m in forest_modes]); ax.set(xlabel="F1 difference from full",title="Label-blind K=3 exploratory contrasts vs full"); fig.tight_layout(); fig.savefig(HERE/"fig_primary_forest.pdf"); fig.savefig(HERE/"fig_primary_forest.png",dpi=450); fig.savefig(HERE/"fig_primary_forest.svg"); plt.close(fig)

    # Runtime is intentionally role/run diagnostic; no mode-level allocation is invented.
    runtime=[]
    for seed,role,_ in paths:
        rp=source(seed,role).parent/"resource_usage.json"; d=json.loads(rp.read_text(encoding="utf-8"))
        runtime.append({"protocol_sha256":protocol_sha,"seed":seed,"role":role,"source":str(rp.relative_to(REPO)),"wall_seconds":d.get("wall_seconds"),"peak_rss_bytes":d.get("peak_rss_bytes"),"boundary":"recorded full selector script; not mode-specific or online latency"})
    write_csv(HERE/"runtime_diagnostic.csv",runtime,list(runtime[0]))
    manifest={"protocol_sha256":protocol_sha,"missing_by_design":["new cross-encoder","no-floor ablation"],"artifacts":{}}
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name not in {"artifact_manifest.json","validation.json"}: manifest["artifacts"][p.name]={"sha256":sha(p),"bytes":p.stat().st_size}
    (HERE/"artifact_manifest.json").write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8")

if __name__ == "__main__": main()
