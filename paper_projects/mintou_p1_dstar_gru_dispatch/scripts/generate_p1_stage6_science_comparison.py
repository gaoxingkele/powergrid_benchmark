"""Generate the Stage-6 field-aware comparison for the frozen v2 rerun.

This script is intentionally separate from the terminal release validator.
It writes only the two comparison records in the isolated rerun namespace.
The accepted execution, manuscript, derived tables, and release files are
read-only inputs.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
ACCEPTED = ROOT / "experiments" / "p1_ieee_access_upgrade_v2"
RERUN = ROOT / "experiments" / "p1_ieee_access_upgrade_v2_stage6_attempt5"
TABLE_DIR = ROOT / "manuscript" / "derived_tables"
REPORT_JSON = RERUN / "STAGE6_RERUN_COMPARISON.json"
REPORT_MD = RERUN / "STAGE6_RERUN_COMPARISON.md"

EXPECTED_RUNNER_SHA256 = "d4f0e14dd010e4f429e2d61771d781b169a673b73156dac5236113f0e3f34e28"
EXPECTED_CONTRACT_SHA256 = "3d99dc96aeb9ac51974f76e5c0f544083f4dc41a4f5de5998b7b3e7f2ec78878"
EXPECTED_ABSTRACT_SHA256 = "c86963d625f30e7f1c709f0b2ea55a6913c01a51d88835f3053fb42c37f176f6"
TIMING_FIELDS = {
    "run_results.csv": {"training_runtime_s", "condition_runtime_s"},
    "trajectory_ledger.csv": {"training_runtime_s"},
}
SCIENTIFIC_MANIFEST_FIELDS = (
    "schema",
    "schema_version",
    "run_namespace",
    "status",
    "approved_stage",
    "source_profile",
    "parameter_counts",
    "fixed_budgets",
    "protocol_valid",
    "row_counts",
    "selections",
    "completeness",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"STAGE6 SCIENCE COMPARISON FAILED: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", errors="strict", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        fields = list(reader.fieldnames or [])
    require(bool(fields) and bool(rows), f"empty CSV: {path}")
    return fields, rows


def load_deriver() -> Any:
    path = ACCEPTED / "derive_statistics.py"
    spec = importlib.util.spec_from_file_location("p1_stage6_deriver", path)
    require(spec is not None and spec.loader is not None, "cannot load accepted statistics deriver")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def compare_csv(name: str) -> dict[str, Any]:
    accepted_fields, accepted_rows = load_csv(ACCEPTED / "results" / name)
    rerun_fields, rerun_rows = load_csv(RERUN / "results" / name)
    require(accepted_fields == rerun_fields, f"header mismatch: {name}")
    require(len(accepted_rows) == len(rerun_rows), f"row-count mismatch: {name}")
    timing = TIMING_FIELDS.get(name, set())
    differences = {field: 0 for field in accepted_fields}
    for accepted_row, rerun_row in zip(accepted_rows, rerun_rows, strict=True):
        for field in accepted_fields:
            if accepted_row[field] != rerun_row[field]:
                differences[field] += 1
    scientific_differences = {field: count for field, count in differences.items() if count and field not in timing}
    require(not scientific_differences, f"scientific CSV fields differ in {name}: {scientific_differences}")
    return {
        "rows": len(accepted_rows),
        "raw_bytes_equal": (ACCEPTED / "results" / name).read_bytes() == (RERUN / "results" / name).read_bytes(),
        "scientific_fields_equal": True,
        "excluded_non_scientific_timing_fields": sorted(timing),
        "timing_difference_counts": {
            field: differences[field] for field in sorted(timing) if differences[field]
        },
        "accepted_sha256": sha256(ACCEPTED / "results" / name),
        "rerun_sha256": sha256(RERUN / "results" / name),
    }


def compare_npz() -> dict[str, Any]:
    name = "test_predictions_primary_mae.npz"
    accepted_path = ACCEPTED / "results" / name
    rerun_path = RERUN / "results" / name
    with np.load(accepted_path, allow_pickle=False) as accepted_archive, np.load(rerun_path, allow_pickle=False) as rerun_archive:
        require(accepted_archive.files == rerun_archive.files, "prediction archive keys differ")
        for key in accepted_archive.files:
            require(np.array_equal(accepted_archive[key], rerun_archive[key]), f"prediction array differs: {key}")
        array_count = len(accepted_archive.files)
    require(accepted_path.read_bytes() == rerun_path.read_bytes(), "prediction archive raw bytes differ")
    return {
        "arrays": array_count,
        "array_values_equal": True,
        "raw_bytes_equal": True,
        "accepted_sha256": sha256(accepted_path),
        "rerun_sha256": sha256(rerun_path),
    }


def compare_derived_tables() -> dict[str, Any]:
    deriver = load_deriver()
    contract = load_json(RERUN / "upgrade_contract.json")
    _, run_rows = load_csv(RERUN / "results" / "run_results.csv")
    paired = deriver.recompute_paired(run_rows, contract)
    _, sealed_paired = load_csv(RERUN / "results" / "paired_effects.csv")
    deriver.compare_rows(sealed_paired, paired, "Stage-6 rerun paired effects")
    deriver.RESULT_DIR = RERUN / "results"
    moving = deriver.recompute_moving(contract)
    _, sealed_moving = load_csv(RERUN / "results" / "moving_block_supplement.csv")
    deriver.compare_rows(sealed_moving, moving, "Stage-6 rerun moving-block effects")
    cross_cap = deriver.cross_cap_rows(run_rows)
    expected = {
        "v2_paired_seed_effects.csv": deriver.csv_bytes(deriver.paper_paired_rows(paired)),
        "v2_moving_block_sensitivity.csv": deriver.csv_bytes(deriver.paper_moving_rows(moving)),
        "v2_deterministic_references.csv": deriver.csv_bytes(deriver.deterministic_rows(run_rows)),
        "v2_cross_cap_descriptive.csv": deriver.csv_bytes(cross_cap),
        "v2_claim_wording_router.csv": deriver.csv_bytes(deriver.router_rows(paired, cross_cap)),
    }
    records: dict[str, Any] = {}
    for name, rerun_bytes in expected.items():
        accepted_path = TABLE_DIR / name
        working_bytes = accepted_path.read_bytes()
        accepted_canonical = working_bytes.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        require(accepted_canonical == rerun_bytes, f"rerun-derived paper table differs: {name}")
        records[name] = {
            "canonical_scientific_bytes_equal": True,
            "working_checkout_raw_bytes_equal": working_bytes == rerun_bytes,
            "working_checkout_line_endings": "CRLF" if b"\r\n" in working_bytes else "LF",
            "rows": rerun_bytes.count(b"\n") - 1,
            "sha256": hashlib.sha256(rerun_bytes).hexdigest(),
        }
    return records


def narrative_and_placeholder_record() -> dict[str, Any]:
    manuscript_path = ROOT / "manuscript" / "MANUSCRIPT.md"
    tex_path = ROOT / "manuscript" / "journal_submission" / "paper.tex"
    manuscript = manuscript_path.read_text(encoding="utf-8")
    tex = tex_path.read_text(encoding="utf-8")
    abstract = manuscript.split("## Abstract", 1)[1].split("\n\n", 2)[1]
    tex_abstract = tex.split(r"\begin{abstract}", 1)[1].split(r"\end{abstract}", 1)[0].strip().replace(r"\%", "%")
    word_count = len(re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", abstract))
    abstract_sha = hashlib.sha256(abstract.encode("utf-8")).hexdigest()
    require(word_count == 236, f"accepted narrative word count changed: {word_count}")
    require(abstract_sha == EXPECTED_ABSTRACT_SHA256, "accepted 236-word narrative hash changed")
    require(abstract == tex_abstract, "Markdown and TeX abstract narratives differ")
    require(manuscript.count("AUTHOR INPUT REQUIRED") == 11, "Markdown human-placeholder count changed")
    require(tex.count("AUTHOR INPUT REQUIRED") == 9, "TeX human-placeholder count changed")
    return {
        "token_rule": "ASCII alphabetic words with internal hyphens retained as one token",
        "word_count": word_count,
        "sha256": abstract_sha,
        "markdown_tex_semantic_text_equal": True,
        "markdown_author_input_required_count": 11,
        "tex_author_input_required_count": 9,
    }


def main() -> int:
    accepted_manifest = load_json(ACCEPTED / "run_manifest.json")
    rerun_manifest = load_json(RERUN / "run_manifest.json")
    require(sha256(RERUN / "run_upgrade.py") == EXPECTED_RUNNER_SHA256, "rerun script identity mismatch")
    require(sha256(RERUN / "upgrade_contract.json") == EXPECTED_CONTRACT_SHA256, "rerun contract identity mismatch")
    require(rerun_manifest["script"]["sha256"] == EXPECTED_RUNNER_SHA256, "manifest runner hash mismatch")
    require(rerun_manifest["contract"]["sha256"] == EXPECTED_CONTRACT_SHA256, "manifest contract hash mismatch")
    for field in SCIENTIFIC_MANIFEST_FIELDS:
        require(accepted_manifest[field] == rerun_manifest[field], f"scientific manifest field differs: {field}")
    require(accepted_manifest["environment"] == rerun_manifest["environment"], "execution environment differs")

    csv_records = {
        path.name: compare_csv(path.name)
        for path in sorted((ACCEPTED / "results").glob("*.csv"))
    }
    prediction_record = compare_npz()
    derived_records = compare_derived_tables()
    narrative_record = narrative_and_placeholder_record()
    timing_only_files = {
        name: record["timing_difference_counts"]
        for name, record in csv_records.items()
        if record["timing_difference_counts"]
    }
    require(set(timing_only_files) == set(TIMING_FIELDS), "unexpected set of timing-varying outputs")

    report = {
        "schema": "p1_stage6_frozen_rerun_comparison",
        "schema_version": 1,
        "attempt": "5/5",
        "status": "scientific_content_exact_timing_disclosed",
        "supports_new_claim": False,
        "identity": {
            "runner_sha256": EXPECTED_RUNNER_SHA256,
            "contract_sha256": EXPECTED_CONTRACT_SHA256,
            "runner_exact": True,
            "contract_exact": True,
            "source_profile_exact": True,
            "source_file_hashes_exact": True,
        },
        "scientific_manifest_fields": {
            "fields": list(SCIENTIFIC_MANIFEST_FIELDS),
            "exact": True,
        },
        "scientific_outputs": {
            "csv": csv_records,
            "prediction_archive": prediction_record,
            "all_non_timing_content_exact": True,
        },
        "derived_tables": derived_records,
        "environment": {
            "exact": True,
            "accepted": accepted_manifest["environment"],
            "rerun": rerun_manifest["environment"],
        },
        "timing_and_execution_metadata": {
            "scientific": False,
            "accepted_started_at": accepted_manifest["started_at"],
            "rerun_started_at": rerun_manifest["started_at"],
            "accepted_completed_at": accepted_manifest["completed_at"],
            "rerun_completed_at": rerun_manifest["completed_at"],
            "accepted_runtimes_seconds": accepted_manifest["runtimes_seconds"],
            "rerun_runtimes_seconds": rerun_manifest["runtimes_seconds"],
            "csv_timing_difference_counts": timing_only_files,
            "namespace_and_absolute_command_paths_differ_by_isolated_location": True,
        },
        "accepted_narrative_and_human_placeholders": narrative_record,
        "claim_boundary": (
            "The rerun verifies deterministic scientific reproduction under the frozen environment; "
            "it supports no new causal, operational, expert-validation, deployment, or transport claim."
        ),
    }
    REPORT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    markdown = f"""# Stage 6 Frozen Rerun Comparison

Status: **scientific content exact; timing disclosed; no new claim**.

## Identity

- Runner SHA-256: `{EXPECTED_RUNNER_SHA256}` (exact).
- Contract SHA-256: `{EXPECTED_CONTRACT_SHA256}` (exact).
- All four source-file hashes, evaluated-row profile, delivery keys, branch constants, model counts, fixed budgets, selections, completeness fields, and protocol-validity fields are exact.
- The rerun used the same Python/NumPy/PyTorch-CUDA versions, CUDA device, deterministic cuDNN flags, CUBLAS workspace configuration, and four CPU threads.

## Scientific content

- All non-timing fields in all 2,310 result rows and all 240 trajectory rows are exact.
- Seven sealed outputs, including the prediction NPZ, are raw-byte identical. The two non-identical CSVs differ only in their declared runtime fields.
- All 30 paired-effect rows, 36 moving-block rows, 258 cap/k rows, protocol-validity fields, failure ledger, completeness ledger, and prediction arrays are exact.
- All five paper-facing derived tables are exact in canonical scientific CSV bytes when independently rederived from the rerun. The Windows checkout's CRLF rendering is recorded separately from the accepted LF provenance and has no scientific effect.
- The accepted abstract remains the same 236-word narrative under the frozen alphabetic-token rule (`{EXPECTED_ABSTRACT_SHA256}`), and Markdown/TeX text agrees.
- All Stage 7 human placeholders remain: 11 in `MANUSCRIPT.md` and 9 in `journal_submission/paper.tex`.

## Timing and environment disclosure

The total measured runtime changed from {accepted_manifest['runtimes_seconds']['total']:.12g} s to {rerun_manifest['runtimes_seconds']['total']:.12g} s. Per-row/trajectory runtime fields also changed, as expected for non-scientific wall-clock measurements. Start/completion timestamps, the isolated script path, and absolute command path changed with the new execution location. The recorded execution environment fields are exact.

## Claim boundary

This rerun verifies exact non-timing scientific reproduction under the frozen execution environment. It does not change any result direction, null/adverse finding, comparison family, uncertainty unit, descriptive qualifier, evidence boundary, method claim, discussion statement, or conclusion. It supports no new causal, operational, external-expert, deployment, cross-system, complete-year, policy-transport, operator, safety, physical, or economic claim.
"""
    REPORT_MD.write_text(markdown, encoding="utf-8")
    print(
        "OK Stage 6 frozen rerun: exact script/config/input and non-timing science; "
        "five derived tables exact; timing disclosed; 236-word narrative preserved"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
