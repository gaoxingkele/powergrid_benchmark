"""Audit C2GES typed edges against human-annotated discourse relations (GUM eRST).

What this measures: among the typed edges the deterministic role/transition rule
produces on GUM elementary discourse units, what share corresponds to a
human-annotated evidence-chain relation (causal, purpose, condition, explanation)
between the same two units -- compared with the base rate of those relations in
the same annotation set.

What this does NOT measure: expert adjudication of NERC report roles, paths,
faithfulness or omissions. GUM is multi-genre (academic, conversation, essay,
fiction, court, reddit, speech, vlog, whow). This is a construct audit on an
adjacent human-annotated corpus, not domain expert gold.

Usage:
    python -B audit_typed_edges_vs_human_rst.py --gum-dir <dir> --json <out.json>
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

EVIDENCE_CHAIN = {"causal", "purpose", "condition", "explanation", "contingency"}
MAX_DISTANCE = 12  # the paper's declared 12-position edge horizon


def default_core() -> Path:
    """Locate the shipped offline implementation without relying on absolute paths."""
    for candidate in (Path(__file__).resolve(), *Path(__file__).resolve().parents):
        marker = candidate / "C2GES_RELEASE_MARKER.json"
        if marker.is_file():
            return candidate / "03_Reproducibility" / "Code" / "core" / "c2ges_offline.py"
    return Path("03_Reproducibility/Code/core/c2ges_offline.py")


def load_core(path: Path):
    spec = importlib.util.spec_from_file_location("c2ges_offline", path)
    module = importlib.util.module_from_spec(spec)
    # dataclasses resolve the defining module through sys.modules
    sys.modules["c2ges_offline"] = module
    spec.loader.exec_module(module)
    return module


def parse_edus(tok_path: Path) -> dict[str, list[str]]:
    """Segment documents into elementary discourse units using the Seg=B-seg mark."""
    docs: dict[str, list[str]] = defaultdict(list)
    buffers: dict[str, list[str]] = defaultdict(list)
    current: str | None = None
    for line in tok_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# newdoc id = "):
            current = line.split("=", 1)[1].strip()
            buffers[current] = []
            continue
        if not line.strip() or current is None:
            continue
        parts = line.split("\t")
        if len(parts) < 10:
            continue
        token, seg = parts[1], parts[9]
        if seg.startswith("Seg=B-seg") and buffers[current]:
            docs[current].append(" ".join(buffers[current]))
            buffers[current] = []
        buffers[current].append(token)
        if seg.startswith("Seg=E-seg"):
            docs[current].append(" ".join(buffers[current]))
            buffers[current] = []
    for doc, buffer in buffers.items():
        if buffer:
            docs[doc].append(" ".join(buffer))
    return {doc: [u for u in units if u.strip()] for doc, units in docs.items()}


def parse_relations(rels_path: Path) -> dict[str, dict[tuple[str, str], str]]:
    """Human relations keyed by the normalized (unit1, unit2) tokenized texts."""
    rows = [l.split("\t") for l in rels_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    header = rows[0]
    index = {name: i for i, name in enumerate(header)}
    out: dict[str, dict[tuple[str, str], str]] = defaultdict(dict)
    for row in rows[1:]:
        if len(row) <= index["label"]:
            continue
        u1 = re.sub(r"\s+", " ", row[index["unit1_txt"]]).strip()
        u2 = re.sub(r"\s+", " ", row[index["unit2_txt"]]).strip()
        label = row[index["label"]].strip()
        direction = row[index["dir"]].strip()
        out[row[index["doc"]]][(u1, u2)] = label
        out[row[index["doc"]]][(u2, u1)] = label
        out[row[index["doc"]]][f"{u1}|{u2}|{direction}"] = label  # directional view
    return out


def dominant_roles(core, units: list[str]) -> list[str | None]:
    raw = {role: [core._role_hits(text, role) for text in units] for role in core.ROLES}
    scaled = {role: core._unit_scale(values) for role, values in raw.items()}
    dominants: list[str | None] = []
    for i in range(len(units)):
        best = max(scaled[role][i] for role in core.ROLES)
        dominants.append(
            next((role for role in core.ROLES if scaled[role][i] == best), None) if best > 0 else None
        )
    return dominants


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--gum-dir", required=True)
    parser.add_argument("--json", required=True)
    parser.add_argument("--core", default=None, help="path to c2ges_offline.py (default: release-relative)")
    args = parser.parse_args()

    gum = Path(args.gum_dir)
    core = load_core(Path(args.core) if args.core else default_core())
    print("roles:", list(core.ROLES))
    print("transitions:", len(core.CAUSAL_TRANSITIONS))

    edus = parse_edus(gum / "eng.erst.gum_dev.tok")
    edus.update(parse_edus(gum / "eng.erst.gum_test.tok"))
    rels = parse_relations(gum / "eng.erst.gum_dev.rels")
    rels.update(parse_relations(gum / "eng.erst.gum_test.rels"))

    label_counts = Counter(value for per_doc in rels.values() for key, value in per_doc.items()
                           if isinstance(key, tuple))
    base_chain = sum(count for label, count in label_counts.items() if label in EVIDENCE_CHAIN)
    base_total = sum(label_counts.values())

    # Design v2. The annotated relation pairs of GUM are the population: for every
    # human-labelled pair we ask whether the deterministic role rule would admit an
    # edge between the two units. That yields interpretable precision/recall on a
    # sample of human judgements instead of a handful of string-matched edges.
    rows = []
    for name in ("eng.erst.gum_dev.rels", "eng.erst.gum_test.rels"):
        raw = [l.split("\t") for l in (gum / name).read_text(encoding="utf-8").splitlines() if l.strip()]
        header = {key: i for i, key in enumerate(raw[0])}
        for row in raw[1:]:
            if len(row) <= header["label"]:
                continue
            rows.append({
                "doc": row[header["doc"]],
                "u1": re.sub(r"\s+", " ", row[header["unit1_txt"]]).strip(),
                "u2": re.sub(r"\s+", " ", row[header["unit2_txt"]]).strip(),
                "label": row[header["label"]].strip(),
                "direction": row[header["dir"]].strip(),
            })

    role_cache: dict[str, str | None] = {}

    def role_of(text: str) -> str | None:
        if text not in role_cache:
            scores = {role: core._role_hits(text, role) for role in core.ROLES}
            best = max(scores.values()) if scores else 0
            role_cache[text] = (
                next((role for role in core.ROLES if scores[role] == best), None) if best > 0 else None
            )
        return role_cache[text]

    position: dict[str, dict[str, int]] = {
        doc: {text: index for index, text in enumerate(units)} for doc, units in edus.items()
    }

    truth_pos = truth_neg = pred_pos = pred_neg = 0
    tp = fp = fn = tn = 0
    covered = 0
    window_excluded = 0
    label_by_prediction: Counter = Counter()
    per_doc_rows = []
    for row in rows:
        doc, u1, u2, label = row["doc"], row["u1"], row["u2"], row["label"]
        r1, r2 = role_of(u1), role_of(u2)
        human_chain = label in EVIDENCE_CHAIN
        if human_chain:
            truth_pos += 1
        else:
            truth_neg += 1
        if r1 is None or r2 is None:
            # No role evidence for at least one unit: the rule cannot fire.
            admissible = False
        else:
            covered += 1
            admissible = (r1, r2) in core.CAUSAL_TRANSITIONS
            if admissible and doc in position:
                p1 = position[doc].get(u1)
                p2 = position[doc].get(u2)
                if p1 is not None and p2 is not None and abs(p1 - p2) > MAX_DISTANCE:
                    admissible = False
                    window_excluded += 1
        if admissible:
            pred_pos += 1
            label_by_prediction[label] += 1
        else:
            pred_neg += 1
        if admissible and human_chain:
            tp += 1
        elif admissible and not human_chain:
            fp += 1
        elif not admissible and human_chain:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    base_rate = truth_pos / (truth_pos + truth_neg) if (truth_pos + truth_neg) else None
    lift = (precision / base_rate) if precision and base_rate else None

    result = {
        "schema": "c2ges-typed-edge-construct-audit-v1",
        "source": "GUM eRST discourse relations (DISRPT .rels, human annotation)",
        "scope": "construct audit on an adjacent multi-genre corpus; not domain expert gold",
        "design": "population = human-labelled relation pairs; predictor = role-compatibility rule (+12-unit window when positions resolve)",
        "max_edge_distance": MAX_DISTANCE,
        "documents": len(edus),
        "edu_total": sum(len(u) for u in edus.values()),
        "human_relation_pairs": truth_pos + truth_neg,
        "human_evidence_chain_pairs": truth_pos,
        "human_evidence_chain_base_rate": round(base_rate, 4) if base_rate else None,
        "pairs_with_role_evidence_both_units": covered,
        "role_coverage": round(covered / (truth_pos + truth_neg), 4) if (truth_pos + truth_neg) else None,
        "predicted_edges": pred_pos,
        "window_excluded_edges": window_excluded,
        "confusion": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
        "precision": round(precision, 4) if precision else None,
        "recall": round(recall, 4) if recall else None,
        "lift_vs_base_rate": round(lift, 2) if lift else None,
        "labels_among_predicted_edges": label_by_prediction.most_common(),
        "per_document": per_doc_rows,
    }
    Path(args.json).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k not in {"per_document", "matched_relation_labels"}},
                     indent=2))
    print("labels among predicted edges:", label_by_prediction.most_common(10))


if __name__ == "__main__":
    main()
