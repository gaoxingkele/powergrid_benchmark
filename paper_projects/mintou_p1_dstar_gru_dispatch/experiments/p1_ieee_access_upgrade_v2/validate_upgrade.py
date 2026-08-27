#!/usr/bin/env python3
"""Fail-closed validator for the P1 IEEE Access v2 contract and execution."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
CONTRACT_PATH = HERE / "upgrade_contract.json"
PROSE_PATH = HERE / "PROSPECTIVE_CONTRACT.md"
CITATION_REPORT_PATH = PROJECT_ROOT / "P1_CITATION_VERIFICATION_V2.md"
LITERATURE_GAP_PATH = PROJECT_ROOT / "P1_LITERATURE_GAP_V2.md"
MANUSCRIPT_PATH = PROJECT_ROOT / "manuscript" / "MANUSCRIPT.md"
PAPER_TEX_PATH = PROJECT_ROOT / "manuscript" / "journal_submission" / "paper.tex"
PAPER_PDF_PATH = PAPER_TEX_PATH.with_suffix(".pdf")
FIGURE_DIR = PROJECT_ROOT / "manuscript" / "figures"
FIGURE_MANIFEST_PATH = FIGURE_DIR / "artifact_manifest.json"


def fail(message: str) -> None:
    raise SystemExit(f"CONTRACT INVALID: {message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def require_equal(actual: Any, expected: Any, label: str) -> None:
    if actual != expected:
        fail(f"{label}: expected {expected!r}, found {actual!r}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_contract() -> dict[str, Any]:
    require(CONTRACT_PATH.is_file(), f"normative JSON missing: {CONTRACT_PATH}")
    try:
        value = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse normative JSON: {exc}")
    require(isinstance(value, dict), "normative JSON root must be an object")
    return value


def validate_identity(contract: dict[str, Any]) -> None:
    require_equal(contract.get("schema"), "p1_ieee_access_upgrade_contract", "schema")
    require_equal(contract.get("schema_version"), 1, "schema_version")
    require_equal(contract.get("run_namespace"), "p1_ieee_access_upgrade_v2", "run_namespace")
    require_equal(
        contract.get("status"),
        "prospectively_frozen_before_v2_execution",
        "status",
    )
    phase = contract.get("contract_phase", {})
    require_equal(phase.get("approved_stage"), "p1v4_s1_upgrade_contract", "approved stage")
    require_equal(
        phase.get("results_visibility"),
        "v2_results_must_not_exist_or_be_inspected_in_this_stage",
        "results visibility",
    )
    require_equal(
        set(phase.get("allowed_outputs", [])),
        {"PROSPECTIVE_CONTRACT.md", "upgrade_contract.json", "validate_upgrade.py"},
        "contract-stage allowed outputs",
    )


def validate_preserved_maps(contract: dict[str, Any], *, require_frozen_hashes: bool = True) -> None:
    preserved = contract.get("preserved_evidence_maps", {})
    artifacts = preserved.get("artifacts")
    require(isinstance(artifacts, list) and len(artifacts) == 3, "three preserved evidence-map artifacts required")
    expected_roles = {
        "manuscript/MANUSCRIPT.md": {
            "title",
            "abstract",
            "contributions",
            "research_questions",
            "discussion",
            "conclusion",
        },
        "manuscript/TABLE_TO_CONFIG_MANIFEST.md": {
            "figures",
            "tables",
            "negative_and_null_results",
        },
        "manuscript/DEEP_REVISION_EVIDENCE.md": {
            "title_to_evidence",
            "estimand",
            "comparison_budget",
            "negative_and_null_results",
            "human_blockers",
        },
    }
    seen: set[str] = set()
    for artifact in artifacts:
        require(isinstance(artifact, dict), "preserved artifact entry must be an object")
        relative = artifact.get("path")
        require(relative in expected_roles, f"unexpected preserved artifact: {relative!r}")
        require(relative not in seen, f"duplicate preserved artifact: {relative}")
        seen.add(relative)
        require_equal(set(artifact.get("map_roles", [])), expected_roles[relative], f"map roles for {relative}")
        path = PROJECT_ROOT / relative
        require(path.is_file(), f"preserved evidence artifact missing: {relative}")
        if require_frozen_hashes:
            require_equal(sha256(path), artifact.get("sha256"), f"preserved evidence hash for {relative}")
    require_equal(seen, set(expected_roles), "preserved evidence paths")

    manuscript = (PROJECT_ROOT / "manuscript" / "MANUSCRIPT.md").read_text(encoding="utf-8")
    for token in (
        "# A Reproducible Retrospective Curtailment-Risk Benchmark",
        "## Abstract",
        "**RQ1:**",
        "**RQ2:**",
        "**RQ3:**",
        "The contributions follow those questions:",
        "## IX. Conclusion",
        "AUTHOR INPUT REQUIRED",
    ):
        require(token in manuscript, f"preserved manuscript marker missing: {token}")

    matrix = (PROJECT_ROOT / "manuscript" / "DEEP_REVISION_EVIDENCE.md").read_text(encoding="utf-8")
    for heading in (
        "# Title-to-Evidence Map",
        "# Primary Estimand and Analysis Unit",
        "# Comparison Budget and Data Visibility",
        "# Negative and Null Results",
        "# Shared Assets and Independent Contribution",
        "# New or Rerun Experiments",
        "# Unresolved Human Blockers",
    ):
        require(heading in matrix, f"required revision-evidence heading missing: {heading}")
    require("AUTHOR INPUT REQUIRED" in matrix, "human blockers were removed from the evidence matrix")
    require(
        "Do not add, remove, resolve, or infer" in preserved.get("human_metadata_rule", ""),
        "human metadata must remain explicitly untouched",
    )


def validate_scope(contract: dict[str, Any]) -> None:
    scope = contract.get("scope", {})
    source = scope.get("source_sequence", {})
    require_equal(source.get("evaluated_rows"), 8760, "evaluated source rows")
    require_equal(source.get("source_rows"), 8784, "available source rows")
    require_equal(source.get("last_delivery_key"), "2020-12-30 period 24", "last delivery key")
    require(source.get("complete_calendar_year") is False, "complete-year boundary must be false")
    require_equal(source.get("systems"), 1, "system count")
    require_equal(source.get("sequences"), 1, "sequence count")

    expected_hashes = {
        "load": "6efb6e3e06f7f1cee0d59eaf33768e06c33c737beb875676433850d8659943ee",
        "wind": "b933f810511ce3d2128c490e4b230defcdc3c15ed4db0838c6fd4c62640e2208",
        "pv": "bfede6e558df5ea0f244b6326940a4ee0b95138643aa8a062897c67134c9c185",
        "branch": "2f8f80f6f95ca46c2997646d56892436b50d7fb81163b680d06767bc3c1b179f",
    }
    files = scope.get("source_files", {})
    require_equal(set(files), set(expected_hashes), "source-file identities")
    for name, expected_hash in expected_hashes.items():
        require_equal(files[name].get("sha256"), expected_hash, f"source hash {name}")

    info = scope.get("information_boundary", {})
    for field in (
        "forecast_issue_timestamps_available",
        "as_of_mapping_available",
        "release_identifier_available",
        "data_vintage_available",
    ):
        require(info.get(field) is False, f"information boundary must keep {field}=false")
    target = scope.get("target", {})
    require(target.get("method_independent") is True, "target must remain method independent")
    for field in (
        "observed_curtailment",
        "operator_action",
        "opf_or_unit_commitment_output",
        "economic_outcome",
    ):
        require(target.get(field) is False, f"proxy boundary must keep {field}=false")
    features = scope.get("features", {})
    require_equal(features.get("window_rows"), 48, "window length")
    require_equal(features.get("count"), 7, "feature count")
    require_equal(len(features.get("ordered_names", [])), 7, "ordered feature-name count")


def validate_grid_and_temporal(contract: dict[str, Any]) -> None:
    grid = contract.get("experimental_grid", {})
    require_equal(grid.get("caps"), [0.6, 0.7, 0.8], "caps")
    require_equal(grid.get("cap_execution_order"), [0.7, 0.6, 0.8], "cap execution order")
    require_equal(grid.get("primary_cap"), 0.7, "primary cap")
    require("descriptive only" in grid.get("cross_cap_interpretation", ""), "cross-cap scope must be descriptive")
    require_equal(grid.get("horizons_hours"), [1, 24], "horizons")
    require_equal(grid.get("selection_objectives"), ["mae", "onset_f1"], "selection objectives")
    seeds = [11, 23, 47, 59, 71, 83, 97, 109, 127, 139]
    require_equal(grid.get("common_seeds"), seeds, "common seeds")

    temporal = contract.get("temporal_protocol", {})
    require_equal(temporal.get("total_rows"), 8760, "temporal total rows")
    require_equal(temporal.get("query_window_rows"), 48, "temporal window")
    boundaries = temporal.get("phase_boundaries", {})
    require_equal(
        boundaries,
        {
            "fit_end_exclusive": 4380,
            "selection_end_exclusive": 5256,
            "calibration_end_exclusive": 6132,
            "test_end_exclusive": 8760,
        },
        "phase boundaries",
    )
    per_horizon = temporal.get("per_horizon", {})
    require_equal(set(per_horizon), {"1", "24"}, "per-horizon partition keys")
    for horizon in (1, 24):
        value = per_horizon[str(horizon)]
        first_target = 47 + horizon
        expected_ranges = {
            "fit": [first_target, 4380],
            "selection": [4380 + horizon, 5256],
            "calibration": [5256 + horizon, 6132],
            "test": [6132 + horizon, 8760],
        }
        require_equal(value.get("first_target_inclusive"), first_target, f"h{horizon} first target")
        for phase, expected_range in expected_ranges.items():
            require_equal(value.get(phase), expected_range, f"h{horizon} {phase} range")
        expected_embargo = [
            [4380, 4380 + horizon],
            [5256, 5256 + horizon],
            [6132, 6132 + horizon],
        ]
        require_equal(value.get("embargo_target_ranges"), expected_embargo, f"h{horizon} embargo ranges")
        counts = {name: stop - start for name, (start, stop) in expected_ranges.items()}
        counts["embargoed"] = 3 * horizon
        counts["all_constructed_targets"] = 8760 - first_target
        require_equal(value.get("counts"), counts, f"h{horizon} phase counts")
        require_equal(
            sum(counts[name] for name in ("fit", "selection", "calibration", "test")) + counts["embargoed"],
            counts["all_constructed_targets"],
            f"h{horizon} partition accounting",
        )
    uses = temporal.get("allowed_uses", {})
    require_equal(uses.get("calibration"), ["detection threshold only"], "calibration use")
    require_equal(uses.get("test"), ["single final scoring pass only"], "test use")


def validate_architectures_and_budget(contract: dict[str, Any]) -> None:
    architectures = contract.get("architectures", {})
    require_equal(set(architectures) - {"common_input_shape", "comparison_boundary"}, {"GRU", "LSTM", "DLinear", "TCN"}, "architecture set")
    require_equal(architectures.get("common_input_shape"), [48, 7], "common input shape")
    for recurrent in ("GRU", "LSTM"):
        spec = architectures[recurrent]
        require_equal(spec.get("layers"), 1, f"{recurrent} layers")
        require_equal(spec.get("hidden_size"), 48, f"{recurrent} hidden size")
        require(spec.get("bidirectional") is False, f"{recurrent} must be unidirectional")
        require_equal(spec.get("dropout"), 0.0, f"{recurrent} dropout")
    dlinear = architectures["DLinear"]
    require_equal(dlinear.get("moving_average_kernel"), 25, "DLinear moving-average kernel")
    require("Linear(48, 1)" in dlinear.get("temporal_maps", ""), "DLinear temporal maps not frozen")
    tcn = architectures["TCN"]
    require_equal(tcn.get("channels"), [48, 48], "TCN channels")
    require_equal(tcn.get("kernel_size"), 3, "TCN kernel")
    require_equal(tcn.get("dilations"), [1, 2], "TCN dilations")
    require_equal(tcn.get("convolutions_per_block"), 2, "TCN convolutions per block")
    require("not parameter-count matched" in architectures.get("comparison_boundary", ""), "architecture fairness boundary missing")

    budget = contract.get("common_training_budget", {})
    expected_budget = {
        "epochs": 20,
        "checkpoint_epochs": [5, 10, 15, 20],
        "batch_size": 256,
        "learning_rate": 0.001,
        "beta1": 0.9,
        "beta2": 0.999,
        "epsilon": 1e-8,
        "weight_decay": 0.0,
        "gradient_clipping": None,
        "training_trajectories": 240,
    }
    for field, expected in expected_budget.items():
        require_equal(budget.get(field), expected, f"training budget {field}")
    require(budget.get("fit_partition_only") is True, "training must be fit-only")

    selection = contract.get("selection_and_scoring", {})
    require_equal(selection.get("blend_alpha_grid_order"), [1.0, 0.8, 0.6, 0.5, 0.4, 0.2, 0.0], "alpha grid")
    require_equal(selection.get("reported_prediction_clip"), [0.0, 1.0], "prediction clip")
    require_equal(selection.get("tie_tolerance"), 1e-15, "selection tie tolerance")
    require("No test metric" in selection.get("test_visibility", ""), "test visibility fail-closed rule missing")


def validate_baselines_retrieval_and_onset(contract: dict[str, Any]) -> None:
    controls = contract.get("baselines_and_controls", {})
    require_equal(
        set(controls),
        {"Ridge", "Persistence", "Seasonal-24h", "DirectPolicyTransform-Privileged"},
        "baseline/control set",
    )
    require_equal(controls["Ridge"].get("penalties_order"), [1e-6, 1e-4, 1e-3, 1e-2, 1e-1, 1.0, 10.0], "Ridge penalties")
    require(controls["Ridge"].get("intercept") is False, "Ridge intercept must remain disabled")
    require(controls["DirectPolicyTransform-Privileged"].get("rank_as_forecaster") is False, "privileged control must not be ranked")

    retrieval = contract.get("retrieval", {})
    require_equal(retrieval.get("k_values"), [4, 8, 16, 32], "retrieval k values")
    require_equal(retrieval.get("primary_k"), 8, "primary k")
    spaces = retrieval.get("spaces", {})
    require_equal(set(spaces), {"learned", "raw", "randomized"}, "retrieval spaces")
    require_equal(spaces["randomized"].get("training_updates"), 0, "randomized encoder updates")
    gate = retrieval.get("learned_space_attribution_gate", "")
    require("learned-versus-raw" in gate and "learned-versus-randomized" in gate, "both learned-space attribution controls must be gates")

    onset = contract.get("onset_protocol", {})
    require_equal(onset.get("calibration_quantiles"), 40, "onset threshold quantiles")
    require_equal(onset.get("zero_positive_fallback_threshold"), 0.02, "onset fallback threshold")
    require_equal(onset.get("zero_positive_status"), "fallback_no_positive_onsets", "onset fallback status")
    inapplicable = onset.get("onset_inapplicable_rule", "")
    require("not execution failure" in inapplicable and "not proof of no effect" in inapplicable, "onset inapplicability boundary missing")


def validate_rows_and_failures(contract: dict[str, Any]) -> set[str]:
    catalog = contract.get("seeded_condition_catalog")
    require(isinstance(catalog, list), "seeded condition catalog must be a list")
    require_equal(len(catalog), 19, "seeded condition count")
    ids = [row.get("id") for row in catalog if isinstance(row, dict)]
    require_equal(len(ids), 19, "seeded condition entries")
    require_equal(len(set(ids)), 19, "unique seeded condition ids")
    id_set = set(ids)
    require_equal({f"{name}_head" for name in ("gru", "lstm", "dlinear", "tcn")}.issubset(id_set), True, "architecture-head conditions")
    for space, prefix in (("learned", "gru_learned"), ("raw", "raw"), ("randomized", "gru_randomized")):
        for k in (4, 8, 16, 32):
            condition_id = f"{prefix}_k{k}_retrieval"
            require(condition_id in id_set, f"missing {space} k={k} retrieval condition")
    for condition_id in (
        "gru_learned_k8_selected_blend",
        "gru_learned_k8_fixed_0_5",
        "gru_learned_k8_fixed_1",
    ):
        require(condition_id in id_set, f"missing learned-space blend condition: {condition_id}")

    row_contract = contract.get("row_contract", {})
    caps = len(contract["experimental_grid"]["caps"])
    horizons = len(contract["experimental_grid"]["horizons_hours"])
    objectives = len(contract["experimental_grid"]["selection_objectives"])
    seeds = len(contract["experimental_grid"]["common_seeds"])
    seeded = caps * horizons * objectives * seeds * len(catalog)
    deterministic = caps * horizons * 3
    ridge = caps * horizons * objectives
    total = seeded + deterministic + ridge
    require_equal(seeded, 2280, "derived seeded row count")
    require_equal(deterministic, 18, "derived deterministic row count")
    require_equal(ridge, 12, "derived Ridge row count")
    require_equal(total, 2310, "derived total row count")
    expected_counts = {
        "seeded_conditions_per_objective_seed_task": 19,
        "seeded_rows": seeded,
        "objective_free_deterministic_conditions_per_task": 3,
        "objective_free_deterministic_rows": deterministic,
        "objective_specific_ridge_rows": ridge,
        "total_rows": total,
        "primary_cap_rows": 770,
        "sensitivity_cap_rows": 1540,
        "per_cap_horizon_rows": 385,
    }
    for field, expected in expected_counts.items():
        require_equal(row_contract.get(field), expected, f"row contract {field}")
    require_equal(
        row_contract.get("objective_free_deterministic_ids"),
        ["DirectPolicyTransform-Privileged", "Persistence", "Seasonal-24h"],
        "objective-free deterministic conditions",
    )
    required_columns = set(row_contract.get("required_execution_columns", []))
    for column in (
        "execution_status",
        "scientific_support_status",
        "failure_code",
        "n_onsets_selection",
        "n_onsets_calibration",
    ):
        require(column in required_columns, f"required execution column missing: {column}")

    handling = contract.get("failure_handling", {})
    expected_statuses = {
        "completed",
        "failed_exception",
        "failed_nonfinite",
        "failed_resource",
        "failed_integrity",
    }
    require_equal(set(handling.get("allowed_execution_statuses", [])), expected_statuses, "execution status vocabulary")
    for field in (
        "seed_replacement",
        "architecture_substitution",
        "metric_imputation",
        "result_triggered_retry",
        "batch_size_fallback",
        "tuning_after_failure",
    ):
        require(handling.get(field) is False, f"failure handling must freeze {field}=false")
    require("favorable, null, mixed, or adverse" in handling.get("effect_direction_separation", ""), "valid effects must be separated from protocol status")
    require("not execution failures" in handling.get("onset_separation", ""), "onset fallback must not be an execution failure")
    return id_set


def validate_statistics(contract: dict[str, Any], condition_ids: set[str]) -> set[str]:
    statistics = contract.get("statistics", {})
    require_equal(statistics.get("primary_cap"), 0.7, "statistics primary cap")
    require_equal(statistics.get("primary_k"), 8, "statistics primary k")
    require_equal(statistics.get("complete_pairs_required"), 10, "complete paired seeds")
    sign_flip = statistics.get("exact_sign_flip", {})
    require_equal(sign_flip.get("sidedness"), "two-sided", "sign-flip sidedness")
    require("all 2^10 sign assignments" in sign_flip.get("enumeration", ""), "exact sign enumeration missing")
    require(sign_flip.get("continuity_or_plus_one_correction") is False, "sign-flip plus-one correction must be false")
    interval = statistics.get("seed_conditional_interval", {})
    require_equal(interval.get("confidence_level"), 0.95, "seed interval level")
    require(math.isclose(interval.get("critical_value", 0.0), 2.2621571627409915, rel_tol=0.0, abs_tol=1e-15), "seed interval critical value")
    require("not uncertainty over hours" in interval.get("scope", ""), "seed interval scope boundary missing")
    holm = statistics.get("holm", {})
    require("separately for each family_id and horizon" in holm.get("family_partition", ""), "Holm family partition missing")
    require_equal(holm.get("alpha"), 0.05, "Holm alpha")

    families = statistics.get("families")
    require(isinstance(families, list), "statistical families must be a list")
    expected = {
        "primary_mae_mechanism_attribution": ("mae", "curtailment_mae", "lower", 6),
        "architecture_head_mae": ("mae", "curtailment_mae", "lower", 3),
        "onset_f1_diagnostic": ("onset_f1", "onset_f1", "higher", 6),
    }
    require_equal({family.get("family_id") for family in families}, set(expected), "statistical family ids")
    contrast_ids: set[str] = set()
    for family in families:
        family_id = family["family_id"]
        objective, metric, direction, count = expected[family_id]
        require_equal(family.get("selection_objective"), objective, f"{family_id} objective")
        require_equal(family.get("metric"), metric, f"{family_id} metric")
        require_equal(family.get("better_direction"), direction, f"{family_id} direction")
        contrasts = family.get("contrasts", [])
        require_equal(len(contrasts), count, f"{family_id} contrast count")
        for contrast in contrasts:
            contrast_id = contrast.get("id")
            require(contrast_id not in contrast_ids, f"duplicate contrast id: {contrast_id}")
            contrast_ids.add(contrast_id)
            require(contrast.get("treatment") in condition_ids, f"unknown treatment in {contrast_id}")
            require(contrast.get("control") in condition_ids, f"unknown control in {contrast_id}")

    required_attribution = {"learned_retrieval_vs_raw", "learned_retrieval_vs_randomized"}
    require(required_attribution.issubset(contrast_ids), "both learned-space attribution contrasts are required")
    for contrast_id in ("gru_head_vs_lstm_head", "gru_head_vs_dlinear_head", "gru_head_vs_tcn_head"):
        require(contrast_id in contrast_ids, f"architecture contrast missing: {contrast_id}")
    descriptive = " ".join(statistics.get("descriptive_only", []))
    for token in ("cross-cap", "k=4/16/32", "Persistence", "onset-family"):
        require(token in descriptive, f"descriptive-only scope missing: {token}")
    return contrast_ids


def validate_moving_block(contract: dict[str, Any], contrast_ids: set[str]) -> None:
    block = contract.get("supplementary_moving_block_analysis", {})
    require_equal(block.get("status"), "required supplementary descriptive analysis", "moving-block status")
    scope = block.get("scope", {})
    require_equal(scope.get("cap"), 0.7, "moving-block cap")
    require_equal(scope.get("selection_objective"), "mae", "moving-block objective")
    expected_contrasts = [
        "selected_learned_vs_gru_head",
        "learned_retrieval_vs_gru_head",
        "fixed_half_vs_gru_head",
        "learned_retrieval_vs_fixed_half",
        "learned_retrieval_vs_raw",
        "learned_retrieval_vs_randomized",
        "gru_head_vs_lstm_head",
        "gru_head_vs_dlinear_head",
        "gru_head_vs_tcn_head",
    ]
    require_equal(scope.get("contrasts"), expected_contrasts, "moving-block contrast order")
    require(set(expected_contrasts).issubset(contrast_ids), "moving-block references unknown contrasts")
    loss = block.get("loss_series", "")
    for token in ("abs(y_t-clipped_prediction_treatment", "abs(y_t-clipped_prediction_control", "ten common seeds"):
        require(token in loss, f"moving-block loss series missing: {token}")
    require_equal(block.get("test_series_lengths"), {"1": 2627, "24": 2604}, "moving-block series lengths")
    bootstrap = block.get("bootstrap", {})
    require_equal(bootstrap.get("block_lengths"), [24, 168], "moving-block lengths")
    require_equal(bootstrap.get("repetitions"), 5000, "moving-block repetitions")
    require_equal(bootstrap.get("rng"), "NumPy Generator(PCG64)", "moving-block RNG")
    require(bootstrap.get("reset_for_each_contrast") is True, "moving-block RNG must reset per contrast")
    require(bootstrap.get("common_resamples_across_contrasts") is True, "moving-block resamples must be common across contrasts")
    require_equal(
        bootstrap.get("rng_seeds"),
        {
            "h1_block24": 610024,
            "h1_block168": 610168,
            "h24_block24": 624024,
            "h24_block168": 624168,
        },
        "moving-block RNG seeds",
    )
    require("n-L+1" in bootstrap.get("construction", ""), "moving-block overlapping construction missing")
    interpretation = block.get("interpretation", "")
    for token in ("descriptive sensitivity", "single observed test sequence", "do not use them for Holm"):
        require(token in interpretation, f"moving-block interpretation boundary missing: {token}")


def validate_claim_gates(contract: dict[str, Any]) -> None:
    validity = contract.get("validity_and_interpretation", {})
    protocol = validity.get("protocol_validity", {})
    not_required = set(protocol.get("does_not_require", []))
    for item in (
        "positive effect",
        "statistical significance",
        "GRU superiority",
        "retrieval superiority",
        "learned-space superiority",
        "beating Persistence",
        "applicable onset selection",
    ):
        require(item in not_required, f"protocol validity improperly depends on: {item}")
    bounded = validity.get("bounded_benchmark_contribution", "")
    require("complete valid null, mixed, or adverse result" in bounded, "bounded benchmark contribution must retain valid null/adverse results")
    scopes = set(validity.get("scope_boundaries", []))
    for token in (
        "proxy rather than observed curtailment",
        "retrospective delivery-row lags rather than operational forecasts",
        "one truncated 8760-row sequence rather than a complete year",
        "no OPF/UC, operator, deployment, safety, or economic validation",
        "combined ablations support joint conclusions only",
    ):
        require(token in scopes, f"scope boundary missing: {token}")

    gates = contract.get("claim_gates", {})
    require(gates.get("benchmark_contribution", {}).get("favorable_model_comparisons_required") is False, "benchmark gate must not require favorable comparisons")
    learned = gates.get("learned_space_attribution", {})
    require_equal(
        learned.get("required_named_controls"),
        ["raw-feature kNN attribution control", "randomized-encoder retrieval attribution control"],
        "named learned-space attribution controls",
    )
    require(learned.get("head_only_comparison_sufficient") is False, "head-only comparison cannot license learned-space wording")
    architecture = gates.get("architecture_superiority", {})
    require(architecture.get("overall_winner_wording") is False, "overall architecture-winner wording must be disabled")
    require(architecture.get("benchmark_gate") is False, "architecture superiority must not gate benchmark contribution")
    clear = gates.get("ieee_access_clear_advance", {})
    require_equal(
        clear.get("requires"),
        ["complete protocol-valid v2 evidence", "Stage-4 verified literature positioning of the auditable benchmark"],
        "IEEE Access clear-advance requirements",
    )
    clear_not_required = set(clear.get("does_not_require", []))
    require("every model comparison favorable" in clear_not_required, "clear advance must not require every favorable comparison")
    require("valid null or adverse method result" in clear.get("failed_effect_rule", ""), "clear-advance null/adverse rule missing")


def validate_prose() -> None:
    require(PROSE_PATH.is_file(), f"prospective contract prose missing: {PROSE_PATH}")
    text = PROSE_PATH.read_text(encoding="utf-8")
    for heading in (
        "# Prospective IEEE Access Upgrade Contract",
        "## 1. Evidence and claim boundary",
        "## 2. Frozen task grid and temporal gate",
        "## 3. Architectures and common budget",
        "## 4. Baselines, retrieval spaces, and k sensitivity",
        "## 5. Complete row contract and failures",
        "## 6. Paired effects, exact tests, and seed interval",
        "## 7. Supplementary moving-block analysis",
        "## 8. Validity and IEEE Access interpretation gate",
    ):
        require(heading in text, f"prospective contract heading missing: {heading}")
    for token in (
        "No v2 result",
        "**2310 rows**",
        "610024",
        "624168",
        "Stage-4 verified literature positioning",
        "does not require every model comparison to be favorable",
        "Human metadata is outside this stage",
    ):
        require(token in text, f"prospective contract statement missing: {token}")


def validate_contract_stage_absence(contract: dict[str, Any]) -> None:
    future = contract.get("future_artifact_contract", {})
    required_contract_files = {
        "experiments/p1_ieee_access_upgrade_v2/PROSPECTIVE_CONTRACT.md",
        "experiments/p1_ieee_access_upgrade_v2/upgrade_contract.json",
        "experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py",
    }
    require_equal(set(future.get("contract_stage_files", [])), required_contract_files, "required contract-stage files")
    for relative in required_contract_files:
        require((PROJECT_ROOT / relative).is_file(), f"required contract-stage file missing: {relative}")

    # Check existence only. Do not enumerate or open any forbidden execution path.
    forbidden = (
        HERE / "results",
        HERE / "run_upgrade.py",
        HERE / "run_manifest.json",
    )
    for path in forbidden:
        require(not path.exists(), f"v2 execution artifact must be absent in contract phase: {path.name}")
    allowed_names = {"PROSPECTIVE_CONTRACT.md", "upgrade_contract.json", "validate_upgrade.py"}
    actual_names = {path.name for path in HERE.iterdir()}
    require_equal(actual_names, allowed_names, "files present in contract namespace")


def validate_contract(
    *,
    require_contract_stage_absence: bool,
    require_preserved_map_hashes: bool = True,
) -> dict[str, Any]:
    contract = load_contract()
    validate_identity(contract)
    validate_preserved_maps(contract, require_frozen_hashes=require_preserved_map_hashes)
    validate_scope(contract)
    validate_grid_and_temporal(contract)
    validate_architectures_and_budget(contract)
    validate_baselines_retrieval_and_onset(contract)
    condition_ids = validate_rows_and_failures(contract)
    contrast_ids = validate_statistics(contract, condition_ids)
    validate_moving_block(contract, contrast_ids)
    validate_claim_gates(contract)
    validate_prose()
    if require_contract_stage_absence:
        validate_contract_stage_absence(contract)
    return contract


def load_csv(path: Path) -> list[dict[str, str]]:
    require(path.is_file(), f"execution table missing: {path.relative_to(PROJECT_ROOT)}")
    try:
        with path.open(encoding="utf-8", errors="strict", newline="") as handle:
            rows = list(csv.DictReader(handle))
    except (OSError, UnicodeError, csv.Error) as exc:
        fail(f"cannot read execution table {path.name}: {exc}")
    require(rows, f"execution table is empty: {path.name}")
    return rows


def finite_field(row: dict[str, str], field: str, label: str) -> float:
    value = row.get(field, "")
    require(value != "", f"{label} has null {field}")
    try:
        number = float(value)
    except ValueError:
        fail(f"{label} has invalid {field}: {value!r}")
    require(math.isfinite(number), f"{label} has nonfinite {field}")
    return number


def validate_execution(contract: dict[str, Any]) -> dict[str, Any]:
    future = contract["future_artifact_contract"]
    for relative in future["contract_stage_files"] + future["later_execution_files"]:
        require((PROJECT_ROOT / relative).is_file(), f"required execution artifact missing: {relative}")
    required_extras = (
        HERE / "results" / "trajectory_ledger.csv",
        HERE / "results" / "completeness_ledger.csv",
        HERE / "results" / "failure_ledger.csv",
        HERE / "results" / "test_predictions_primary_mae.npz",
        HERE / "logs" / "run.log",
    )
    for path in required_extras:
        require(path.is_file(), f"required audit artifact missing: {path.relative_to(PROJECT_ROOT)}")
    require(not (HERE / "results" / "run_results.partial.csv").exists(), "partial result table remains after sealing")
    require(not (HERE / "results" / "trajectory_ledger.partial.csv").exists(), "partial trajectory table remains after sealing")

    manifest_path = HERE / "run_manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse execution manifest: {exc}")
    require_equal(manifest.get("schema"), "p1_ieee_access_upgrade_execution_manifest", "execution manifest schema")
    require_equal(manifest.get("schema_version"), 1, "execution manifest schema version")
    require_equal(manifest.get("run_namespace"), contract["run_namespace"], "execution namespace")
    require_equal(manifest.get("approved_stage"), "p1v4_s2_fair_baselines_attribution", "execution stage")
    require_equal(manifest.get("status"), "completed", "execution manifest status")
    require(manifest.get("protocol_valid") is True, "manifest protocol_valid must be true")
    require_equal(manifest.get("contract", {}).get("sha256"), sha256(CONTRACT_PATH), "manifest contract hash")
    runner = HERE / "run_upgrade.py"
    require_equal(manifest.get("script", {}).get("sha256"), sha256(runner), "manifest runner hash")
    require_equal(
        manifest.get("parameter_counts"),
        {"GRU": 8257, "LSTM": 10993, "DLinear": 106, "TCN": 28273, "randomized_GRU_encoder": 8208},
        "parameter counts",
    )
    environment = manifest.get("environment", {})
    for field in ("python", "platform", "numpy", "torch", "device", "cudnn_deterministic", "cudnn_benchmark"):
        require(field in environment, f"environment field missing: {field}")
    require(environment.get("cudnn_deterministic") is True, "cuDNN deterministic flag not recorded")
    require(environment.get("cudnn_benchmark") is False, "cuDNN benchmark must be false")
    source_profile = manifest.get("source_profile", {})
    for name, source in contract["scope"]["source_files"].items():
        observed = source_profile.get("source_files", {}).get(name, {})
        require_equal(observed.get("sha256"), source["sha256"], f"executed source hash {name}")
        require(int(observed.get("bytes", 0)) > 0, f"executed source size missing: {name}")
    require_equal(source_profile.get("first_delivery_key"), [2020, 1, 1, 1], "first executed delivery key")
    require_equal(source_profile.get("last_delivery_key"), [2020, 12, 30, 24], "last executed delivery key")

    output_index = manifest.get("outputs", {})
    result_files = sorted(path for path in (HERE / "results").iterdir() if path.is_file())
    require_equal(set(output_index), {path.name for path in result_files}, "manifest output index")
    for path in result_files:
        require_equal(output_index[path.name].get("sha256"), sha256(path), f"output hash {path.name}")
        require_equal(output_index[path.name].get("bytes"), path.stat().st_size, f"output size {path.name}")

    rows = load_csv(HERE / "results" / "run_results.csv")
    required_columns = set(contract["row_contract"]["required_execution_columns"])
    require(required_columns.issubset(rows[0]), "run_results is missing required execution columns")
    require_equal(len(rows), 2310, "run_results row count")
    allowed_statuses = set(contract["failure_handling"]["allowed_execution_statuses"])
    require(all(row["execution_status"] in allowed_statuses for row in rows), "unknown execution status in run_results")
    require(all(row["execution_status"] == "completed" for row in rows), "one or more evidence rows failed")
    require(all(row.get("failure_code", "") == "" for row in rows), "completed row contains a failure code")
    require(all(row.get("sanitized_exception_class", "") == "" for row in rows), "completed row contains an exception class")

    catalog = {item["id"] for item in contract["seeded_condition_catalog"]}
    seeds = [str(value) for value in contract["experimental_grid"]["common_seeds"]]
    expected: set[tuple[str, str, str, str, str, str]] = set()
    for cap in contract["experimental_grid"]["caps"]:
        cap_text = f"{float(cap):.2f}"
        for horizon in contract["experimental_grid"]["horizons_hours"]:
            for condition in contract["row_contract"]["objective_free_deterministic_ids"]:
                expected.add((contract["run_namespace"], cap_text, str(horizon), "not_applicable", condition, "deterministic"))
            for objective in contract["experimental_grid"]["selection_objectives"]:
                expected.add((contract["run_namespace"], cap_text, str(horizon), objective, "Ridge", "deterministic"))
                for seed_index in range(10):
                    for condition in catalog:
                        expected.add((contract["run_namespace"], cap_text, str(horizon), objective, condition, str(seed_index)))
    observed = [
        (
            row["run_namespace"],
            row["cap"],
            row["horizon_hours"],
            row["selection_objective"],
            row["condition_id"],
            row["seed_index"],
        )
        for row in rows
    ]
    require_equal(len(set(observed)), len(observed), "unique result keys")
    require_equal(set(observed), expected, "complete expected result-key set")
    for cap in ("0.60", "0.70", "0.80"):
        for horizon in ("1", "24"):
            require_equal(sum(row["cap"] == cap and row["horizon_hours"] == horizon for row in rows), 385, f"rows cap={cap} h={horizon}")
    for row in rows:
        label = f"{row['cap']}/h{row['horizon_hours']}/{row['selection_objective']}/{row['condition_id']}/{row['seed_index']}"
        for metric in ("curtailment_mae", "curtailment_rmse", "onset_f1"):
            finite_field(row, metric, label)
        for field in ("n_fit", "n_selection", "n_calibration", "n_test", "n_onsets_selection", "n_onsets_calibration", "n_onsets_test"):
            require(row[field] != "" and int(row[field]) >= 0, f"{label} missing count {field}")
        if row["seed_index"] != "deterministic":
            require_equal(row["seed"], seeds[int(row["seed_index"])], f"common seed for {label}")

    direct = [row for row in rows if row["condition_id"] == "DirectPolicyTransform-Privileged"]
    require_equal(len(direct), 6, "privileged audit rows")
    require(all(finite_field(row, "curtailment_mae", "privileged audit") == 0.0 for row in direct), "privileged audit continuous error is nonzero")
    require(all(row["rank_eligible"].lower() == "false" for row in direct), "privileged audit was admitted to forecast rank")
    for cap in ("0.60", "0.70", "0.80"):
        persistence = next(row for row in rows if row["cap"] == cap and row["horizon_hours"] == "24" and row["condition_id"] == "Persistence")
        seasonal = next(row for row in rows if row["cap"] == cap and row["horizon_hours"] == "24" and row["condition_id"] == "Seasonal-24h")
        for metric in ("curtailment_mae", "curtailment_rmse", "onset_f1"):
            require_equal(persistence[metric], seasonal[metric], f"24 h seasonal identity {cap} {metric}")

    allowed_epochs = {"5", "10", "15", "20"}
    head_or_learned = [row for row in rows if row["architecture"] in {"GRU", "LSTM", "DLinear", "TCN"}]
    require(all(row["checkpoint_epoch"] in allowed_epochs for row in head_or_learned), "invalid or absent frozen checkpoint selection")
    selected = [row for row in rows if row["condition_id"] == "gru_learned_k8_selected_blend"]
    allowed_alphas = {str(float(value)) for value in contract["selection_and_scoring"]["blend_alpha_grid_order"]}
    require(all(row["alpha_head"] in allowed_alphas for row in selected), "selected alpha is outside frozen grid")
    ridge = [row for row in rows if row["condition_id"] == "Ridge"]
    allowed_penalties = {float(value) for value in contract["baselines_and_controls"]["Ridge"]["penalties_order"]}
    require(all(float(row["ridge_lambda"]) in allowed_penalties for row in ridge), "Ridge penalty outside frozen grid")

    trajectories = load_csv(HERE / "results" / "trajectory_ledger.csv")
    require_equal(len(trajectories), 240, "training trajectory count")
    require(all(row["execution_status"] == "completed" for row in trajectories), "training trajectory failure recorded")
    trajectory_keys = {
        (row["cap"], row["horizon_hours"], row["architecture"], row["seed_index"])
        for row in trajectories
    }
    require_equal(len(trajectory_keys), 240, "unique trajectory keys")
    require(all(row["epochs"] == "20" and row["batch_size"] == "256" and row["checkpoint_epochs"] == "5|10|15|20" for row in trajectories), "trajectory budget changed")
    require(all(finite_field(row, "training_runtime_s", "trajectory") > 0 for row in trajectories), "trajectory runtime missing")

    paired = load_csv(HERE / "results" / "paired_effects.csv")
    require_equal(len(paired), 30, "paired-effect row count")
    require(all(row["execution_status"] == "completed" and row["n_pairs"] == "10" for row in paired), "paired effect is incomplete")
    require(all(row["p_exact_sign_flip"] != "" and row["p_holm_within_family_horizon"] != "" for row in paired), "paired exact/Holm result missing")
    expected_contrasts = {
        (family["family_id"], str(horizon), contrast["id"])
        for family in contract["statistics"]["families"]
        for horizon in contract["experimental_grid"]["horizons_hours"]
        for contrast in family["contrasts"]
    }
    require_equal({(row["family_id"], row["horizon_hours"], row["contrast_id"]) for row in paired}, expected_contrasts, "paired contrast grid")

    moving = load_csv(HERE / "results" / "moving_block_supplement.csv")
    require_equal(len(moving), 36, "moving-block row count")
    require(all(row["execution_status"] == "completed" and row["repetitions"] == "5000" for row in moving), "moving-block cell incomplete")
    expected_moving = {
        (str(horizon), contrast, str(length))
        for horizon in contract["experimental_grid"]["horizons_hours"]
        for contrast in contract["supplementary_moving_block_analysis"]["scope"]["contrasts"]
        for length in (24, 168)
    }
    require_equal({(row["horizon_hours"], row["contrast_id"], row["block_length"]) for row in moving}, expected_moving, "moving-block grid")

    aggregate = load_csv(HERE / "results" / "cap_k_sensitivity.csv")
    require_equal(len(aggregate), 258, "condition aggregate row count")
    require(all(row["aggregation_status"] == "complete" for row in aggregate), "incomplete cap/k aggregate")
    ledger = load_csv(HERE / "results" / "completeness_ledger.csv")
    require_equal(len(ledger), 2310, "completeness-ledger row count")
    require(all(row["observed_count"] == "1" and row["ledger_status"] == "complete" for row in ledger), "completeness ledger is not closed")
    failures = load_csv(HERE / "results" / "failure_ledger.csv")
    require_equal(len(failures), 1, "failure-ledger summary rows")
    require_equal(failures[0]["execution_status"], "no_failures_recorded", "failure-ledger status")

    protocol_path = HERE / "results" / "protocol_validity.json"
    try:
        protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse protocol validity record: {exc}")
    require(protocol.get("protocol_valid") is True, "protocol-validity gate is false")
    require(protocol.get("effect_direction_is_not_validity_gate") is True, "effect direction was used as a validity gate")
    require(all(protocol.get("checks", {}).values()), "one or more protocol validity checks failed")
    require(protocol.get("privileged_control_ranked_as_forecaster") is False, "privileged audit rank boundary changed")
    require_equal(protocol.get("completeness", {}).get("completed_rows"), 2310, "protocol completed-row count")
    require(int(protocol.get("effect_direction_counts", {}).get("adverse", 0)) >= 0, "invalid adverse-result ledger")
    return manifest


def validate_statistics_stage() -> dict[str, Any]:
    try:
        from derive_statistics import check_statistics_artifacts
    except (ImportError, OSError) as exc:
        fail(f"cannot load Stage-3 statistics validator: {exc}")
    try:
        return check_statistics_artifacts()
    except SystemExit as exc:
        fail(str(exc))


def validate_references_stage() -> dict[str, int]:
    """Validate the fail-closed citation and nearest-neighbor audit."""

    for path in (CITATION_REPORT_PATH, LITERATURE_GAP_PATH, MANUSCRIPT_PATH):
        require(path.is_file(), f"references-stage artifact missing: {path.relative_to(PROJECT_ROOT)}")
    try:
        citation = CITATION_REPORT_PATH.read_text(encoding="utf-8", errors="strict")
        gap = LITERATURE_GAP_PATH.read_text(encoding="utf-8", errors="strict")
        manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError) as exc:
        fail(f"cannot read references-stage artifact: {exc}")

    audit_lines = re.findall(r"^\|\s*\[(\d+)\]\s*\|(.+)$", citation, flags=re.MULTILINE)
    require_equal(len(audit_lines), 30, "citation-audit row count")
    require_equal({int(number) for number, _ in audit_lines}, set(range(1, 31)), "citation-audit reference IDs")
    for number, body in audit_lines:
        require("IDENTITY-VERIFIED" in body, f"reference [{number}] lacks identity status")
        require("RW0/C" in body, f"reference [{number}] lacks correction status")
        require(any(token in body for token in ("FULL", "PARTIAL")), f"reference [{number}] lacks support level")

    manuscript_reference_rows = {
        int(number): body
        for number, body in re.findall(r"^\[(\d+)\]\s+(.+)$", manuscript, flags=re.MULTILINE)
    }
    audited_manuscript_dois = {
        match.rstrip(".,")
        for number, body in manuscript_reference_rows.items()
        if number <= 30
        for match in re.findall(r"doi:\s*(10\.\d{4,9}/\S+)", body, flags=re.IGNORECASE)
    }
    audit_dois = {
        match.lower()
        for _, body in audit_lines
        for match in re.findall(r"`(10\.\d{4,9}/[^`]+)`", body.split("|", 1)[0], flags=re.IGNORECASE)
    }
    require_equal(len(audited_manuscript_dois), 30, "audited manuscript DOI count")
    require_equal({value.lower() for value in audited_manuscript_dois}, audit_dois, "audited manuscript DOI set")

    citation_tokens = (
        "1,762 files",
        "1,238 files",
        "85fab064661f740a096f12b7e82df0e4455ccba54e26e875aeabf96ef1c18fdc",
        "150383007faca4c61b58953875863868a972d84904eb897e1cc6d8e983badd79",
        "2a57e02daf24ae5ca0ac890cf65cca5f5dcc1124ec5f90d06ad44f107c0c73f7",
        "4fc6574ef453d644fcba8d82be3bb8874816394ccdd86f9861d234a7b4824929",
        "007e61d9e960bcaa29f7132707c1af23306c97213f0ef86a3bfaf290b73f32ea",
        "5908282d0c137859cefa5bdd77472662e9969e67e5805623543b2a459b767396",
        "9054a62c1e9b25b46ea044e981f8ff89c68d2f706aebb5db8cfcdc72392f4e01",
        "Crossref / Retraction Watch",
        "https://gitlab.com/crossref/retraction-watch-data",
        "2026-08-26",
        "d624b4ae1f19a47b6cbcb0f8d548f7048e4f3d71",
        "2962f61f31cfa29efd644cb8b8b60f59456cff225af8bf909dc0be611632a9d9",
        "10.1016/j.ijforecast.2021.01.013",
        "UNSUPPORTED COMPOUND CLAIM",
        "No manuscript file was changed in this stage",
    )
    for token in citation_tokens:
        require(token in citation, f"citation report missing required token: {token}")

    mandatory_dois = (
        "10.1016/j.enconman.2021.114892",
        "10.1109/ACCESS.2026.3686958",
        "10.11159/ehst23.120",
        "10.1016/j.segan.2026.102496",
        "10.1109/ICASSP49660.2025.10889933",
        "10.1016/j.egyai.2026.100855",
        "10.3390/forecast8020032",
        "10.52202/085713-4860",
    )
    for doi in mandatory_dois:
        require(doi.lower() in gap.lower(), f"mandatory nearest comparator absent: {doi}")
        matching_rows = [line for line in gap.splitlines() if line.startswith("| NN-") and doi.lower() in line.lower()]
        require_equal(len(matching_rows), 1, f"nearest-neighbor matrix row for {doi}")
        require_equal(matching_rows[0].count("|"), 13, f"nearest-neighbor matrix dimensions for {doi}")
        require("RW0/C0" in matching_rows[0], f"mandatory DOI lacks correction status: {doi}")

    matrix_dimensions = (
        "Target",
        "Data visibility",
        "Forecast horizon",
        "Retrieval mechanism",
        "Uncertainty output",
        "Baseline breadth",
        "Statistics",
        "Release / provenance",
        "Correction status",
        "Direct / adjacent",
        "Support basis",
    )
    matrix_header = next((line for line in gap.splitlines() if line.startswith("| ID / record |")), "")
    for dimension in matrix_dimensions:
        require(dimension in matrix_header, f"nearest-neighbor matrix dimension absent: {dimension}")

    required_gap_tokens = (
        "https://proceedings.mlr.press/v267/han25d.html",
        "conference-to-journal lineage",
        "PRIMARY-FULL",
        "PRIMARY-ABSTRACT",
        "AUTHOR-FULL",
        "LOCAL-FULL",
        "OFFICIAL-REPO",
        "UNVERIFIED",
        "VERIFIED-DIRECT",
        "VERIFIED-ADJACENT",
        "bounded protocol/evidence advance over the explicitly verified corpus",
        "not proof of global novelty",
        "global first",
        "exhaustive SOTA",
        "cross-paper superiority",
        "No manuscript file was changed in this stage",
        "API responses",
        "publisher files",
        "extracted text",
        "caches",
        "temporary directories",
    )
    for token in required_gap_tokens:
        require(token in gap, f"literature-gap report missing required token: {token}")

    local_inventory = {
        "ieee_access_2023_federated_load_forecasting.pdf": (
            "10.1109/ACCESS.2023.3262171",
            "76bd3403ef95b3c1176fd9fb6e2801db079ab88be9efe0ed8af99ee5707718b6",
        ),
        "ieee_access_2023_vmd_pyraformer_adan.pdf": (
            "10.1109/ACCESS.2023.3273596",
            "1d0f96081ce9a6ff09783883eddfff26138db1826493b82c0466b26e107a8945",
        ),
        "ieee_access_2024_de_ihho_bilstm.pdf": (
            "10.1109/ACCESS.2024.3437247",
            "0e43fa69b58683db740640d3f4efe52da6bffb882d15108a99de8761507f5060",
        ),
        "ieee_access_2024_enhanced_dnn_distribution.pdf": (
            "10.1109/ACCESS.2024.3432647",
            "b02e33f9916fbf9f5850b416e8e49295ee50574735ffd4483b8ab0ee5d3ef04f",
        ),
        "ieee_access_2024_feature_extraction_combination.pdf": (
            "10.1109/ACCESS.2024.3384246",
            "03241b3797adbc1ffae1145ebdb70db578416f7d7d0ae8c46676723701de4cbf",
        ),
        "ieee_access_2024_sade_elm_cawoa_svm.pdf": (
            "10.1109/ACCESS.2024.3377097",
            "9a7efe82b64a042985511ab4de2479fbfdae98ebb21c51c0cdf58b627a169f75",
        ),
        "ieee_access_2024_timesnet_crossformer_lstm.pdf": (
            "10.1109/ACCESS.2024.3383912",
            "9054a62c1e9b25b46ea044e981f8ff89c68d2f706aebb5db8cfcdc72392f4e01",
        ),
    }
    for filename, (doi, digest) in local_inventory.items():
        rows = [line for line in gap.splitlines() if line.startswith("| `ieee_access_") and filename in line]
        require_equal(len(rows), 1, f"local IEEE Access inventory row for {filename}")
        require(doi.lower() in rows[0].lower(), f"local inventory DOI missing for {filename}")
        require(digest in rows[0], f"local inventory hash missing for {filename}")
        require("RW0/C0" in rows[0], f"local inventory correction status missing for {filename}")

    prohibited_assertions = (
        r"\bwe are the first\b",
        r"\bfirst-ever\b",
        r"\boutperforms all\b",
        r"\bglobally novel\b",
    )
    for pattern in prohibited_assertions:
        require(re.search(pattern, gap, flags=re.IGNORECASE) is None, f"unbounded assertion present: {pattern}")

    return {"citation_rows": len(audit_lines), "nearest_rows": len(re.findall(r"^\| NN-", gap, flags=re.MULTILINE)), "local_pdfs": len(local_inventory)}


def validate_manuscript_stage() -> dict[str, int]:
    """Validate the Stage-5 narrative, artifact, citation, and PDF boundary."""

    required_paths = (
        MANUSCRIPT_PATH,
        PROJECT_ROOT / "manuscript" / "DEEP_REVISION_EVIDENCE.md",
        PROJECT_ROOT / "manuscript" / "TABLE_TO_CONFIG_MANIFEST.md",
        FIGURE_DIR / "make_figures.py",
        FIGURE_MANIFEST_PATH,
        PAPER_TEX_PATH,
        PAPER_PDF_PATH,
    )
    for path in required_paths:
        require(path.is_file(), f"manuscript-stage artifact missing: {path.relative_to(PROJECT_ROOT)}")

    manuscript = MANUSCRIPT_PATH.read_text(encoding="utf-8", errors="strict")
    tex = PAPER_TEX_PATH.read_text(encoding="utf-8", errors="strict")
    evidence = (PROJECT_ROOT / "manuscript" / "DEEP_REVISION_EVIDENCE.md").read_text(encoding="utf-8", errors="strict")
    table_map = (PROJECT_ROOT / "manuscript" / "TABLE_TO_CONFIG_MANIFEST.md").read_text(encoding="utf-8", errors="strict")
    try:
        figure_manifest = json.loads(FIGURE_MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        fail(f"cannot parse paper-facing figure manifest: {exc}")

    narrative_tokens = (
        "# A Reproducible Retrospective Curtailment-Risk Benchmark",
        "**RQ1:**",
        "**RQ2:**",
        "**RQ3:**",
        "The contributions follow those questions:",
        "Gap-to-contribution-to-result map",
        "bounded protocol/evidence advance over the explicitly verified corpus",
        "Persistence nevertheless has lower MAE",
        "no general learned-space advantage is supported",
        "Onset-targeted analysis is inapplicable",
        "conditional descriptive sensitivities",
        "not operational forecasts",
        "AUTHOR INPUT REQUIRED",
        "## IX. Conclusion",
    )
    for token in narrative_tokens:
        require(token in manuscript, f"manuscript narrative token missing: {token}")

    numeric_tokens = (
        "2310",
        "240 training trajectories",
        "0.00690794",
        "0.00777391",
        "0.02054651",
        "0.02076857",
        "-0.00498575",
        "-0.00026812",
        "+0.00126543",
        "-0.00004826",
        "0.01171875",
        "0.36328125",
        "[-0.00032314, +0.00305015]",
        "[-0.00008188, +0.00309993]",
    )
    for token in numeric_tokens:
        require(token in manuscript, f"paper-facing evidence value missing: {token}")

    body_before_references = manuscript.split("## References", 1)[0]
    unsupported_repairs = (
        "Three-North wind curtailment",
        "economically optimal marginal curtailment",
        "Euclidean similar days",
        "retrieve–reuse–revise–retain",
        "reinforce a relevant evaluation requirement",
        "raw-feature k-NN or randomized-space control would be required",
    )
    for phrase in unsupported_repairs:
        require(phrase.lower() not in body_before_references.lower(), f"Stage-4 unsupported proposition remains: {phrase}")
    prohibited_claims = (
        r"\bwe are the first\b",
        r"\bfirst-ever\b",
        r"\boutperforms all\b",
        r"\bglobally novel\b",
        r"\boperational deployment\b",
        r"\bobserved-curtailment accuracy\b",
    )
    for pattern in prohibited_claims:
        require(re.search(pattern, body_before_references, flags=re.IGNORECASE) is None, f"unlicensed manuscript claim present: {pattern}")

    references = {
        int(number): body
        for number, body in re.findall(r"^\[(\d+)\]\s+(.+)$", manuscript, flags=re.MULTILINE)
    }
    require_equal(set(references), set(range(1, 39)), "manuscript reference numbering")
    citation_rows = re.findall(r"^\|\s*\[(\d+)\]\s*\|(.+)$", CITATION_REPORT_PATH.read_text(encoding="utf-8"), flags=re.MULTILINE)
    audited_dois = {
        int(number): re.search(r"`(10\.\d{4,9}/[^`]+)`", body, flags=re.IGNORECASE).group(1).lower()
        for number, body in citation_rows
    }
    for number, doi in audited_dois.items():
        require(doi in references[number].lower(), f"audited DOI missing or renumbered at reference [{number}]")
    nearest_dois = (
        "10.1016/j.enconman.2021.114892",
        "10.1016/j.segan.2026.102496",
        "10.1109/access.2026.3686958",
        "10.1109/icassp49660.2025.10889933",
        "10.1016/j.egyai.2026.100855",
        "10.3390/forecast8020032",
        "10.52202/085713-4860",
    )
    for doi in nearest_dois:
        require(doi in manuscript.lower(), f"Stage-4 nearest DOI absent from manuscript: {doi}")
    require("https://proceedings.mlr.press/v267/han25d.html" in manuscript, "RAFT primary record absent from manuscript")

    required_headings = (
        "Title-to-Evidence Map",
        "Primary Estimand and Analysis Unit",
        "Comparison Budget and Data Visibility",
        "Negative and Null Results",
        "Shared Assets and Independent Contribution",
        "New or Rerun Experiments",
        "Unresolved Human Blockers",
    )
    for heading in required_headings:
        require(heading in evidence, f"revision-evidence heading missing: {heading}")
    require("Stage-5 manuscript binding" in evidence, "revision evidence was not advanced to Stage 5")
    require("Paper-facing figure bindings" in table_map, "figure-to-evidence bindings missing")
    require("pre-v2 result family" not in table_map, "stale version-scope handoff remains")

    require_equal(figure_manifest.get("schema"), "p1_manuscript_figure_manifest", "figure manifest schema")
    require_equal(figure_manifest.get("schema_version"), 2, "figure manifest schema version")
    require_equal(figure_manifest.get("source_run_namespace"), "p1_ieee_access_upgrade_v2", "figure source namespace")
    require("p1_s3_fair_v1" not in json.dumps(figure_manifest), "legacy v1 source leaked into figure manifest")
    expected_stems = {
        "fig_benchmark_overview",
        "fig_architecture",
        "fig_primary_effects",
        "fig_cap_profile",
    }
    require_equal(set(figure_manifest.get("paper_facing_stems", [])), expected_stems, "paper-facing figure stems")
    generated = figure_manifest.get("generated_figures", [])
    require_equal(len(generated), 8, "generated PNG/PDF figure count")
    for record in generated:
        path = FIGURE_DIR / record["file"]
        require(path.is_file(), f"generated figure missing: {record['file']}")
        require_equal(path.stat().st_size, int(record["bytes"]), f"generated figure bytes {record['file']}")
        require_equal(sha256(path), record["sha256"], f"generated figure hash {record['file']}")
    for stem in expected_stems:
        require(f"figures/{stem}.png" in manuscript, f"paper-facing image not cited: {stem}")
        require(f"figures/{stem}.png" in tex, f"paper-facing image absent from TeX: {stem}")
    require_equal(len(re.findall(r"^\*\*Table\s+\d+\.\*\*", manuscript, flags=re.MULTILINE)), 6, "Markdown table caption count")
    require_equal(len(re.findall(r"^\*\*Fig\.\s+\d+\.\*\*", manuscript, flags=re.MULTILINE)), 4, "Markdown figure caption count")
    require_equal(len(re.findall(r"\\caption\{", tex)), 10, "TeX float caption count")
    require_equal(len(re.findall(r"\\bibitem\{ref\d+\}", tex)), 38, "TeX bibliography count")
    tex_tokens = tex.replace(r"\_", "_")
    require("p1_s3_fair_v1" not in tex_tokens, "legacy v1 namespace remains in exact TeX source")
    require("p1_ieee_access_upgrade_v2" in tex_tokens, "v2 namespace absent from exact TeX source")

    require(PAPER_PDF_PATH.stat().st_size >= 100_000, "paper PDF is implausibly small")
    require(PAPER_PDF_PATH.stat().st_mtime_ns >= PAPER_TEX_PATH.stat().st_mtime_ns, "paper PDF predates exact TeX source")
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(PAPER_PDF_PATH))
        page_count = len(reader.pages)
        require(0 < page_count < 20, f"pre-biography page target failed: {page_count} pages")
        extracted = "\n".join((page.extract_text() or "") for page in reader.pages)
    except (ImportError, OSError, ValueError) as exc:
        fail(f"cannot inspect exact paper PDF: {exc}")
    for token in ("Persistence", "GRU", "2310", "AUTHOR INPUT REQUIRED"):
        require(token.lower() in extracted.lower(), f"built PDF text missing required token: {token}")
    require("p1_s3_fair_v1" not in extracted, "legacy v1 namespace remains in built PDF")
    log_path = PAPER_TEX_PATH.with_suffix(".log")
    if log_path.is_file():
        log = log_path.read_text(encoding="utf-8", errors="replace")
        require("There were undefined references" not in log, "LaTeX reports undefined references")
        require("Citation `" not in log or "undefined" not in log, "LaTeX reports an undefined citation")

    return {
        "references": len(references),
        "figures": len(expected_stems),
        "tables": 6,
        "pages": page_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--phase", choices=("contract", "experiments", "statistics", "references", "manuscript"), default="contract")
    args = parser.parse_args(argv)
    contract = validate_contract(
        require_contract_stage_absence=args.phase == "contract",
        # Stage 3 is explicitly allowed to supersede the pre-v2 evidence map.
        # The normative contract and sealed Stage-2 inputs remain immutable.
        require_preserved_map_hashes=args.phase not in {"statistics", "references", "manuscript"},
    )
    if args.phase == "experiments":
        manifest = validate_execution(contract)
        print(
            "OK "
            f"{contract['run_namespace']}: execution valid; rows={manifest['row_counts']['run_results']}; "
            f"trajectories={manifest['row_counts']['trajectory_ledger']}; "
            f"contract_sha256={sha256(CONTRACT_PATH)}; phase=experiments"
        )
        return 0
    if args.phase == "statistics":
        summary = validate_statistics_stage()
        print(
            "OK "
            f"{contract['run_namespace']}: statistics valid; paired={summary['paired_rows']}; "
            f"moving_block={summary['moving_block_rows']}; paper_tables={summary['paper_tables']}; "
            f"provenance={summary['provenance_schema']}; phase=statistics"
        )
        return 0
    if args.phase == "references":
        summary = validate_references_stage()
        print(
            "OK "
            f"{contract['run_namespace']}: references valid; citations={summary['citation_rows']}; "
            f"nearest={summary['nearest_rows']}; local_pdfs={summary['local_pdfs']}; phase=references"
        )
        return 0
    if args.phase == "manuscript":
        summary = validate_manuscript_stage()
        print(
            "OK "
            f"{contract['run_namespace']}: manuscript valid; references={summary['references']}; "
            f"figures={summary['figures']}; tables={summary['tables']}; pages={summary['pages']}; "
            "phase=manuscript"
        )
        return 0
    print(
        "OK "
        f"{contract['run_namespace']}: prospective contract valid; "
        f"rows={contract['row_contract']['total_rows']}; "
        f"contract_sha256={sha256(CONTRACT_PATH)}; phase={args.phase}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
