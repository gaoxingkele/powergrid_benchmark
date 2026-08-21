#!/usr/bin/env python3
"""Create the complete local C2GES reproducibility manifest.

The manifest references retained local artifacts; it does not imply redistribution
permission or substitute for the permanent DOI required before submission.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve()
MANUSCRIPT = HERE.parent.parent
ROOT = next(p for p in HERE.parents if (p / "paper_projects").is_dir())
PROJECT = ROOT / "paper_projects/2026_c2ges_engineeringletters"
REBUILD_C2 = MANUSCRIPT.parent
OUT = HERE.parent / "bundle_manifest.json"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def files_under(path: Path):
    return sorted(p for p in path.rglob("*") if p.is_file())


def main() -> None:
    individual = [
        PROJECT / "source/code/c2ges_learnable.py",
        PROJECT / "source/code/predict_fever_labels.py",
        PROJECT / "source/code/prepare_fever_benchmark.py",
        PROJECT / "source/code/run_c2_protocol_pilot.py",
        PROJECT / "source/code/aggregate_c2_w4_five_seed.py",
        PROJECT / "source/code/w4_freeze_guard.py",
        PROJECT / "source/code/requirements.txt",
        MANUSCRIPT / "evidence/conversion_audit.json",
        MANUSCRIPT / "evidence/method_implementation_contract.json",
        MANUSCRIPT / "evidence/canonical_gzip_transition.json",
        HERE.parent / "environment_lock.txt",
        HERE.parent / "create_bundle_manifest.py",
        HERE.parent / "verify_local_bundle.py",
        HERE.parent / "verify_canonical_gzip.py",
        HERE.parent / "verify_bundle.ps1",
        MANUSCRIPT / "paper_applsci.tex",
        MANUSCRIPT / "references_cited_verified.bib",
        MANUSCRIPT / "build.ps1",
        MANUSCRIPT / "README.md",
        MANUSCRIPT / "build/paper_applsci.pdf",
    ]
    trees = [
        PROJECT / "workspace/fever_benchmark_document_grouped",
        PROJECT / "workspace/w3_c2_pilot/full_8000_1500_1500",
        PROJECT / "workspace/w4_c2_five_seed",
        PROJECT / "workspace/w6_c2_canonical_v2",
        MANUSCRIPT / "Definitions",
        MANUSCRIPT / "figures",
        MANUSCRIPT / "generated",
        MANUSCRIPT / "scripts",
        REBUILD_C2 / "exploratory_v3",
        REBUILD_C2 / "addon_round3",
        REBUILD_C2 / "bge_expansion_20260806",
        REBUILD_C2 / "upstream_uncertainty_20260806",
    ]
    paths = {p.resolve() for p in individual if p.is_file()}
    for tree in trees:
        paths.update(p.resolve() for p in files_under(tree))
    records = []
    for path in sorted(paths, key=lambda p: p.as_posix().lower()):
        records.append({
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        })
    payload = {
        "schema_version": "1.0",
        "status": "complete_local_manifest_generated_and_verified_after_manuscript_build",
        "public_doi": None,
        "public_doi_blocker": "Human repository selection, license review, upload, and DOI minting required before submission.",
        "known_provenance_limitations": [
            "The Hugging Face source dataset revision was not recorded by the original converter.",
            "The three external Hugging Face cache Arrow files are not redistributed in this bundle; their exact byte sizes and SHA-256 hashes are recorded in evidence/conversion_audit.json.",
            "OOF upstream fold models were not serialized; only the final all-training model and complete prediction ledger remain.",
            "The execution git worktree was dirty; executable file hashes, not the commit alone, define the run code.",
            "A prior gzip byte hash is documented in evidence/canonical_gzip_transition.json. The prior compressed artifact is unavailable, so cross-version decompressed identity is not claimed; current payload identity and numerical invariance are verified.",
        ],
        "artifact_count": len(records),
        "total_bytes": sum(r["bytes"] for r in records),
        "artifacts": records,
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"WROTE {OUT}: {len(records)} artifacts, {payload['total_bytes']} bytes")


if __name__ == "__main__":
    main()
