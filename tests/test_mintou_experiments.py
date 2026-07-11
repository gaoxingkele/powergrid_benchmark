from __future__ import annotations

import csv
from pathlib import Path

from powergrid_benchmark.mintou_experiments import PAPERS, MINTOU_ROOT, result_rows


def test_mintou_portfolio_has_six_unique_papers() -> None:
    assert len(PAPERS) == 6
    assert len({paper.paper_id for paper in PAPERS}) == 6
    assert len({paper.algorithm_name for paper in PAPERS}) == 6
    assert all(paper.tag == "mintou" for paper in PAPERS)


def test_each_paper_has_target_journal_level_experiment_coverage() -> None:
    for paper in PAPERS:
        assert len(paper.main_experiments) >= 7
        assert len(paper.ablations) >= 6
        assert len(paper.baselines) >= 5
        assert paper.datasets
        assert paper.metrics


def test_result_generation_covers_proposed_baselines_and_ablations() -> None:
    for paper in PAPERS:
        rows = result_rows(paper, repeats=2)
        roles = {row["method_role"] for row in rows}
        assert {"proposed", "baseline", "ablation"} <= roles
        assert len({row["experiment_id"] for row in rows}) == len(paper.main_experiments)


def test_scaffold_outputs_exist_after_generation() -> None:
    for paper in PAPERS:
        root = MINTOU_ROOT / paper.directory
        assert (root / "PAPER.md").exists()
        assert (root / "logic" / "claims.md").exists()
        assert (root / "evidence" / "runs" / "synthetic_smoke_results.csv").exists()
        with (root / "evidence" / "tables" / "synthetic_smoke_leaderboard.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        assert rows[0]["method"] == paper.algorithm_name


def test_p2_real_opsd_public_benchmark_outputs_exist() -> None:
    root = MINTOU_ROOT / "mintou_p2_hygraph_load_forecasting"
    required = [
        root / "evidence" / "runs" / "real_opsd_forecasting_results.csv",
        root / "evidence" / "tables" / "real_opsd_leaderboard.csv",
        root / "evidence" / "runs" / "real_opsd_analysis.md",
        root / "evidence" / "runs" / "real_opsd_analysis_v1_weak.md",
        root / "evidence" / "runs" / "real_opsd_analysis_v2_mixed.md",
        root / "evidence" / "runs" / "real_opsd_analysis_v3_gate_mixed.md",
        root / "evidence" / "runs" / "real_opsd_rolling_results.csv",
        root / "evidence" / "tables" / "real_opsd_rolling_leaderboard.csv",
        root / "evidence" / "runs" / "real_opsd_rolling_analysis.md",
        root / "evidence" / "source" / "real_opsd_source_profile.csv",
        root / "src" / "configs" / "real_opsd_config.json",
    ]
    for path in required:
        assert path.exists(), path
    with (root / "evidence" / "tables" / "real_opsd_leaderboard.csv").open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    horizons = {row["horizon_hours"] for row in rows}
    methods = {row["method"] for row in rows}
    assert {"1", "24"} <= horizons
    assert "HyG-LoadFormer" in methods
    with (root / "evidence" / "tables" / "real_opsd_rolling_leaderboard.csv").open(encoding="utf-8-sig") as handle:
        rolling_rows = list(csv.DictReader(handle))
    assert any(row["method"] == "HyG-LoadFormer" and row["horizon_hours"] == "24" for row in rolling_rows)
    assert "mean_mape" in rolling_rows[0]


def test_p2_real_simbench_public_benchmark_outputs_exist() -> None:
    root = MINTOU_ROOT / "mintou_p2_hygraph_load_forecasting"
    required = [
        root / "evidence" / "runs" / "real_simbench_forecasting_results.csv",
        root / "evidence" / "tables" / "real_simbench_leaderboard.csv",
        root / "evidence" / "runs" / "real_simbench_analysis.md",
        root / "evidence" / "runs" / "real_simbench_analysis_v1_mixed.md",
        root / "evidence" / "runs" / "real_simbench_analysis_v2_gate_mixed.md",
        root / "evidence" / "runs" / "real_simbench_rolling_results.csv",
        root / "evidence" / "tables" / "real_simbench_rolling_leaderboard.csv",
        root / "evidence" / "runs" / "real_simbench_rolling_analysis.md",
        root / "evidence" / "source" / "real_simbench_source_profile.csv",
        root / "src" / "configs" / "real_simbench_config.json",
    ]
    for path in required:
        assert path.exists(), path
    with (root / "evidence" / "tables" / "real_simbench_leaderboard.csv").open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    horizons = {row["horizon_hours"] for row in rows}
    assert {"1", "24"} <= horizons
    assert any(row["method"] == "HyG-LoadFormer" for row in rows)
    assert "normalized_mae" in rows[0]
    with (root / "evidence" / "tables" / "real_simbench_rolling_leaderboard.csv").open(encoding="utf-8-sig") as handle:
        rolling_rows = list(csv.DictReader(handle))
    assert any(row["method"] == "HyG-LoadFormer" and row["horizon_hours"] == "24" for row in rolling_rows)
    assert "mean_normalized_mae" in rolling_rows[0]


def test_p3_p4_real_simbench_planning_outputs_exist() -> None:
    checks = [
        ("mintou_p3_samode_distribution_planning", "CARS-MODE"),
        ("mintou_p4_shield_resilience_planning", "SHIELD-MOEA"),
    ]
    for directory, method in checks:
        root = MINTOU_ROOT / directory
        required = [
            root / "evidence" / "runs" / "real_simbench_planning_results.csv",
            root / "evidence" / "tables" / "real_simbench_planning_leaderboard.csv",
            root / "evidence" / "runs" / "real_simbench_planning_analysis.md",
            root / "evidence" / "runs" / "real_simbench_planning_analysis_v1_weak.md",
            root / "evidence" / "source" / "real_simbench_planning_source_profile.csv",
            root / "src" / "configs" / "real_simbench_planning_config.json",
        ]
        for path in required:
            assert path.exists(), path
        with (root / "evidence" / "tables" / "real_simbench_planning_leaderboard.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        assert any(row["method"] == method for row in rows)
        assert "mean_hypervolume_proxy" in rows[0]
        assert "mean_der_readiness" in rows[0]
        assert "mean_flexibility_ratio" in rows[0]


def test_p3_preserves_second_weak_revision() -> None:
    root = MINTOU_ROOT / "mintou_p3_samode_distribution_planning"
    assert (root / "evidence" / "runs" / "real_simbench_planning_analysis_v2_weak.md").exists()
    assert (root / "evidence" / "runs" / "real_simbench_planning_analysis_v3_weak.md").exists()
    assert (root / "evidence" / "runs" / "real_simbench_planning_analysis_v4_near_miss.md").exists()


def test_p1_real_rts_dispatch_outputs_exist() -> None:
    root = MINTOU_ROOT / "mintou_p1_dstar_gru_dispatch"
    required = [
        root / "evidence" / "runs" / "real_rts_dispatch_results.csv",
        root / "evidence" / "tables" / "real_rts_dispatch_leaderboard.csv",
        root / "evidence" / "tables" / "real_rts_dispatch_stress_leaderboard.csv",
        root / "evidence" / "tables" / "real_rts_dispatch_rolling_leaderboard.csv",
        root / "evidence" / "tables" / "real_rts_dispatch_rolling_summary.csv",
        root / "evidence" / "runs" / "real_rts_dispatch_analysis.md",
        root / "evidence" / "runs" / "real_rts_dispatch_stress_analysis.md",
        root / "evidence" / "runs" / "real_rts_dispatch_rolling_analysis.md",
        root / "evidence" / "runs" / "real_rts_dispatch_analysis_v1_weak.md",
        root / "evidence" / "runs" / "real_rts_dispatch_analysis_v2_marginal.md",
        root / "evidence" / "source" / "real_rts_dispatch_source_profile.csv",
        root / "src" / "configs" / "real_rts_dispatch_config.json",
    ]
    for path in required:
        assert path.exists(), path
    with (root / "evidence" / "tables" / "real_rts_dispatch_leaderboard.csv").open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert any(row["method"] == "DSTAR-GRU" for row in rows)
    assert "composite_dispatch_score" in rows[0]
    with (root / "evidence" / "tables" / "real_rts_dispatch_rolling_summary.csv").open(encoding="utf-8-sig") as handle:
        rolling_rows = list(csv.DictReader(handle))
    assert any(row["method"] == "DSTAR-GRU" for row in rolling_rows)
    assert "mean_composite_dispatch_score" in rolling_rows[0]


def test_p5_p6_real_project_review_outputs_exist() -> None:
    checks = [
        ("mintou_p5_trace_moea_feasibility_review", "TRACE-MOEA", "budget_feasibility_rate"),
        ("mintou_p6_bilonsga_project_review", "BiLo-NSGA", "move_trace_completeness"),
    ]
    for directory, method, metric in checks:
        root = MINTOU_ROOT / directory
        required = [
            root / "evidence" / "runs" / "real_project_review_results.csv",
            root / "evidence" / "tables" / "real_project_review_leaderboard.csv",
            root / "evidence" / "runs" / "real_project_review_analysis.md",
            root / "evidence" / "runs" / "real_project_review_analysis_v1_weak.md",
            root / "evidence" / "runs" / "real_project_review_analysis_v2_weak.md",
            root / "evidence" / "source" / "real_project_review_source_profile.csv",
            root / "src" / "configs" / "real_project_review_config.json",
            root / "src" / "configs" / "real_project_review_methods.json",
        ]
        for path in required:
            assert path.exists(), path
        with (root / "evidence" / "tables" / "real_project_review_leaderboard.csv").open(encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        assert any(row["method"] == method for row in rows)
        assert "mean_hypervolume_proxy" in rows[0]
        assert f"mean_{metric}" in rows[0]


def test_p5_preserves_near_miss_revision() -> None:
    root = MINTOU_ROOT / "mintou_p5_trace_moea_feasibility_review"
    assert (root / "evidence" / "runs" / "real_project_review_analysis_v3_near_miss.md").exists()


def test_submission_asset_package_indexes_all_mintou_papers() -> None:
    root = MINTOU_ROOT / "submission_assets"
    required = [
        root / "README.md",
        root / "paper_asset_manifest.csv",
        root / "evidence_index.csv",
        root / "claim_scope_matrix.md",
        root / "reviewer_readiness_checklist.md",
        root / "remaining_validation_gaps.md",
    ]
    for path in required:
        assert path.exists(), path
    with (root / "paper_asset_manifest.csv").open(encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 6
    assert {row["paper_id"] for row in rows} == {f"mintou_p{idx}" for idx in range(1, 7)}
    assert all(row["status"] != "project_original_planned" for row in rows)
    with (root / "evidence_index.csv").open(encoding="utf-8-sig") as handle:
        evidence_rows = list(csv.DictReader(handle))
    assert len(evidence_rows) >= 100
    assert all(row["path"].startswith("papers/mintou/") for row in evidence_rows)
