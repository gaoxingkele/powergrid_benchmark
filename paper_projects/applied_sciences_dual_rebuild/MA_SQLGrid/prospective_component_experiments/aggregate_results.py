#!/usr/bin/env python3
"""Registered cluster-aware aggregation for prospective MA-SQLGrid E1/E2/E4.

Importing this module is side-effect free. The CLI reads formal outputs only
after both model runs and scoring seals exist. Tests use synthetic fixtures.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

import numpy as np

import verify_freeze


HERE = Path(__file__).resolve().parent
MA = HERE.parent
SEED = 20260805
BOOTSTRAP_SAMPLES = 20_000
RANDOMIZATION_SAMPLES = 100_000
MODELS = ("qwen", "granite")
V0 = "V0_NoValueEvidence"
V1 = "V1_WithValueEvidence"


@dataclass(frozen=True)
class PairedValue:
    question_id: str
    cluster: str
    difference: float


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def _cluster_summaries(rows: Iterable[PairedValue]) -> tuple[np.ndarray, np.ndarray]:
    grouped: dict[str, list[float]] = {}
    for row in rows:
        grouped.setdefault(row.cluster, []).append(float(row.difference))
    if not grouped:
        raise ValueError("paired contrast has no rows")
    keys = sorted(grouped)
    sums = np.asarray([sum(grouped[key]) for key in keys], dtype=float)
    counts = np.asarray([len(grouped[key]) for key in keys], dtype=float)
    return sums, counts


def cluster_bootstrap(rows: list[PairedValue], *, samples: int, seed: int) -> dict[str, float]:
    """Question-weighted mean with whole-cluster percentile bootstrap."""
    sums, counts = _cluster_summaries(rows)
    estimate = float(sums.sum() / counts.sum())
    rng = np.random.default_rng(seed)
    draws = np.empty(samples, dtype=float)
    cluster_count = len(sums)
    chunk = 2_000
    for start in range(0, samples, chunk):
        stop = min(samples, start + chunk)
        indexes = rng.integers(0, cluster_count, size=(stop - start, cluster_count))
        draws[start:stop] = sums[indexes].sum(axis=1) / counts[indexes].sum(axis=1)
    low, high = np.quantile(draws, [0.025, 0.975], method="linear")
    return {"estimate": estimate, "ci_low": float(low), "ci_high": float(high),
            "bootstrap_samples": samples, "bootstrap_seed": seed}


def cluster_sign_flip(rows: list[PairedValue], *, samples: int, seed: int) -> dict[str, float | int]:
    """Two-sided Monte Carlo sign flip, preserving all rows within a cluster."""
    sums, counts = _cluster_summaries(rows)
    observed = float(sums.sum() / counts.sum())
    denominator = float(counts.sum())
    threshold = abs(observed) - 1e-15
    rng = np.random.default_rng(seed)
    extreme = 0
    chunk = 5_000
    for start in range(0, samples, chunk):
        stop = min(samples, start + chunk)
        signs = rng.integers(0, 2, size=(stop - start, len(sums)), dtype=np.int8) * 2 - 1
        statistics = (signs * sums).sum(axis=1) / denominator
        extreme += int(np.count_nonzero(np.abs(statistics) >= threshold))
    return {"p_value": (extreme + 1) / (samples + 1), "randomization_samples": samples,
            "randomization_seed": seed, "extreme_draws": extreme}


def contrast(rows: list[PairedValue], *, bootstrap_seed: int, randomization_seed: int) -> dict[str, Any]:
    out = cluster_bootstrap(rows, samples=BOOTSTRAP_SAMPLES, seed=bootstrap_seed)
    out.update(cluster_sign_flip(rows, samples=RANDOMIZATION_SAMPLES, seed=randomization_seed))
    out.update({"questions": len(rows), "clusters": len({row.cluster for row in rows})})
    return out


def holm_adjust(p_values: list[float]) -> list[float]:
    order = sorted(range(len(p_values)), key=lambda index: p_values[index])
    adjusted = [0.0] * len(p_values)
    running = 0.0
    m = len(p_values)
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (m - rank) * float(p_values[index])))
        adjusted[index] = running
    return adjusted


def claim_label(effect: dict[str, Any]) -> str:
    estimate, low, high = effect["estimate"], effect["ci_low"], effect["ci_high"]
    adjusted = effect["holm_adjusted_p"]
    if estimate > 0 and low > 0 and adjusted < 0.05:
        return "positive_component_efficacy"
    if estimate < 0 and high < 0 and adjusted < 0.05:
        return "significant_harm"
    return "no_detectable_improvement"


def apply_holm_family(effects: list[dict[str, Any]]) -> None:
    adjusted = holm_adjust([float(effect["p_value"]) for effect in effects])
    for effect, p_value in zip(effects, adjusted):
        effect["holm_adjusted_p"] = p_value
        effect["claim_label"] = claim_label(effect)


def apply_modifier_holm_family(effects: list[dict[str, Any]]) -> None:
    adjusted = holm_adjust([float(effect["p_value"]) for effect in effects])
    for effect, p_value in zip(effects, adjusted):
        effect["holm_adjusted_p"] = p_value
        if effect["estimate"] > 0 and effect["ci_low"] > 0 and p_value < 0.05:
            effect["claim_label"] = "positive_granite_minus_qwen_modifier"
        elif effect["estimate"] < 0 and effect["ci_high"] < 0 and p_value < 0.05:
            effect["claim_label"] = "negative_granite_minus_qwen_modifier"
        else:
            effect["claim_label"] = "no_detectable_backbone_modifier"


def _source_model(model: str, freeze: dict[str, Any], runs_root: Path) -> dict[str, Any]:
    run_dir = runs_root / model
    paths = {name: run_dir / name for name in (
        "predictions.jsonl", "RUN_MANIFEST.json", "candidate_selections.jsonl",
        "SELECTION_SEAL.json", "scored_rows.jsonl", "SCORING_MANIFEST.json")}
    missing = [name for name, path in paths.items() if not path.is_file()]
    if missing:
        raise RuntimeError(f"{model} missing formal artifacts: {missing}")
    run_manifest = json.loads(paths["RUN_MANIFEST.json"].read_text(encoding="utf-8"))
    scoring_manifest = json.loads(paths["SCORING_MANIFEST.json"].read_text(encoding="utf-8"))
    selection_seal = json.loads(paths["SELECTION_SEAL.json"].read_text(encoding="utf-8"))
    if run_manifest["status"] != "completed_predictions_unscored":
        raise RuntimeError(f"{model} prediction run is not complete")
    if run_manifest["freeze_sha256"] != sha256_file(HERE / "PROTOCOL_FREEZE.json"):
        raise RuntimeError(f"{model} used a different freeze")
    if run_manifest["model_sha256"] != freeze["models"][model]["model_sha256"]:
        raise RuntimeError(f"{model} model hash drift")
    if run_manifest["prediction_ledger_sha256"] != sha256_file(paths["predictions.jsonl"]):
        raise RuntimeError(f"{model} prediction ledger drift")
    if selection_seal["selection_ledger_sha256"] != sha256_file(paths["candidate_selections.jsonl"]):
        raise RuntimeError(f"{model} selection ledger drift")
    if scoring_manifest["scored_rows_sha256"] != sha256_file(paths["scored_rows.jsonl"]):
        raise RuntimeError(f"{model} scored ledger drift")
    if scoring_manifest["selection_ledger_sha256"] != selection_seal["selection_ledger_sha256"]:
        raise RuntimeError(f"{model} scoring is not tied to the sealed selection")

    expected = {(row["question_id"], row["condition"]) for row in read_jsonl(HERE / f"call_order_{model}.jsonl")}
    scored = read_jsonl(paths["scored_rows.jsonl"])
    if {(row["question_id"], row["condition"]) for row in scored} != expected or len(scored) != len(expected):
        raise RuntimeError(f"{model} scored keys do not exactly match the call-order ledger")
    predictions_all = read_jsonl(paths["predictions.jsonl"])
    predictions = {}
    for row in predictions_all:
        if row["status"] == "success":
            predictions[(row["question_id"], row["condition"])] = row
    if set(predictions) != expected:
        raise RuntimeError(f"{model} successful prediction keys are incomplete")
    for row in predictions.values():
        if row["model_sha256"] != freeze["models"][model]["model_sha256"] or row["served_model_id"] != freeze["models"][model]["served_model_id"]:
            raise RuntimeError(f"{model} prediction model identity drift")
    selections = read_jsonl(paths["candidate_selections.jsonl"])
    if {(row["question_id"], row["condition"]) for row in selections} != expected or len(selections) != len(expected):
        raise RuntimeError(f"{model} selection keys do not exactly match the call-order ledger")
    return {"run_dir": run_dir, "run_manifest": run_manifest, "scored": {(row["question_id"], row["condition"]): row for row in scored},
            "predictions": predictions, "predictions_all": predictions_all,
            "selections": {(row["question_id"], row["condition"]): row for row in selections},
            "source_hashes": {name: sha256_file(path) for name, path in paths.items()}}


def _cluster_map() -> dict[str, str]:
    rows = read_jsonl(MA / "canonical_v2_reanalysis" / "canonical_rows_v2.jsonl")
    mapping = {row["question_id"]: row["template_cluster"] for row in rows}
    if len(mapping) != 180:
        raise RuntimeError("cluster mapping is not exactly 180 questions")
    return mapping


def _efficiency_attestation(model: str, run_dir: Path, predictions_all: list[dict[str, Any]], run_manifest: dict[str, Any]) -> dict[str, Any]:
    path = run_dir / "EFFICIENCY_ATTESTATION.json"
    reasons = []
    if any(row["status"] != "success" for row in predictions_all): reasons.append("provider_failure_recorded")
    zero_retry = sum(row["retry_count"] == 0 for row in predictions_all) / len(predictions_all)
    if zero_retry < 0.95: reasons.append("zero_retry_fraction_below_0.95")
    if not path.is_file():
        reasons.append("efficiency_attestation_missing")
        attestation = None
    else:
        attestation = json.loads(path.read_text(encoding="utf-8"))
        required = {
            "exclusive_gpu_access": True, "same_server_arguments_within_backbone": True,
            "thermal_throttling_observed": False, "competing_gpu_process_incident": False,
        }
        for field, expected in required.items():
            if attestation.get(field) is not expected: reasons.append(f"attestation_{field}_not_{str(expected).lower()}")
        if attestation.get("model_key") != model: reasons.append("attestation_model_mismatch")
    return {"formal_latency_eligible": not reasons, "demotion_reasons": reasons,
            "zero_retry_fraction": zero_retry, "attestation": attestation,
            "gpu_before": run_manifest.get("gpu_before"), "gpu_after": run_manifest.get("gpu_after")}


def _bootstrap_only(rows: list[PairedValue], seed: int) -> dict[str, Any]:
    result = cluster_bootstrap(rows, samples=BOOTSTRAP_SAMPLES, seed=seed)
    result.update({"questions": len(rows), "clusters": len({row.cluster for row in rows})})
    return result


def analyze(runs_root: Path) -> dict[str, Any]:
    verify_freeze.main()
    freeze = json.loads((HERE / "PROTOCOL_FREEZE.json").read_text(encoding="utf-8"))
    cluster = _cluster_map()
    sources = {model: _source_model(model, freeze, runs_root) for model in MODELS}
    eligible = {
        row["question_id"] for row in read_jsonl(HERE / "frozen_prompts.jsonl")
        if row["condition"] == V0 and row["context_sha256"] != next(
            other["context_sha256"] for other in read_jsonl(HERE / "frozen_prompts.jsonl")
            if other["question_id"] == row["question_id"] and other["condition"] == V1)
    }
    if len(eligible) != freeze["eligible_value_intervention_questions"]:
        raise RuntimeError("eligible population drift")

    primary: dict[str, list[dict[str, Any]]] = {"E1": [], "E2": [], "cross_backbone": []}
    pair_vectors: dict[str, dict[str, dict[str, float]]] = {"E1": {}, "E2": {}}
    efficiency = []
    descriptives = []
    for model_index, model in enumerate(MODELS):
        scored = sources[model]["scored"]
        selections = sources[model]["selections"]
        predictions = sources[model]["predictions"]
        e1_rows = [PairedValue(qid, cluster[qid], float(scored[(qid, V1)]["first_correct"]) - float(scored[(qid, V0)]["first_correct"])) for qid in sorted(eligible)]
        e2_rows = [PairedValue(qid, cluster[qid], float(scored[(qid, V1)]["validator_selected_correct"]) - float(scored[(qid, V1)]["first_correct"])) for qid in sorted(cluster)]
        pair_vectors["E1"][model] = {row.question_id: row.difference for row in e1_rows}
        pair_vectors["E2"][model] = {row.question_id: row.difference for row in e2_rows}
        e2_source = [scored[(qid, V1)] for qid in sorted(cluster)]
        selection_source = [selections[(qid, V1)] for qid in sorted(cluster)]
        selected_validations = []
        for row in selection_source:
            index = row["selected_candidate_index"]
            trace = row.get("rank_trace") or []
            if index is not None and index < len(trace):
                selected_validations.append(trace[index])
        descriptives.append({
            "model": model,
            "E1_candidate_count_distribution": {
                condition: {str(count): sum(scored[(qid, condition)]["candidate_count"] == count for qid in eligible) for count in range(4)}
                for condition in (V0, V1)
            },
            "E2_questions": len(e2_source),
            "E2_candidate_count_at_least_2": sum(row["candidate_count"] >= 2 for row in e2_source),
            "E2_candidate_count_exactly_3": sum(row["candidate_count"] == 3 for row in e2_source),
            "E2_first_accuracy": sum(bool(row["first_correct"]) for row in e2_source) / len(e2_source),
            "E2_validator_accuracy": sum(bool(row["validator_selected_correct"]) for row in e2_source) / len(e2_source),
            "E2_oracle_at_3_accuracy_diagnostic_only": sum(bool(row["oracle_at_3_correct_diagnostic_only"]) for row in e2_source) / len(e2_source),
            "E2_selection_change_count": sum(row["selected_candidate_index"] not in (None, 0) for row in selection_source),
            "E2_rescue_count": sum((not row["first_correct"]) and row["validator_selected_correct"] for row in e2_source),
            "E2_harm_count": sum(row["first_correct"] and (not row["validator_selected_correct"]) for row in e2_source),
            "E2_selected_safe_count": sum(bool(row.get("safe")) for row in selected_validations),
            "E2_selected_exec_ok_count": sum(bool(row.get("exec_ok")) for row in selected_validations),
        })
        for family, rows, offset in (("E1", e1_rows, 1_100), ("E2", e2_rows, 2_100)):
            result = contrast(rows, bootstrap_seed=SEED + offset + model_index + 1,
                              randomization_seed=SEED + offset + 100 + model_index + 1)
            result.update({"family": family, "model": model, "contrast": "V1_minus_V0_first_candidate" if family == "E1" else "validator_minus_first_on_V1"})
            primary[family].append(result)

        log_latency, input_delta, output_delta, total_delta, throughput_log = [], [], [], [], []
        order = {(row["question_id"], row["condition"]): row["call_index"] for row in read_jsonl(HERE / f"call_order_{model}.jsonl")}
        order_groups: dict[str, list[float]] = {"V0_first": [], "V1_first": []}
        midpoint_rows: list[tuple[float, float]] = []
        for qid in sorted(eligible):
            p0, p1 = predictions[(qid, V0)], predictions[(qid, V1)]
            lr = math.log((float(p1["latency_ms"]) + 1.0) / (float(p0["latency_ms"]) + 1.0))
            log_latency.append(PairedValue(qid, cluster[qid], lr))
            input_delta.append(PairedValue(qid, cluster[qid], float(p1["token_input"]) - float(p0["token_input"])))
            output_delta.append(PairedValue(qid, cluster[qid], float(p1["token_output"]) - float(p0["token_output"])))
            total_delta.append(PairedValue(qid, cluster[qid], float(p1["token_total"]) - float(p0["token_total"])))
            t0 = 1000.0 * float(p0["token_output"]) / max(1.0, float(p0["latency_ms"]))
            t1 = 1000.0 * float(p1["token_output"]) / max(1.0, float(p1["latency_ms"]))
            throughput_log.append(PairedValue(qid, cluster[qid], math.log((t1 + 1e-9) / (t0 + 1e-9))))
            group = "V0_first" if order[(qid, V0)] < order[(qid, V1)] else "V1_first"
            order_groups[group].append(lr)
            midpoint_rows.append(((order[(qid, V0)] + order[(qid, V1)]) / 2.0, lr))
        latency = _bootstrap_only(log_latency, SEED + 4_100 + model_index + 1)
        latency.update({"geometric_ratio": math.exp(latency.pop("estimate")),
                        "ratio_ci_low": math.exp(latency.pop("ci_low")), "ratio_ci_high": math.exp(latency.pop("ci_high"))})
        median_midpoint = float(np.median([row[0] for row in midpoint_rows]))
        first_half = [row[1] for row in midpoint_rows if row[0] <= median_midpoint]
        second_half = [row[1] for row in midpoint_rows if row[0] > median_midpoint]
        efficiency.append({
            "model": model, "latency": latency,
            "input_token_delta": _bootstrap_only(input_delta, SEED + 4_200 + model_index + 1),
            "output_token_delta": _bootstrap_only(output_delta, SEED + 4_300 + model_index + 1),
            "total_token_delta": _bootstrap_only(total_delta, SEED + 4_400 + model_index + 1),
            "throughput_geometric_ratio": {key.replace("estimate", "geometric_ratio").replace("ci_low", "ratio_ci_low").replace("ci_high", "ratio_ci_high"): (math.exp(value) if key in {"estimate", "ci_low", "ci_high"} else value) for key, value in _bootstrap_only(throughput_log, SEED + 4_500 + model_index + 1).items()},
            "order_sensitivity_mean_log_ratio": {key: float(np.mean(values)) for key, values in order_groups.items()},
            "order_sensitivity_n": {key: len(values) for key, values in order_groups.items()},
            "drift_mean_log_ratio": {"first_half": float(np.mean(first_half)), "second_half": float(np.mean(second_half))},
            "validity": _efficiency_attestation(model, sources[model]["run_dir"], sources[model]["predictions_all"], sources[model]["run_manifest"]),
        })

    apply_holm_family(primary["E1"])
    apply_holm_family(primary["E2"])
    for index, family in enumerate(("E1", "E2")):
        qids = sorted(pair_vectors[family]["qwen"])
        rows = [PairedValue(qid, cluster[qid], pair_vectors[family]["granite"][qid] - pair_vectors[family]["qwen"][qid]) for qid in qids]
        result = contrast(rows, bootstrap_seed=SEED + 3_100 + index + 1, randomization_seed=SEED + 3_200 + index + 1)
        result.update({"family": "cross_backbone", "component": family, "contrast": "Granite_effect_minus_Qwen_effect"})
        primary["cross_backbone"].append(result)
    apply_modifier_holm_family(primary["cross_backbone"])

    return {
        "schema_version": "ma-sqlgrid-prospective-component-analysis-v1", "sap_seed": SEED,
        "bootstrap_samples": BOOTSTRAP_SAMPLES, "randomization_samples": RANDOMIZATION_SAMPLES,
        "primary_effects": primary, "descriptives": descriptives, "efficiency": efficiency,
        "replication": {family: all(effect["claim_label"] == "positive_component_efficacy" for effect in primary[family]) for family in ("E1", "E2")},
        "source_hashes": {model: sources[model]["source_hashes"] for model in MODELS},
    }


def write_outputs(result: dict[str, Any], out: Path, overwrite: bool) -> None:
    if out.exists() and any(out.iterdir()) and not overwrite:
        raise RuntimeError("analysis output exists; pass --overwrite only for a byte-identical rerun audit")
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "RESULTS.json", result)
    with (out / "primary_effects.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["family", "model", "component", "contrast", "questions", "clusters", "estimate", "ci_low", "ci_high", "p_value", "holm_adjusted_p", "claim_label"]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for family in ("E1", "E2", "cross_backbone"):
            writer.writerows(result["primary_effects"][family])
    with (out / "efficiency.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["model", "geometric_latency_ratio", "ratio_ci_low", "ratio_ci_high", "formal_latency_eligible", "demotion_reasons"])
        writer.writeheader()
        for row in result["efficiency"]:
            writer.writerow({"model": row["model"], "geometric_latency_ratio": row["latency"]["geometric_ratio"],
                             "ratio_ci_low": row["latency"]["ratio_ci_low"], "ratio_ci_high": row["latency"]["ratio_ci_high"],
                             "formal_latency_eligible": row["validity"]["formal_latency_eligible"],
                             "demotion_reasons": ";".join(row["validity"]["demotion_reasons"])})
    lines = ["# Prospective Component Analysis", "", "Generated strictly under the frozen SAP.", ""]
    for family in ("E1", "E2", "cross_backbone"):
        lines += [f"## {family}", ""]
        for effect in result["primary_effects"][family]:
            name = effect.get("model") or effect.get("component")
            lines.append(f"- {name}: effect {effect['estimate']:+.4f}, 95% cluster CI [{effect['ci_low']:+.4f}, {effect['ci_high']:+.4f}], Holm p={effect['holm_adjusted_p']:.6g}; {effect['claim_label']}.")
        lines.append("")
    (out / "ANALYSIS_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    files = [out / "RESULTS.json", out / "primary_effects.csv", out / "efficiency.csv", out / "ANALYSIS_REPORT.md"]
    write_json(out / "ANALYSIS_MANIFEST.json", {"schema_version": "ma-sqlgrid-prospective-analysis-manifest-v1",
              "files": {path.name: {"sha256": sha256_file(path), "bytes": path.stat().st_size} for path in files}})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs-root", type=Path, default=HERE / "runs")
    parser.add_argument("--out", type=Path, default=HERE / "analysis")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    result = analyze(args.runs_root.resolve())
    write_outputs(result, args.out.resolve(), args.overwrite)
    print("PASS: registered E1/E2/E4 aggregation completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
