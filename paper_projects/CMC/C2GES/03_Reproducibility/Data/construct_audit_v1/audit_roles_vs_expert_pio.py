"""Audit C2GES role heuristics against expert P/I/O sentence labels (EBM-NLP).

EBM-NLP/AbstRCT annotates PubMed RCT abstracts for Participants, Interventions
and Outcomes; the released test annotations were produced by medical
professionals. Two roles map onto C2GES role names without stretching:
intervention -> mitigation, outcome -> impact. Participant has no counterpart in
the C2GES role set and is reported as unmapped.

This is an adjacent-domain construct audit. It does not substitute for expert
adjudication of power-system report roles, and the cue lexicon is expected to
transfer poorly.

Usage:
    python -B audit_roles_vs_expert_pio.py --ebm-dir <dir> --json <out.json>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROLE_MAP = {"interventions": "mitigation", "outcomes": "impact"}


def default_core() -> Path:
    """Locate the shipped offline implementation without relying on absolute paths."""
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate / "03_Reproducibility" / "Code" / "core" / "c2ges_offline.py"
    return Path("03_Reproducibility/Code/core/c2ges_offline.py")


def load_core(path: Path):
    spec = importlib.util.spec_from_file_location("c2ges_offline", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["c2ges_offline"] = module
    spec.loader.exec_module(module)
    return module


def sentences(tokens: list[str]) -> list[tuple[int, int, str]]:
    out, start = [], 0
    for index, token in enumerate(tokens):
        if token in {".", "?", "!"} or token.endswith((".\"", "?)", "!\"'", ".)")):
            text = " ".join(tokens[start : index + 1]).strip()
            if text:
                out.append((start, index, text))
            start = index + 1
    if start < len(tokens):
        text = " ".join(tokens[start:]).strip()
        if text:
            out.append((start, len(tokens) - 1, text))
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ebm-dir", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--core", default=None, help="path to c2ges_offline.py (default: release-relative)")
    args = parser.parse_args()

    ebm = Path(args.ebm_dir)
    core = load_core(Path(args.core) if args.core else default_core())
    ann_root = ebm / "annotations" / "aggregated" / "starting_spans"

    docs = sorted(p.stem for p in (ebm / "documents").glob("*.tokens"))
    stats = {label: {"tp": 0, "fp": 0, "fn": 0, "tn": 0, "pos": 0} for label in ROLE_MAP}
    sentences_total = with_role = 0
    docs_used = 0
    for doc in docs:
        labels = {}
        for label in ROLE_MAP:
            path = ann_root / label / "test" / "crowd" / f"{doc}_AGGREGATED.ann"
            if not path.is_file():
                labels = {}
                break
            labels[label] = [x.strip() == "1" for x in path.read_text(encoding="utf-8-sig").split(",")]
        if not labels:
            continue
        tokens = (ebm / "documents" / f"{doc}.tokens").read_text(encoding="utf-8", errors="replace").split()
        if not tokens:
            continue
        if any(len(labels[label]) != len(tokens) for label in ROLE_MAP):
            continue
        docs_used += 1
        for start, end, text in sentences(tokens):
            sentences_total += 1
            scores = {role: core._role_hits(text, role) for role in core.ROLES}
            best = max(scores.values()) if scores else 0
            dominant = next((r for r in core.ROLES if scores[r] == best), None) if best > 0 else None
            if dominant:
                with_role += 1
            for label, role in ROLE_MAP.items():
                human = any(labels[label][start : end + 1])
                pred = dominant == role
                cell = stats[label]
                if human:
                    cell["pos"] += 1
                if pred and human:
                    cell["tp"] += 1
                elif pred and not human:
                    cell["fp"] += 1
                elif not pred and human:
                    cell["fn"] += 1
                else:
                    cell["tn"] += 1

    report = {
        "schema": "c2ges-role-construct-audit-ebm-v1",
        "source": "EBM-NLP (AbstRCT) aggregated starting-span labels; test split annotated by medical professionals",
        "scope": "adjacent-domain construct audit; not power-system expert gold",
        "documents_used": docs_used,
        "sentences": sentences_total,
        "sentences_with_dominant_role": with_role,
        "unit_role_coverage": round(with_role / sentences_total, 4) if sentences_total else None,
        "role_map": ROLE_MAP,
        "per_role": {},
    }
    for label, role in ROLE_MAP.items():
        cell = stats[label]
        precision = cell["tp"] / (cell["tp"] + cell["fp"]) if (cell["tp"] + cell["fp"]) else None
        recall = cell["tp"] / (cell["tp"] + cell["fn"]) if (cell["tp"] + cell["fn"]) else None
        report["per_role"][f"{label}->{role}"] = {
            **cell,
            "precision": round(precision, 4) if precision else None,
            "recall": round(recall, 4) if recall else None,
            "base_rate": round(cell["pos"] / sentences_total, 4) if sentences_total else None,
        }
    Path(args.json).write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
