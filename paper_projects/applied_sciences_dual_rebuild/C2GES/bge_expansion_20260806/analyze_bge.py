#!/usr/bin/env python3
"""Analyze the prospectively frozen BGE FEVER expansion."""
from __future__ import annotations

import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SEEDS = [2026, 2027, 2028, 2029, 2030]
KS = [1, 3, 5, 10]
METHODS = ["c2ges_full", "bm25", "minilm_cross_encoder", "bge_reranker_base"]
DISPLAY = {"c2ges_full": "C2GES full", "bm25": "BM25", "minilm_cross_encoder": "MiniLM cross-encoder", "bge_reranker_base": "BGE reranker"}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def holm(raw: list[float]) -> list[float]:
    order = sorted(range(len(raw)), key=lambda i: raw[i])
    adjusted = [0.0] * len(raw)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(raw) - rank) * raw[index]))
        adjusted[index] = running
    return adjusted


def source_path(seed: int) -> Path:
    if seed == 2026:
        return REPO / "paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/label_blind/predictions.jsonl"
    return REPO / f"paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/seed_{seed}/label_blind/predictions.jsonl"


def load_values(freeze: dict) -> tuple[dict, dict]:
    values: dict[tuple[str, int], dict[tuple[str, int], tuple[float, float, float]]] = defaultdict(dict)
    docs: dict[str, str] = {}
    for seed in SEEDS:
        path = source_path(seed)
        expected = freeze["inputs"]["reference_ledgers"][f"c2ges_seed_{seed}"]
        if sha256(path).upper() != expected["sha256"]:
            raise RuntimeError(f"source identity mismatch: {path}")
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                k = int(row["k"])
                qid = str(row["qid"])
                docs[qid] = str(row["underlying_document_id"])
                if row["mode"] == "full":
                    values[("c2ges_full", k)][(qid, seed)] = (float(row["precision"]), float(row["recall"]), float(row["f1"]))
                elif row["mode"] == "bm25" and seed == 2026:
                    values[("bm25", k)][(qid, 0)] = (float(row["precision"]), float(row["recall"]), float(row["f1"]))
    for method, path, key in [
        ("minilm_cross_encoder", REPO / freeze["inputs"]["reference_ledgers"]["minilm"]["path"], "minilm"),
        ("bge_reranker_base", HERE / "formal_run/predictions.jsonl", None),
    ]:
        if key and sha256(path).upper() != freeze["inputs"]["reference_ledgers"][key]["sha256"]:
            raise RuntimeError(f"reference identity mismatch: {path}")
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                k = int(row["k"])
                qid = str(row["qid"])
                values[(method, k)][(qid, 0)] = (float(row["precision"]), float(row["recall"]), float(row["f1"]))
                docs[qid] = str(row["underlying_document_id"])
    return values, docs


def claim_metric(values: dict, method: str, k: int, metric_index: int) -> dict[str, float]:
    source = values[(method, k)]
    qids = sorted({qid for qid, _ in source})
    return {qid: float(np.mean([triple[metric_index] for (q, _), triple in source.items() if q == qid])) for qid in qids}


def main() -> int:
    freeze_path = HERE / "PROTOCOL_FREEZE.json"
    freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
    run = HERE / "formal_run"
    provenance = json.loads((run / "provenance.json").read_text(encoding="utf-8"))
    if provenance["freeze_sha256"] != sha256(freeze_path):
        raise RuntimeError("formal run is not bound to current freeze")
    if provenance["predictions_sha256"] != sha256(run / "predictions.jsonl"):
        raise RuntimeError("formal prediction identity mismatch")
    values, docs = load_values(freeze)

    cells = []
    for method in METHODS:
        for k in KS:
            f1 = claim_metric(values, method, k, 2)
            precision = claim_metric(values, method, k, 0)
            recall = claim_metric(values, method, k, 1)
            cells.append({
                "freeze_content_sha256": freeze["freeze_content_sha256"],
                "method": method,
                "k": k,
                "n_claims": len(f1),
                "n_document_clusters": len({docs[q] for q in f1}),
                "mean_precision": float(np.mean(list(precision.values()))),
                "mean_recall": float(np.mean(list(recall.values()))),
                "mean_f1": float(np.mean(list(f1.values()))),
            })
    write_csv(HERE / "cell_summary.csv", cells)

    comparisons = freeze["statistics"]["primary_comparisons"]
    contrasts = []
    for index, comparator in enumerate(comparisons):
        bge = claim_metric(values, "bge_reranker_base", 3, 2)
        ref = claim_metric(values, comparator, 3, 2)
        qids = sorted(set(bge) & set(ref))
        by_doc: dict[str, list[float]] = defaultdict(list)
        for qid in qids:
            by_doc[docs[qid]].append(bge[qid] - ref[qid])
        names = sorted(by_doc)
        sums = np.asarray([sum(by_doc[name]) for name in names], dtype=float)
        counts = np.asarray([len(by_doc[name]) for name in names], dtype=float)
        estimate = float(sums.sum() / counts.sum())
        boot_seed = int(freeze["statistics"]["bootstrap_seed_base"]) + index
        rng = np.random.default_rng(boot_seed)
        sampled = rng.integers(0, len(names), size=(int(freeze["statistics"]["bootstrap_draws"]), len(names)))
        boot = sums[sampled].sum(axis=1) / counts[sampled].sum(axis=1)
        low, high = np.quantile(boot, [0.025, 0.975])
        flip_seed = int(freeze["statistics"]["signflip_seed_base"]) + index
        rng = np.random.default_rng(flip_seed)
        extreme = 0
        done = 0
        batch = 1000
        while done < int(freeze["statistics"]["signflip_samples"]):
            take = min(batch, int(freeze["statistics"]["signflip_samples"]) - done)
            signs = rng.choice((-1.0, 1.0), size=(take, len(names)))
            simulations = (signs * sums).sum(axis=1) / counts.sum()
            extreme += int(np.sum(np.abs(simulations) >= abs(estimate) - 1e-15))
            done += take
        contrasts.append({
            "freeze_content_sha256": freeze["freeze_content_sha256"],
            "comparison": f"bge_reranker_base-minus-{comparator}",
            "k": 3,
            "n_claims": len(qids),
            "n_document_clusters": len(names),
            "mean_difference": estimate,
            "composition_interval_low": float(low),
            "composition_interval_high": float(high),
            "signflip_p_raw": extreme / done,
            "holm_p": None,
            "promoted": None,
        })
    adjusted = holm([row["signflip_p_raw"] for row in contrasts])
    for row, value in zip(contrasts, adjusted):
        row["holm_p"] = value
        row["promoted"] = bool(value < float(freeze["statistics"]["alpha"]))
    write_csv(HERE / "primary_contrasts.csv", contrasts)

    tex = [
        f"% freeze content SHA-256 {freeze['freeze_content_sha256']}",
        "\\begin{tabular}{lrrrr}",
        "\\toprule",
        "BGE minus comparator & $\\Delta$ F1 & 95\\% composition interval & raw $p$ & Holm $p$ \\\\",
        "\\midrule",
    ]
    for row in contrasts:
        comparator = row["comparison"].split("-minus-", 1)[1]
        tex.append(f"{DISPLAY[comparator]} & {row['mean_difference']:+.4f} & [{row['composition_interval_low']:+.4f}, {row['composition_interval_high']:+.4f}] & {row['signflip_p_raw']:.4f} & {row['holm_p']:.4f} \\\\")
    tex.extend(["\\bottomrule", "\\end{tabular}"])
    (HERE / "primary_contrasts.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, ax = plt.subplots(figsize=(7.2, 4.5))
    styles = {"c2ges_full": ("o", "-"), "bm25": ("s", "--"), "minilm_cross_encoder": ("^", "-."), "bge_reranker_base": ("D", ":")}
    for method in METHODS:
        marker, linestyle = styles[method]
        ys = [next(row["mean_f1"] for row in cells if row["method"] == method and row["k"] == k) for k in KS]
        ax.plot(KS, ys, marker=marker, linestyle=linestyle, label=DISPLAY[method])
    ax.set(xlabel="Evidence budget K", ylabel="Claim-weighted evidence F1", title="Prospective BGE comparison on human-gold FEVER")
    ax.legend(fontsize=8)
    fig.tight_layout()
    for ext in ("svg", "pdf"):
        fig.savefig(HERE / f"fig_bge_budget.{ext}")
    fig.savefig(HERE / "fig_bge_budget.png", dpi=450)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    y = np.arange(len(contrasts))
    estimates = np.asarray([row["mean_difference"] for row in contrasts])
    lows = np.asarray([row["composition_interval_low"] for row in contrasts])
    highs = np.asarray([row["composition_interval_high"] for row in contrasts])
    ax.errorbar(estimates, y, xerr=[estimates - lows, highs - estimates], fmt="o", capsize=3)
    ax.axvline(0.0, color="black", linewidth=1)
    ax.set_yticks(y, [DISPLAY[row["comparison"].split("-minus-", 1)[1]] for row in contrasts])
    ax.set(xlabel="BGE minus comparator evidence F1", title="K=3 document-cluster composition sensitivity")
    fig.tight_layout()
    for ext in ("svg", "pdf"):
        fig.savefig(HERE / f"fig_bge_forest.{ext}")
    fig.savefig(HERE / "fig_bge_forest.png", dpi=450)
    plt.close(fig)

    resource = json.loads((run / "resource_usage.json").read_text(encoding="utf-8"))
    summary = {
        "schema_version": "c2ges-bge-expansion-results-v1",
        "freeze_content_sha256": freeze["freeze_content_sha256"],
        "prediction_rows": resource["prediction_rows"],
        "candidate_pairs": resource["candidate_pairs"],
        "test_claims": resource["instances"],
        "document_clusters": 145,
        "cells": cells,
        "primary_contrasts": contrasts,
        "resource_usage": resource,
        "claim_boundary": freeze["claim_boundary"],
    }
    (HERE / "RESULTS_SUMMARY.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# Prospective BGE Expansion Results",
        "",
        f"Freeze: `{freeze['freeze_content_sha256']}`.",
        "",
        "Primary endpoint: claim-weighted exact sentence-ID evidence F1 at K=3 on 1,500 human-gold FEVER claims in 145 document clusters.",
        "",
        "| Comparison | Difference | 95% composition interval | Raw p | Holm p | Promoted |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for row in contrasts:
        lines.append(f"| {row['comparison']} | {row['mean_difference']:+.4f} | [{row['composition_interval_low']:+.4f}, {row['composition_interval_high']:+.4f}] | {row['signflip_p_raw']:.4f} | {row['holm_p']:.4f} | {str(row['promoted']).lower()} |")
    lines += ["", f"Formal CPU run: {resource['wall_seconds']:.1f} s; sampled peak RSS {resource['sampled_peak_rss_bytes'] / 2**20:.1f} MiB; {resource['candidate_pairs']} candidate pairs.", "", "This is a zero-shot FEVER baseline comparison, not NERC or deployed power-grid validation."]
    (HERE / "RESULTS_SUMMARY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    excluded = {"artifact_manifest.json", "INDEPENDENT_VALIDATION.json", "INDEPENDENT_VALIDATION.md"}
    artifacts = {}
    for path in sorted(p for p in HERE.rglob("*") if p.is_file() and p.name not in excluded and "__pycache__" not in p.parts):
        rel = path.relative_to(HERE).as_posix()
        artifacts[rel] = {"bytes": path.stat().st_size, "sha256": sha256(path)}
    manifest = {"schema_version": "c2ges-bge-expansion-artifact-manifest-v1", "freeze_content_sha256": freeze["freeze_content_sha256"], "artifact_count": len(artifacts), "artifacts": artifacts}
    (HERE / "artifact_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"cells": len(cells), "contrasts": len(contrasts), "artifacts": len(artifacts)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
