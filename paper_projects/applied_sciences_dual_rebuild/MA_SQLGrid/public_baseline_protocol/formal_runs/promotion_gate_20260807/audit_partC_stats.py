"""Promotion-gate audit part C: statistics from ledger scores (+ re-execution override).

Cluster bootstrap (cluster = db_id, 11 clusters, 10000 resamples, seed 20260807).
Writes stats_ex_by_method.csv, stats_pairwise_holm.csv, stats_by_database.csv,
and _stats.json (machine-readable copy for the final report).
"""
import csv
import json
from itertools import combinations
from pathlib import Path

import numpy as np

P = Path(r"D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\public_baseline_protocol")
OUT = P / "formal_runs" / "promotion_gate_20260807"
MODELS = ("qwen", "granite")
METHODS = ("B0_DIRECT", "B1_DECOMP", "B2_SCHEMA_SELECT", "B3_EXEC_REPAIR")
N_BOOT = 10000
SEED = 20260807

# ---- load scores: re-execution values override ledger when they differ ----
reexec = {}
with (OUT / "_reexecution.jsonl").open(encoding="utf-8") as handle:
    for line in handle:
        r = json.loads(line)
        reexec[(r["model"], r["question_id"], r["method"])] = r
n_override = sum(1 for r in reexec.values()
                 if r["reexec_ex"] != r["ledger_ex"] or r["reexec_status"] != r["ledger_status"])

# scores[model][method] = array over 500 question_ids; db per question
rows_meta = {r["question_id"]: r for r in json.loads(
    (P / "official_metadata" / "bird_mini_dev_sqlite.json").read_text(encoding="utf-8"))}
qids = sorted(rows_meta)
dbs = sorted({rows_meta[q]["db_id"] for q in qids})
scores = {m: {meth: np.zeros(len(qids)) for meth in METHODS} for m in MODELS}
qid_idx = {q: i for i, q in enumerate(qids)}
db_of = np.array([dbs.index(rows_meta[q]["db_id"]) for q in qids])
for (model, qid, meth), r in reexec.items():
    scores[model][meth][qid_idx[qid]] = r["reexec_ex"]

rng = np.random.RandomState(SEED)
cluster_ids = np.arange(len(dbs))
questions_per_cluster = np.array([np.sum(db_of == c) for c in cluster_ids])


def boot_samples(stat_fn):
    """Yield bootstrap statistics by resampling clusters with replacement."""
    out = np.empty(N_BOOT)
    for b in range(N_BOOT):
        picked = rng.choice(cluster_ids, size=len(cluster_ids), replace=True)
        weights = np.array([np.sum(picked == c) for c in cluster_ids], dtype=float)
        out[b] = stat_fn(weights)
    return out


def weighted_mean(values, weights):
    # mean over all questions with cluster multiplicity weights
    w = weights[db_of]
    denom = np.sum(questions_per_cluster * weights)
    return float(np.sum(values * w) / denom)


def ci(samples):
    return float(np.percentile(samples, 2.5)), float(np.percentile(samples, 97.5))


def boot_pvalue(samples):
    # two-sided sign test on the bootstrap distribution of the difference
    p_le = float(np.mean(samples <= 0))
    p_ge = float(np.mean(samples >= 0))
    return min(1.0, 2.0 * min(p_le, p_ge))


def holm(pvals):
    """Holm-adjusted p-values, returned in original order."""
    m = len(pvals)
    order = np.argsort(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, idx in enumerate(order):
        running = max(running, (m - rank) * pvals[idx])
        adj[idx] = min(1.0, running)
    return adj


# ---- 1. per model x method EX + CI ----
ex_rows = []
boot_means = {}
for model in MODELS:
    for meth in METHODS:
        vals = scores[model][meth]
        mean = float(np.mean(vals))
        samples = boot_samples(lambda w, v=vals: weighted_mean(v, w))
        lo, hi = ci(samples)
        boot_means[(model, meth)] = (mean, lo, hi)
        ex_rows.append({"model": model, "method": meth, "n": len(vals),
                        "ex_mean": mean, "ci95_low": lo, "ci95_high": hi})

# ---- 2/3. pairwise diffs ----
pair_rows = []
# within-model: all 6 pairs
for model in MODELS:
    pairs = list(combinations(METHODS, 2))
    recs = []
    for a, b in pairs:
        diff_vals = scores[model][a] - scores[model][b]
        point = float(np.mean(diff_vals))
        samples = boot_samples(lambda w, d=diff_vals: weighted_mean(d, w))
        lo, hi = ci(samples)
        recs.append({"scope": f"within_model:{model}", "comparison": f"{a} - {b}",
                     "diff": point, "ci95_low": lo, "ci95_high": hi, "p_raw": boot_pvalue(samples)})
    adj = holm([r["p_raw"] for r in recs])
    for r, p in zip(recs, adj):
        r["p_holm"] = float(p)
        pair_rows.append(r)
# between-models: same method, 4 comparisons, Holm family = 4
recs = []
for meth in METHODS:
    diff_vals = scores["qwen"][meth] - scores["granite"][meth]
    point = float(np.mean(diff_vals))
    samples = boot_samples(lambda w, d=diff_vals: weighted_mean(d, w))
    lo, hi = ci(samples)
    recs.append({"scope": "between_models:qwen-granite", "comparison": meth,
                 "diff": point, "ci95_low": lo, "ci95_high": hi, "p_raw": boot_pvalue(samples)})
adj = holm([r["p_raw"] for r in recs])
for r, p in zip(recs, adj):
    r["p_holm"] = float(p)
    pair_rows.append(r)

# ---- 5. per-db detail ----
db_rows = []
for model in MODELS:
    for db in dbs:
        mask = db_of == dbs.index(db)
        for meth in METHODS:
            vals = scores[model][meth][mask]
            db_rows.append({"model": model, "db_id": db, "method": meth,
                            "n": int(np.sum(mask)), "ex_mean": float(np.mean(vals))})

# ---- write CSVs ----
with (OUT / "stats_ex_by_method.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["model", "method", "n", "ex_mean", "ci95_low", "ci95_high"])
    w.writeheader()
    w.writerows(ex_rows)
with (OUT / "stats_pairwise_holm.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["scope", "comparison", "diff", "ci95_low", "ci95_high", "p_raw", "p_holm"])
    w.writeheader()
    w.writerows(pair_rows)
with (OUT / "stats_by_database.csv").open("w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["model", "db_id", "method", "n", "ex_mean"])
    w.writeheader()
    w.writerows(db_rows)

(OUT / "_stats.json").write_text(json.dumps({
    "seed": SEED, "n_boot": N_BOOT, "clusters": dbs, "n_reexec_overrides_used": n_override,
    "ex_by_method": ex_rows, "pairwise": pair_rows, "by_database": db_rows,
}, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"ex_by_method": ex_rows, "n_overrides": n_override}))
