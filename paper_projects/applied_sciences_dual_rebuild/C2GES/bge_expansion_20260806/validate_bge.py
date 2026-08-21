#!/usr/bin/env python3
"""Independent recomputation validator for the prospective BGE expansion."""
from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
SEEDS = [2026, 2027, 2028, 2029, 2030]
KS = [1, 3, 5, 10]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_path(seed: int) -> Path:
    if seed == 2026:
        return REPO / "paper_projects/2026_c2ges_engineeringletters/workspace/w3_c2_pilot/full_8000_1500_1500/label_blind/predictions.jsonl"
    return REPO / f"paper_projects/2026_c2ges_engineeringletters/workspace/w4_c2_five_seed/seed_{seed}/label_blind/predictions.jsonl"


def holm(raw: list[float]) -> list[float]:
    order = sorted(range(len(raw)), key=lambda i: raw[i])
    out = [0.0] * len(raw)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(raw) - rank) * raw[index]))
        out[index] = running
    return out


def main() -> int:
    freeze = json.loads((HERE / "PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
    published = json.loads((HERE / "RESULTS_SUMMARY.json").read_text(encoding="utf-8"))
    checks = []

    def check(name: str, passed: bool, evidence) -> None:
        checks.append({"name": name, "passed": bool(passed), "evidence": evidence})

    bge_path = HERE / "formal_run/predictions.jsonl"
    bge_rows = [json.loads(line) for line in bge_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    keys = [(row["qid"], int(row["k"])) for row in bge_rows]
    check("BGE 6000 unique rows", len(bge_rows) == 6000 and len(set(keys)) == 6000, {"rows": len(bge_rows), "unique": len(set(keys))})
    check("BGE four complete budgets", {k: sum(int(row["k"]) == k for row in bge_rows) for k in KS} == {k: 1500 for k in KS}, {k: sum(int(row["k"]) == k for row in bge_rows) for k in KS})
    check("BGE mode and finite metrics", all(row["mode"] == "bge_reranker_base" and all(np.isfinite(float(row[x])) for x in ("precision", "recall", "f1")) for row in bge_rows), "all rows")
    check("145 BGE document clusters", len({row["underlying_document_id"] for row in bge_rows}) == 145, len({row["underlying_document_id"] for row in bge_rows}))

    values = defaultdict(dict)
    docs = {}
    for seed in SEEDS:
        path = source_path(seed)
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                qid, k = str(row["qid"]), int(row["k"])
                docs[qid] = str(row["underlying_document_id"])
                if row["mode"] == "full":
                    values[("c2ges_full", k)][(qid, seed)] = tuple(float(row[x]) for x in ("precision", "recall", "f1"))
                elif row["mode"] == "bm25" and seed == 2026:
                    values[("bm25", k)][(qid, 0)] = tuple(float(row[x]) for x in ("precision", "recall", "f1"))
    mini_path = REPO / freeze["inputs"]["reference_ledgers"]["minilm"]["path"]
    for method, path in (("minilm_cross_encoder", mini_path), ("bge_reranker_base", bge_path)):
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                row = json.loads(line)
                qid, k = str(row["qid"]), int(row["k"])
                docs[qid] = str(row["underlying_document_id"])
                values[(method, k)][(qid, 0)] = tuple(float(row[x]) for x in ("precision", "recall", "f1"))

    def claims(method: str, k: int, metric: int) -> dict[str, float]:
        source = values[(method, k)]
        return {qid: float(np.mean([v[metric] for (q, _), v in source.items() if q == qid])) for qid in sorted({q for q, _ in source})}

    cell_diffs = []
    for row in published["cells"]:
        for key, metric in (("mean_precision", 0), ("mean_recall", 1), ("mean_f1", 2)):
            cell_diffs.append(abs(float(row[key]) - float(np.mean(list(claims(row["method"], int(row["k"]), metric).values())))))
        check(f"cell coverage {row['method']} K={row['k']}", int(row["n_claims"]) == 1500 and int(row["n_document_clusters"]) == 145, {"claims": row["n_claims"], "clusters": row["n_document_clusters"]})
    check("independent 16-cell metric recomputation", max(cell_diffs) < 1e-15, max(cell_diffs))

    recomputed = []
    for index, comparator in enumerate(freeze["statistics"]["primary_comparisons"]):
        bge, ref = claims("bge_reranker_base", 3, 2), claims(comparator, 3, 2)
        by_doc = defaultdict(list)
        for qid in sorted(set(bge) & set(ref)):
            by_doc[docs[qid]].append(bge[qid] - ref[qid])
        names = sorted(by_doc)
        sums = np.asarray([sum(by_doc[name]) for name in names], dtype=float)
        counts = np.asarray([len(by_doc[name]) for name in names], dtype=float)
        estimate = float(sums.sum() / counts.sum())
        rng = np.random.default_rng(int(freeze["statistics"]["bootstrap_seed_base"]) + index)
        sampled = rng.integers(0, len(names), size=(int(freeze["statistics"]["bootstrap_draws"]), len(names)))
        low, high = np.quantile(sums[sampled].sum(axis=1) / counts[sampled].sum(axis=1), [0.025, 0.975])
        rng = np.random.default_rng(int(freeze["statistics"]["signflip_seed_base"]) + index)
        extreme, done = 0, 0
        while done < int(freeze["statistics"]["signflip_samples"]):
            take = min(1000, int(freeze["statistics"]["signflip_samples"]) - done)
            simulations = (rng.choice((-1.0, 1.0), size=(take, len(names))) * sums).sum(axis=1) / counts.sum()
            extreme += int(np.sum(np.abs(simulations) >= abs(estimate) - 1e-15))
            done += take
        recomputed.append((estimate, float(low), float(high), extreme / done))
    adjusted = holm([row[3] for row in recomputed])
    contrast_diffs = []
    for published_row, raw, adj in zip(published["primary_contrasts"], recomputed, adjusted):
        contrast_diffs += [abs(float(published_row["mean_difference"]) - raw[0]), abs(float(published_row["composition_interval_low"]) - raw[1]), abs(float(published_row["composition_interval_high"]) - raw[2]), abs(float(published_row["signflip_p_raw"]) - raw[3]), abs(float(published_row["holm_p"]) - adj)]
    check("independent three-contrast statistics and Holm recomputation", max(contrast_diffs) < 1e-15, max(contrast_diffs))

    provenance = json.loads((HERE / "formal_run/provenance.json").read_text(encoding="utf-8"))
    resource = json.loads((HERE / "formal_run/resource_usage.json").read_text(encoding="utf-8"))
    check("formal provenance prediction binding", provenance["predictions_sha256"] == sha256(bge_path), provenance["predictions_sha256"])
    check("formal run success and counts", resource["status"] == "success" and resource["instances"] == 1500 and resource["prediction_rows"] == 6000, resource)
    check("model revision binding", provenance["model_revision"] == freeze["inputs"]["model"]["revision"] and provenance["model_inventory"] == freeze["inputs"]["model"]["inventory"], provenance["model_revision"])
    manifest = json.loads((HERE / "artifact_manifest.json").read_text(encoding="utf-8"))
    bad = []
    for rel, identity in manifest["artifacts"].items():
        path = HERE / rel
        if not path.is_file() or path.stat().st_size != identity["bytes"] or sha256(path) != identity["sha256"]:
            bad.append(rel)
    check("artifact manifest identity", not bad, {"checked": len(manifest["artifacts"]), "bad": bad})
    for name in ("fig_bge_budget.svg", "fig_bge_forest.svg"):
        ET.parse(HERE / name)
    check("SVG figures parse", True, 2)
    check("TeX and raster/vector assets present", all((HERE / name).is_file() and (HERE / name).stat().st_size > 0 for name in ("primary_contrasts.tex", "fig_bge_budget.pdf", "fig_bge_budget.png", "fig_bge_forest.pdf", "fig_bge_forest.png")), "all present")

    report = {
        "schema_version": "c2ges-bge-expansion-independent-validation-v1",
        "decision": "PASS_INTEGRATION" if all(item["passed"] for item in checks) else "BLOCK",
        "freeze_content_sha256": freeze["freeze_content_sha256"],
        "checks": checks,
        "claim_boundary": freeze["claim_boundary"],
    }
    (HERE / "INDEPENDENT_VALIDATION.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md = ["# Independent BGE Expansion Validation", "", f"Decision: **{report['decision']}**", "", f"Freeze: `{freeze['freeze_content_sha256']}`", ""]
    md += [f"- {'PASS' if item['passed'] else 'FAIL'} — {item['name']}: `{item['evidence']}`" for item in checks]
    md += ["", "Integration is authorized only within the frozen human-gold FEVER zero-shot comparison boundary; this is not NERC validation."]
    (HERE / "INDEPENDENT_VALIDATION.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps({"decision": report["decision"], "checks": len(checks)}))
    return 0 if report["decision"] == "PASS_INTEGRATION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
