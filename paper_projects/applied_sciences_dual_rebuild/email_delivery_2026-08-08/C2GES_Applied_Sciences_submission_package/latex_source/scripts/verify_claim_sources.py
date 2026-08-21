#!/usr/bin/env python3
"""Fail closed when manuscript claims detach from canonical evidence."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve()
MANUSCRIPT = HERE.parent.parent
ROOT = next(p for p in HERE.parents if (p / "paper_projects").is_dir())
TEX = MANUSCRIPT / "paper_applsci.tex"
MAP = MANUSCRIPT / "generated/claim_source_map.json"


def sha(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fail(message):
    print(f"FAIL: {message}")
    return 1


def main():
    errors = 0
    text = TEX.read_text(encoding="utf-8")
    mapping = json.loads(MAP.read_text(encoding="utf-8"))
    for name, spec in mapping["sources"].items():
        path = ROOT / spec["path"]
        if not path.is_file() or sha(path) != spec["sha256"]:
            errors += fail(f"source hash mismatch: {name}: {path}")
    required_extended_sources = {
        "addon_protocol_freeze", "addon_results", "addon_manifest",
        "addon_primary_contrasts", "addon_primary_table",
        "exploratory_protocol_freeze", "exploratory_manifest",
        "exploratory_validation", "exploratory_primary_contrasts",
        "exploratory_primary_figure", "canonical_gzip_transition",
        "bge_protocol_freeze", "bge_results", "bge_artifact_manifest",
        "bge_validation", "bge_cell_summary", "bge_primary_contrasts",
        "bge_primary_table", "bge_predictions", "bge_provenance",
        "bge_resources",
        "upstream_matrix_protocol_freeze", "upstream_matrix_protocol_clarification",
        "upstream_matrix_analysis_freeze", "upstream_matrix_run_success",
        "upstream_matrix_results", "upstream_matrix_validation", "upstream_matrix_cells",
        "upstream_matrix_independent_audit", "upstream_matrix_independent_report",
    }
    missing_extended = sorted(required_extended_sources - set(mapping["sources"]))
    if missing_extended:
        errors += fail("extended evidence sources absent from claim map: " + ", ".join(missing_extended))
    for name, digest in mapping["generated"].items():
        path = MANUSCRIPT / "generated" / name
        if not path.is_file() or sha(path) != digest:
            errors += fail(f"generated fragment mismatch: {name}")

    required = [
        r"\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}",
        r"\input{generated/canonical_numbers.tex}",
        r"\dataavailability{", r"\authorcontributions{", r"\funding{",
        r"\conflictsofinterest{",
        "Liu Bijing $^{1,2}$ and Yang Yong",
        "Conceptualization, B.L. and Y.Y.; methodology, B.L.",
        "During preparation of this manuscript, the authors used OpenAI Codex",
        "conditional, non-end-to-end",
        "Neither the predefined role-effect criterion",
        "At label-blind $K=3$, the MiniLM cross-encoder difference was +0.0102",
        "with Holm-adjusted $p=0.1877$",
        r"\subsection{Independent BGE Strong-Baseline Comparison}",
        "These percentile ranges are composition-sensitivity intervals, not population confidence intervals.",
        r"\input{generated/table_bge_contrasts.tex}",
        r"\input{generated/table_structural_neural_contrasts.tex}",
        r"\subsection{Crossed Upstream--Downstream Seed Sensitivity}",
        r"\input{generated/table_upstream_seed_matrix.tex}",
        "none of the three BGE comparisons supports a promoted difference",
        "all nine existing modes",
        "long-term accessibility additionally requires deposit in a permanent public archive",
    ]
    for token in required:
        if token not in text:
            errors += fail(f"required boundary missing: {token}")
    forbidden = [
        "0.5066", "0.5030", "0.0099", "4000 training", "800 development",
        "significant no-role ablation gap", "role contribution is useful",
        "W7\\_FRONT\\_MATTER", "agent-produced", "generated and checked by agents",
        "Round-3 add-on", "canonical v2", "canonical W6", "demonstrates validated power-grid performance",
    ]
    for token in forbidden:
        if token.lower() in text.lower():
            errors += fail(f"superseded or prohibited claim found: {token}")

    bib = (MANUSCRIPT / "references_cited_verified.bib").read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", bib))
    cited = set()
    for group in re.findall(r"\\cite[pt]?\{([^}]+)\}", text):
        cited.update(k.strip() for k in group.split(","))
    missing = sorted(cited - bib_keys)
    if missing:
        errors += fail("missing bibliography keys: " + ", ".join(missing))
    bib_blocks = {m.group(1): m.group(0) for m in re.finditer(r"@[A-Za-z]+\s*\{\s*([^,\s]+),.*?\n\}", bib, re.S)}
    for key in sorted(cited):
        block = bib_blocks.get(key, "")
        has_doi = bool(re.search(r"\n\s*doi\s*=", block, re.I))
        has_primary_non_doi = (
            "archivePrefix = {arXiv}" in block
            or "www.nerc.com/" in block
        )
        if not (has_doi or has_primary_non_doi):
            errors += fail(f"cited entry lacks structured DOI or verified primary non-DOI URL: {key}")
        if "CrossRef" in block and "note =" in block:
            errors += fail(f"legacy DOI-in-note field remains in cited entry: {key}")

    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    for rel in figures:
        if not (MANUSCRIPT / rel).is_file():
            errors += fail(f"missing figure: {rel}")
    if len(figures) != 9:
        errors += fail(f"expected 8 accepted/canonical figures plus 1 hash-bound exploratory figure, found {len(figures)}")
    exploratory_source = ROOT / mapping["sources"]["exploratory_primary_figure"]["path"]
    exploratory_target = MANUSCRIPT / "figures/results/fig06_exploratory_forest.pdf"
    if not exploratory_target.is_file() or sha(exploratory_target) != sha(exploratory_source):
        errors += fail("isolated-manuscript exploratory figure differs from its hash-bound source")

    decisions = mapping["claim_decisions"]
    if decisions["role_conditioning_primary_claim"]["decision"] != "NO-GO":
        errors += fail("canonical role decision is not NO-GO")
    if decisions["blanket_superiority_over_bm25"]["decision"] != "NO-GO":
        errors += fail("canonical BM25 decision is not NO-GO")

    bge_validation = json.loads((ROOT / mapping["sources"]["bge_validation"]["path"]).read_text(encoding="utf-8"))
    if bge_validation.get("decision") != "PASS_INTEGRATION":
        errors += fail("BGE independent validation did not pass")
    bge_text = text[text.index(r"\subsection{Independent BGE Strong-Baseline Comparison}"):text.index(r"\subsection{Role-Effect Decision}")]
    if "NERC" in bge_text or "power-grid" in bge_text:
        errors += fail("BGE quantitative subsection exceeds the FEVER-only boundary")

    if errors:
        print(f"Claim/source verification failed with {errors} error(s).")
        return 1
    print(f"PASS: {len(mapping['sources'])} source hashes, {len(mapping['generated'])} generated fragments, {len(figures)} figures, and {len(cited)} citation keys verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
