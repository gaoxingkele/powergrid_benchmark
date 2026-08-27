"""Derive the frozen Stage-3 paper tables from the accepted v2 execution.

This script is deliberately read-only with respect to the Stage-2 execution
namespace.  It verifies the sealed manifest and its outputs, independently
recomputes the paired and moving-block statistics, applies the frozen claim
gates, and writes only Stage-3 paper tables plus a provenance record.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import subprocess
from collections.abc import Iterable
from io import StringIO
from pathlib import Path
from typing import Any

import numpy as np


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
RESULT_DIR = HERE / "results"
CONTRACT_PATH = HERE / "upgrade_contract.json"
EXECUTION_MANIFEST_PATH = HERE / "run_manifest.json"
PROVENANCE_PATH = HERE / "statistics_provenance.json"
TABLE_DIR = PROJECT_ROOT / "manuscript" / "derived_tables"
RUN_NAMESPACE = "p1_ieee_access_upgrade_v2"
STAGE_ID = "p1v5_s3_statistics_robustness"
EXPECTED_STAGE2_COMMIT = "cffe8fdb80a022978cc3715bd1fb014647bd1617"
TABLE_PATHS = {
    "paired": TABLE_DIR / "v2_paired_seed_effects.csv",
    "moving": TABLE_DIR / "v2_moving_block_sensitivity.csv",
    "deterministic": TABLE_DIR / "v2_deterministic_references.csv",
    "cross_cap": TABLE_DIR / "v2_cross_cap_descriptive.csv",
    "router": TABLE_DIR / "v2_claim_wording_router.csv",
}


def fail(message: str) -> None:
    raise SystemExit(f"STATISTICS INVALID: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_lf(value: bytes) -> bytes:
    return value.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def canonical_crlf(value: bytes) -> bytes:
    return canonical_lf(value).replace(b"\n", b"\r\n")


def line_ending_record(value: bytes) -> dict[str, Any]:
    crlf = value.count(b"\r\n")
    bare_cr = value.replace(b"\r\n", b"").count(b"\r")
    lf = value.count(b"\n") - crlf
    if crlf and not lf and not bare_cr:
        rendering = "CRLF"
    elif lf and not crlf and not bare_cr:
        rendering = "LF"
    elif not crlf and not lf and not bare_cr:
        rendering = "no_line_endings"
    else:
        rendering = "mixed"
    return {
        "rendering": rendering,
        "crlf_count": crlf,
        "lf_only_count": lf,
        "bare_cr_count": bare_cr,
        "bytes": len(value),
        "sha256": sha256_bytes(value),
        "canonical_lf_sha256": sha256_bytes(canonical_lf(value)),
    }


def git_output(*args: str, binary: bool = False) -> bytes | str:
    completed = subprocess.run(
        ["git", *args],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=not binary,
    )
    if completed.returncode:
        error = completed.stderr if isinstance(completed.stderr, str) else completed.stderr.decode(errors="replace")
        fail(f"git {' '.join(args)} failed: {error.strip()}")
    return completed.stdout


def git_blob(relative: Path, revision: str = "HEAD") -> tuple[str, bytes]:
    prefix = str(git_output("rev-parse", "--show-prefix")).strip().replace("\\", "/")
    repository_path = prefix + relative.as_posix()
    return repository_path, bytes(git_output("show", f"{revision}:{repository_path}", binary=True))


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required JSON missing: {path.relative_to(PROJECT_ROOT)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse {path.name}: {exc}")
    require(isinstance(value, dict), f"{path.name} root must be an object")
    return value


def load_csv(path: Path) -> list[dict[str, str]]:
    require(path.is_file(), f"required CSV missing: {path.relative_to(PROJECT_ROOT)}")
    try:
        with path.open("r", encoding="utf-8", errors="strict", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        fail(f"cannot parse {path.name}: {exc}")
    require(rows, f"CSV is empty: {path.name}")
    return rows


def format_float(value: float | None, digits: int = 12) -> str:
    if value is None or not math.isfinite(value):
        return ""
    return f"{value:.{digits}g}"


def csv_bytes(rows: list[dict[str, Any]], fieldnames: Iterable[str] | None = None) -> bytes:
    require(bool(rows), "cannot serialize an empty paper table")
    names = list(fieldnames or rows[0].keys())
    buffer = StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=names, extrasaction="raise", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")


def verify_frozen_sources() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    contract = load_json(CONTRACT_PATH)
    manifest = load_json(EXECUTION_MANIFEST_PATH)
    require(contract.get("run_namespace") == RUN_NAMESPACE, "contract namespace changed")
    require(manifest.get("run_namespace") == RUN_NAMESPACE, "manifest namespace changed")
    require(manifest.get("status") == "completed", "accepted execution is not completed")
    require(manifest.get("protocol_valid") is True, "accepted execution is not protocol-valid")
    require(
        manifest.get("approved_stage") == "p1v4_s2_fair_baselines_attribution",
        "execution does not identify the accepted Stage-2 source",
    )
    require(manifest.get("row_counts", {}).get("run_results") == 2310, "manifest result-row count changed")
    require(manifest.get("row_counts", {}).get("paired_effects") == 30, "manifest paired-row count changed")
    require(manifest.get("row_counts", {}).get("moving_block_supplement") == 36, "manifest block-row count changed")

    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", EXPECTED_STAGE2_COMMIT, "HEAD"],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
    )
    require(ancestor.returncode == 0, "accepted Stage-2 commit is not an ancestor of HEAD")

    manifest_relative = EXECUTION_MANIFEST_PATH.relative_to(PROJECT_ROOT)
    manifest_repo_path, manifest_blob = git_blob(manifest_relative)
    _, accepted_manifest_blob = git_blob(manifest_relative, EXPECTED_STAGE2_COMMIT)
    manifest_working = EXECUTION_MANIFEST_PATH.read_bytes()
    require(
        canonical_lf(manifest_blob) == canonical_lf(accepted_manifest_blob),
        "committed execution manifest no longer matches the accepted Stage-2 commit",
    )
    require(
        canonical_lf(manifest_working) == canonical_lf(manifest_blob),
        "working execution manifest differs in content from its committed Git blob",
    )

    script_relative = Path(manifest["script"]["path"].replace("\\", "/"))
    script_path = PROJECT_ROOT / script_relative
    require(script_path.is_file(), "execution script named by manifest is missing")
    script_repo_path, script_blob = git_blob(script_relative)
    _, accepted_script_blob = git_blob(script_relative, EXPECTED_STAGE2_COMMIT)
    script_working = script_path.read_bytes()
    script_recorded = manifest["script"]["sha256"]
    script_blob_hash = sha256_bytes(script_blob)
    require(
        canonical_lf(script_blob) == canonical_lf(accepted_script_blob),
        "committed runner no longer matches the accepted Stage-2 commit",
    )
    require(
        script_recorded == script_blob_hash,
        "real committed-content mismatch: manifest runner hash does not match the committed Git blob",
    )
    require(
        canonical_lf(script_working) == canonical_lf(script_blob),
        "working runner differs from committed content after line-ending normalization",
    )

    contract_relative = Path(manifest["contract"]["path"].replace("\\", "/"))
    contract_path = PROJECT_ROOT / contract_relative
    require(contract_path.resolve() == CONTRACT_PATH.resolve(), "manifest points to an unexpected contract")
    contract_repo_path, contract_blob = git_blob(contract_relative)
    _, accepted_contract_blob = git_blob(contract_relative, EXPECTED_STAGE2_COMMIT)
    contract_working = contract_path.read_bytes()
    contract_recorded = manifest["contract"]["sha256"]
    require(
        canonical_lf(contract_blob) == canonical_lf(accepted_contract_blob),
        "committed contract no longer matches the accepted Stage-2 commit",
    )
    require(
        canonical_lf(contract_working) == canonical_lf(contract_blob),
        "working contract differs from committed content after line-ending normalization",
    )
    contract_match_basis = "working_checkout_bytes"
    if sha256_bytes(contract_working) != contract_recorded:
        require(
            sha256_bytes(contract_blob) == contract_recorded
            or sha256_bytes(canonical_crlf(contract_blob)) == contract_recorded,
            "manifest contract hash matches neither committed nor line-ending-rendered committed content",
        )
        contract_match_basis = "committed_content_with_recorded_line_ending_rendering"

    output_index = manifest.get("outputs", {})
    require(isinstance(output_index, dict) and output_index, "manifest output index is missing")
    verified_outputs: dict[str, Any] = {}
    for name, record in sorted(output_index.items()):
        path = RESULT_DIR / name
        require(path.is_file(), f"sealed manifest output missing: results/{name}")
        observed_hash = sha256(path)
        require(observed_hash == record.get("sha256"), f"sealed output hash mismatch: {name}")
        require(path.stat().st_size == record.get("bytes"), f"sealed output size mismatch: {name}")
        verified_outputs[name] = {"sha256": observed_hash, "bytes": path.stat().st_size}

    provenance = {
        "accepted_stage2_commit": EXPECTED_STAGE2_COMMIT,
        "accepted_stage2_commit_is_ancestor_of_head": True,
        "execution_manifest": {
            "path": manifest_relative.as_posix(),
            "repository_path": manifest_repo_path,
            "working_checkout": line_ending_record(manifest_working),
            "committed_blob_sha256": sha256_bytes(manifest_blob),
            "accepted_stage2_blob_sha256": sha256_bytes(accepted_manifest_blob),
            "canonical_content_match": True,
        },
        "execution_script": {
            "path": script_relative.as_posix(),
            "repository_path": script_repo_path,
            "manifest_recorded_sha256": script_recorded,
            "committed_blob_sha256": script_blob_hash,
            "accepted_stage2_blob_sha256": sha256_bytes(accepted_script_blob),
            "working_checkout": line_ending_record(script_working),
            "match_basis": "manifest hash equals committed Git blob; working CRLF rendering is recorded separately",
            "scientific_source_match": True,
        },
        "contract": {
            "path": contract_relative.as_posix(),
            "repository_path": contract_repo_path,
            "manifest_recorded_sha256": contract_recorded,
            "committed_blob_sha256": sha256_bytes(contract_blob),
            "accepted_stage2_blob_sha256": sha256_bytes(accepted_contract_blob),
            "working_checkout": line_ending_record(contract_working),
            "match_basis": contract_match_basis,
            "canonical_content_match": True,
        },
        "verified_sealed_outputs": verified_outputs,
    }
    return contract, manifest, provenance


def exact_sign_flip(differences: np.ndarray) -> float:
    observed = abs(float(np.mean(differences)))
    count = 0
    for signs in itertools.product((-1.0, 1.0), repeat=len(differences)):
        statistic = abs(float(np.mean(differences * np.asarray(signs, dtype=np.float64))))
        count += statistic >= observed - 1e-15
    return count / (2 ** len(differences))


def holm_adjust(pvalues: list[float]) -> list[float]:
    order = sorted(range(len(pvalues)), key=lambda index: (pvalues[index], index))
    adjusted = [math.nan] * len(pvalues)
    running = 0.0
    for rank, index in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = running
    return adjusted


def recompute_paired(rows: list[dict[str, str]], contract: dict[str, Any]) -> list[dict[str, Any]]:
    require(len(rows) == 2310, "run_results must contain 2310 rows")
    require(all(row["execution_status"] == "completed" for row in rows), "run_results contains a failed row")
    primary = [row for row in rows if row["cap"] == "0.70"]
    output: list[dict[str, Any]] = []
    for family in contract["statistics"]["families"]:
        objective = family["selection_objective"]
        metric = family["metric"]
        better = family["better_direction"]
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            family_rows: list[dict[str, Any]] = []
            pvalues: list[float] = []
            for contrast in family["contrasts"]:
                treatment = {
                    int(row["seed_index"]): float(row[metric])
                    for row in primary
                    if int(row["horizon_hours"]) == int(horizon)
                    and row["selection_objective"] == objective
                    and row["condition_id"] == contrast["treatment"]
                }
                control = {
                    int(row["seed_index"]): float(row[metric])
                    for row in primary
                    if int(row["horizon_hours"]) == int(horizon)
                    and row["selection_objective"] == objective
                    and row["condition_id"] == contrast["control"]
                }
                common = sorted(set(treatment) & set(control))
                require(common == list(range(10)), f"incomplete paired seeds for {contrast['id']} h={horizon}")
                differences = np.asarray([treatment[index] - control[index] for index in common], dtype=np.float64)
                mean_difference = float(np.mean(differences))
                median_difference = float(np.median(differences))
                sample_sd = float(np.std(differences, ddof=1))
                zero_variance = sample_sd == 0.0
                pvalue = exact_sign_flip(differences)
                critical = float(contract["statistics"]["seed_conditional_interval"]["critical_value"])
                margin = 0.0 if zero_variance else critical * sample_sd / math.sqrt(len(differences))
                ties = np.abs(differences) <= 1e-15
                favorable = differences < -1e-15 if better == "lower" else differences > 1e-15
                adverse = (~ties) & (~favorable)
                if abs(mean_difference) <= 1e-15:
                    direction = "null"
                elif (mean_difference < 0 and better == "lower") or (mean_difference > 0 and better == "higher"):
                    direction = "favorable"
                else:
                    direction = "adverse"
                record: dict[str, Any] = {
                    "run_namespace": RUN_NAMESPACE,
                    "family_id": family["family_id"],
                    "horizon_hours": horizon,
                    "selection_objective": objective,
                    "contrast_id": contrast["id"],
                    "treatment_condition_id": contrast["treatment"],
                    "control_condition_id": contrast["control"],
                    "metric": metric,
                    "better_direction": better,
                    "execution_status": "completed",
                    "n_pairs": len(common),
                    "mean_treatment_minus_control": format_float(mean_difference),
                    "median_treatment_minus_control": format_float(median_difference),
                    "sample_sd": format_float(sample_sd),
                    "dz": "" if zero_variance else format_float(mean_difference / sample_sd),
                    "zero_variance": str(zero_variance).lower(),
                    "treatment_wins": int(favorable.sum()),
                    "ties": int(ties.sum()),
                    "control_wins": int(adverse.sum()),
                    "p_exact_sign_flip": format_float(pvalue),
                    "p_holm_within_family_horizon": "",
                    "holm_significant_005": "",
                    "seed_interval_low": format_float(mean_difference - margin),
                    "seed_interval_high": format_float(mean_difference + margin),
                    "mean_direction": direction,
                }
                family_rows.append(record)
                pvalues.append(pvalue)
            for record, adjusted in zip(family_rows, holm_adjust(pvalues)):
                record["p_holm_within_family_horizon"] = format_float(adjusted)
                record["holm_significant_005"] = str(adjusted < 0.05).lower()
            output.extend(family_rows)
    return output


def compare_rows(observed: list[dict[str, str]], expected: list[dict[str, Any]], label: str) -> None:
    require(len(observed) == len(expected), f"{label} row count changed")
    for index, (left, right) in enumerate(zip(observed, expected), start=2):
        normalized = {name: str(value) for name, value in right.items()}
        require(left == normalized, f"{label} differs from independent recomputation at CSV row {index}")


def recompute_moving(contract: dict[str, Any]) -> list[dict[str, Any]]:
    archive_path = RESULT_DIR / "test_predictions_primary_mae.npz"
    try:
        archive = np.load(archive_path, allow_pickle=False)
    except (OSError, ValueError) as exc:
        fail(f"cannot read prediction archive: {exc}")
    block = contract["supplementary_moving_block_analysis"]
    contrasts = {
        item["id"]: item
        for family in contract["statistics"]["families"]
        for item in family["contrasts"]
    }
    output: list[dict[str, Any]] = []
    try:
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            expected_n = int(block["test_series_lengths"][str(horizon)])
            target_key = f"h{horizon}_target"
            require(target_key in archive.files, f"prediction archive lacks {target_key}")
            target = archive[target_key]
            require(target.shape == (expected_n,), f"target length changed for h={horizon}")
            for contrast_id in block["scope"]["contrasts"]:
                contrast = contrasts[contrast_id]
                per_seed: list[np.ndarray] = []
                for seed_index in range(10):
                    treatment_key = f"h{horizon}_seed{seed_index}_{contrast['treatment']}"
                    control_key = f"h{horizon}_seed{seed_index}_{contrast['control']}"
                    require(treatment_key in archive.files, f"prediction archive lacks {treatment_key}")
                    require(control_key in archive.files, f"prediction archive lacks {control_key}")
                    treatment = archive[treatment_key]
                    control = archive[control_key]
                    require(treatment.shape == (expected_n,), f"prediction length changed: {treatment_key}")
                    require(control.shape == (expected_n,), f"prediction length changed: {control_key}")
                    per_seed.append(np.abs(target - treatment) - np.abs(target - control))
                series = np.mean(np.stack(per_seed), axis=0)
                require(np.isfinite(series).all(), f"nonfinite hourly loss difference for {contrast_id} h={horizon}")
                for length in block["bootstrap"]["block_lengths"]:
                    repetitions = int(block["bootstrap"]["repetitions"])
                    rng_seed = int(block["bootstrap"]["rng_seeds"][f"h{horizon}_block{length}"])
                    n = len(series)
                    blocks_per_sample = math.ceil(n / int(length))
                    rng = np.random.Generator(np.random.PCG64(rng_seed))
                    bootstrap_means = np.empty(repetitions, dtype=np.float64)
                    offsets = np.arange(int(length), dtype=np.int64)
                    for start in range(0, repetitions, 250):
                        count = min(250, repetitions - start)
                        starts = rng.integers(0, n - int(length) + 1, size=(count, blocks_per_sample))
                        indices = (starts[:, :, None] + offsets[None, None, :]).reshape(count, -1)[:, :n]
                        bootstrap_means[start : start + count] = series[indices].mean(axis=1)
                    low, high = np.quantile(bootstrap_means, [0.025, 0.975], method="linear")
                    output.append(
                        {
                            "run_namespace": RUN_NAMESPACE,
                            "cap": "0.70",
                            "horizon_hours": horizon,
                            "selection_objective": "mae",
                            "contrast_id": contrast_id,
                            "block_length": length,
                            "repetitions": repetitions,
                            "rng": block["bootstrap"]["rng"],
                            "rng_seed": rng_seed,
                            "n_test_targets": expected_n,
                            "execution_status": "completed",
                            "unresampled_mean": format_float(float(series.mean())),
                            "percentile_2_5": format_float(float(low)),
                            "percentile_97_5": format_float(float(high)),
                            "interval_label": "descriptive moving-block sensitivity on one observed sequence",
                        }
                    )
    finally:
        archive.close()
    return output


def learned_gate(paired: list[dict[str, Any]], horizon: int) -> tuple[bool, str]:
    named = {
        row["contrast_id"]: row
        for row in paired
        if int(row["horizon_hours"]) == horizon
        and row["contrast_id"] in {"learned_retrieval_vs_raw", "learned_retrieval_vs_randomized"}
    }
    require(set(named) == {"learned_retrieval_vs_raw", "learned_retrieval_vs_randomized"}, f"learned controls incomplete at h={horizon}")
    licensed = all(
        row["execution_status"] == "completed"
        and row["mean_direction"] == "favorable"
        and row["holm_significant_005"] == "true"
        for row in named.values()
    )
    if licensed:
        wording = (
            f"At cap 0.70 and {horizon} h, learned k=8 retrieval had lower MAE than both named "
            "raw-feature and randomized-encoder k=8 controls across the ten frozen seed pairs; "
            "both contrasts were significant after within-family, within-horizon Holm adjustment."
        )
    else:
        wording = (
            f"At cap 0.70 and {horizon} h, no learned-space advantage claim is licensed; report each "
            "named raw-feature and randomized-encoder contrast with its observed direction and Holm result."
        )
    return licensed, wording


def paired_router(row: dict[str, Any], paired: list[dict[str, Any]]) -> tuple[str, str, str]:
    horizon = int(row["horizon_hours"])
    contrast_id = str(row["contrast_id"])
    if row["family_id"] == "onset_f1_diagnostic":
        return (
            "onset-inapplicable",
            "Diagnostic only: selection and calibration contained zero positive onsets; exact and Holm results do not cure objective inapplicability.",
            "onset benefit; supported no-effect conclusion; onset-targeted superiority",
        )
    if contrast_id in {"learned_retrieval_vs_raw", "learned_retrieval_vs_randomized"}:
        _, wording = learned_gate(paired, horizon)
        return (
            "learned-space",
            wording,
            "causal representation proof; overall forecasting superiority; cross-system or cross-year generalization",
        )
    adjusted = float(row["p_holm_within_family_horizon"])
    if row["mean_direction"] in {"null", "adverse"} or adjusted >= 0.05:
        if adjusted >= 0.05:
            wording = (
                "The named contrast was not resolved at alpha=0.05 after within-family, within-horizon Holm adjustment; "
                "retain the observed direction and interval without converting non-significance into a no-effect claim."
            )
        else:
            wording = (
                "The named treatment was adverse for this horizon and metric after within-family, within-horizon Holm adjustment; "
                "retain the adverse result without treating it as a protocol failure."
            )
        return (
            "null/adverse",
            wording,
            "overall winner; protocol failure; no-effect claim inferred only from non-significance",
        )
    return (
        "method-specific",
        "The favorable result is licensed only for this named treatment-control contrast, cap 0.70, horizon, metric, and ten-seed conditional analysis.",
        "overall architecture winner; overall forecasting superiority; deployment or transport claim",
    )


def paper_paired_rows(paired: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in paired:
        branch, wording, prohibited = paired_router(row, paired)
        output.append(
            {
                **row,
                "difference_definition": "treatment minus control",
                "seed_interval_label": "predeclared 95% t interval over ten frozen training seeds",
                "seed_interval_scope": "conditional on the seeds, fixed sequence, cap, horizon, protocol, and contrast; not hours, blocks, years, systems, policies, operators, or deployments",
                "holm_family_scope": f"{row['family_id']} within horizon {row['horizon_hours']} only",
                "wording_router_branch": branch,
                "licensed_interpretation": wording,
                "prohibited_extension": prohibited,
            }
        )
    return output


def paper_moving_rows(moving: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "analysis_scope": "conditional descriptive sensitivity on paired hourly loss differences from the single observed test sequence",
            "resampling_unit": "chronological series of the across-seed mean paired hourly absolute-loss difference",
            "decision_role": "does not enter Holm decisions and does not override the paired-seed analysis",
            "prohibited_extension": "confidence interval across years or systems; independent hourly replication; deployment evidence",
        }
        for row in moving
    ]


def deterministic_rows(run_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    keep = {"Persistence", "Seasonal-24h", "DirectPolicyTransform-Privileged", "Ridge"}
    selected = [
        row
        for row in run_rows
        if row["cap"] == "0.70"
        and row["seed_index"] == "deterministic"
        and row["condition_id"] in keep
    ]
    selected.sort(key=lambda row: (int(row["horizon_hours"]), row["selection_objective"], row["condition_id"]))
    output: list[dict[str, Any]] = []
    for row in selected:
        audit = row["condition_id"] == "DirectPolicyTransform-Privileged"
        output.append(
            {
                "run_namespace": RUN_NAMESPACE,
                "cap": row["cap"],
                "horizon_hours": row["horizon_hours"],
                "selection_objective": row["selection_objective"],
                "condition_id": row["condition_id"],
                "method_role": row["method_role"],
                "rank_eligible": row["rank_eligible"],
                "curtailment_mae": row["curtailment_mae"],
                "curtailment_rmse": row["curtailment_rmse"],
                "onset_f1": row["onset_f1"],
                "comparison_scope": "privileged construction/visibility audit; not a forecaster" if audit else "deterministic descriptive reference; no seed-based p-value",
                "wording_router_branch": "method-specific" if audit else "Persistence" if row["condition_id"] == "Persistence" else "method-specific",
            }
        )
    require(len(output) == 10, "primary-cap deterministic reference table must have 10 rows")
    return output


def cross_cap_rows(run_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for cap in ("0.60", "0.70", "0.80"):
        for horizon in (1, 24):
            treatment = [
                float(row["curtailment_mae"])
                for row in run_rows
                if row["cap"] == cap
                and int(row["horizon_hours"]) == horizon
                and row["selection_objective"] == "mae"
                and row["condition_id"] == "gru_learned_k8_selected_blend"
            ]
            require(len(treatment) == 10, f"selected learned rows incomplete for cap={cap}, h={horizon}")
            persistence = [
                row
                for row in run_rows
                if row["cap"] == cap
                and int(row["horizon_hours"]) == horizon
                and row["condition_id"] == "Persistence"
            ]
            require(len(persistence) == 1, f"Persistence row incomplete for cap={cap}, h={horizon}")
            selected_mean = float(np.mean(np.asarray(treatment, dtype=np.float64)))
            selected_sd = float(np.std(np.asarray(treatment, dtype=np.float64), ddof=1))
            persistence_mae = float(persistence[0]["curtailment_mae"])
            difference = selected_mean - persistence_mae
            output.append(
                {
                    "run_namespace": RUN_NAMESPACE,
                    "cap": cap,
                    "horizon_hours": horizon,
                    "selected_learned_mean_mae": format_float(selected_mean),
                    "selected_learned_seed_sd": format_float(selected_sd),
                    "persistence_mae": format_float(persistence_mae),
                    "selected_minus_persistence_mae": format_float(difference),
                    "descriptive_lower_mae_condition": "selected learned retrieval" if difference < 0 else "Persistence" if difference > 0 else "tie",
                    "comparison_scope": "descriptive comparison on the same fixed sequence; Persistence has no seed distribution or seed-based p-value; no cross-cap inference",
                    "wording_router_branch": "Persistence",
                }
            )
    return output


def router_rows(
    paired: list[dict[str, Any]], cross_cap: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for horizon in (1, 24):
        licensed, wording = learned_gate(paired, horizon)
        output.append(
            {
                "outcome_id": f"learned_space_joint_gate_h{horizon}",
                "wording_router_branch": "learned-space",
                "cap": "0.70",
                "horizon_hours": horizon,
                "source_family_or_table": "primary_mae_mechanism_attribution",
                "observed_state": "licensed_favorable" if licensed else "not_licensed_mixed_or_adverse",
                "licensed_wording": wording,
                "prohibited_wording": "learned-space advantage" if not licensed else "causal learned-representation proof or overall forecasting superiority",
                "scope": "joint gate over learned-versus-raw and learned-versus-randomized k=8 contrasts",
            }
        )
    for row in paired:
        branch, wording, prohibited = paired_router(row, paired)
        adjusted = float(row["p_holm_within_family_horizon"])
        output.append(
            {
                "outcome_id": f"{row['contrast_id']}_h{row['horizon_hours']}",
                "wording_router_branch": branch,
                "cap": "0.70",
                "horizon_hours": row["horizon_hours"],
                "source_family_or_table": row["family_id"],
                "observed_state": f"{row['mean_direction']}; holm_005={'yes' if adjusted < 0.05 else 'no'}",
                "licensed_wording": wording,
                "prohibited_wording": prohibited,
                "scope": "paired seed result; treatment minus control; exact sign-flip and Holm within frozen family and horizon",
            }
        )
    for row in cross_cap:
        output.append(
            {
                "outcome_id": f"selected_vs_persistence_cap{row['cap']}_h{row['horizon_hours']}",
                "wording_router_branch": "Persistence",
                "cap": row["cap"],
                "horizon_hours": row["horizon_hours"],
                "source_family_or_table": "v2_cross_cap_descriptive.csv",
                "observed_state": row["descriptive_lower_mae_condition"],
                "licensed_wording": "Report the observed MAE ordering as descriptive on the same fixed sequence, with no seed-based p-value for Persistence.",
                "prohibited_wording": "inferential superiority; cross-cap generalization; p-value for the deterministic reference",
                "scope": "deterministic/cross-cap descriptive branch",
            }
        )
    branches = {row["wording_router_branch"] for row in output}
    require(
        branches == {"learned-space", "method-specific", "null/adverse", "Persistence", "onset-inapplicable"},
        f"wording router did not exercise all frozen branches: {sorted(branches)}",
    )
    return output


def expected_artifacts() -> tuple[dict[Path, bytes], dict[str, Any]]:
    contract, manifest, source_provenance = verify_frozen_sources()
    run_rows = load_csv(RESULT_DIR / "run_results.csv")
    paired = recompute_paired(run_rows, contract)
    compare_rows(load_csv(RESULT_DIR / "paired_effects.csv"), paired, "sealed paired_effects.csv")
    moving = recompute_moving(contract)
    compare_rows(load_csv(RESULT_DIR / "moving_block_supplement.csv"), moving, "sealed moving_block_supplement.csv")

    cross_cap = cross_cap_rows(run_rows)
    rendered = {
        TABLE_PATHS["paired"]: csv_bytes(paper_paired_rows(paired)),
        TABLE_PATHS["moving"]: csv_bytes(paper_moving_rows(moving)),
        TABLE_PATHS["deterministic"]: csv_bytes(deterministic_rows(run_rows)),
        TABLE_PATHS["cross_cap"]: csv_bytes(cross_cap),
        TABLE_PATHS["router"]: csv_bytes(router_rows(paired, cross_cap)),
    }
    deriver_hash = sha256(Path(__file__))
    provenance = {
        "schema": "p1_ieee_access_upgrade_statistics_provenance",
        "schema_version": 1,
        "stage": STAGE_ID,
        "run_namespace": RUN_NAMESPACE,
        "source_manifest_status": manifest["status"],
        "source_protocol_valid": manifest["protocol_valid"],
        "no_experiment_rerun": True,
        "derivation": {
            "statistics_deriver_path": Path(__file__).relative_to(PROJECT_ROOT).as_posix(),
            "statistics_deriver_working_sha256": deriver_hash,
            "paired_effects": "independently recomputed from sealed run_results.csv using all 2^10 sign assignments, the frozen t critical value, and Holm within each family and horizon",
            "moving_block": "independently recomputed from sealed primary-cap prediction archive using paired hourly absolute-loss differences, 5000 PCG64 repetitions, and frozen block lengths/seeds",
            "wording_router": "frozen contract claim gates applied after numerical recomputation without changing the protocol",
        },
        "source_provenance": source_provenance,
        "paper_tables": {
            path.relative_to(PROJECT_ROOT).as_posix(): {"sha256": sha256_bytes(value), "bytes": len(value)}
            for path, value in sorted(rendered.items(), key=lambda item: item[0].as_posix())
        },
        "scope_boundaries": {
            "seed_intervals": "training-seed conditional only",
            "moving_block_intervals": "conditional descriptive sensitivity on one observed sequence",
            "deterministic_references": "descriptive; no seed-based p-value",
            "cross_cap": "descriptive on the same fixed sequence",
            "onset": "diagnostic only because pre-test positive onset support is absent",
        },
    }
    rendered[PROVENANCE_PATH] = (json.dumps(provenance, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return rendered, provenance


def generate() -> dict[str, Any]:
    rendered, provenance = expected_artifacts()
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    for path, value in rendered.items():
        path.write_bytes(value)
    return provenance


def check_statistics_artifacts() -> dict[str, Any]:
    rendered, provenance = expected_artifacts()
    for path, expected in rendered.items():
        require(path.is_file(), f"Stage-3 artifact missing: {path.relative_to(PROJECT_ROOT)}")
        require(path.read_bytes() == expected, f"Stage-3 artifact is stale or altered: {path.relative_to(PROJECT_ROOT)}")
    return {
        "paired_rows": 30,
        "moving_block_rows": 36,
        "paper_tables": len(TABLE_PATHS),
        "provenance_schema": provenance["schema"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify existing artifacts without writing")
    args = parser.parse_args(argv)
    summary = check_statistics_artifacts() if args.check else generate()
    print(
        f"OK {RUN_NAMESPACE}: Stage-3 statistics {'verified' if args.check else 'generated'}; "
        "paired=30; moving_block=36; paper_tables=5; provenance=committed-blob-aware"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
