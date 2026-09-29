"""Protocol v2 arms on the external corpus: role layer, path layer, equal-unit and Lead.

The v2 run compared only Full vs no-path (the path channel) at matched word
budgets.  The plan requires three further arms so that the pre-declared criteria
can actually be tested:

  AB0  lexical relevance + position only
  AB1  AB0 + role evidence (no role-group reservation)
  AB2  AB1 + role-group reservation           <- role layer = AB2 - AB0
  no-path / Full                              <- path layer = Full - no-path
  TextRank / Lead                             <- comparators

Budgets: matched word (110/260) and matched unit count (K=5/10), the latter being
the protocol that made the historical comparison look strong.

Everything runs on the frozen corpus built by run_external_prospective_v2.py
(same summary rule and deduplication), with no tuning on outcomes.

Usage:
    python -B run_external_arms_v3.py --json external_arms_v3.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _code_dir() -> Path:
    """Locate the shared analysis code from either the release layout or a working copy."""
    for parent in (HERE, *HERE.parents):
        candidate = parent / "03_Reproducibility" / "Code" / "rsi_path_v1"
        if candidate.is_dir():
            return candidate
    raise RuntimeError("cannot locate 03_Reproducibility/Code/rsi_path_v1")


sys.path.insert(0, str(_code_dir()))
sys.path.insert(0, str(HERE))
import rsi_common as R  # noqa: E402
import run_external_prospective_v2 as V2  # noqa: E402
from path_utilities import apply_utility  # noqa: E402

WEIGHTS = {
    "AB0": {"relevance": 0.40, "position": 0.10},
    "AB1": {"relevance": 0.40, "role": 0.20, "position": 0.10},
    "no_path": {"relevance": 0.40, "role": 0.20, "graph": 0.15, "position": 0.10},
}
PATH_WEIGHT = 0.10


def base_scores(prepared, weights, path_weight: float = 0.0):
    graph = prepared["graph"]
    channels = dict(prepared["channels"])
    effective = dict(weights)
    if path_weight > 0:
        channels["path"] = apply_utility(
            "historical", prepared["raw_path"], graph.nodes, channels["relevance"], prepared["word_counts"]
        )
        effective["path"] = path_weight
    else:
        channels["path"] = {node.sid: 0.0 for node in graph.nodes}
    total = sum(effective.values())
    norm = {name: value / total for name, value in effective.items()}
    return {
        node.sid: sum(norm[name] * float(channels[name][node.sid]) for name in norm)
        for node in graph.nodes
    }


def select_units(nodes, scores, k: int, *, reservation: bool, role_groups=None):
    """Unit-count budget: reserve one unit per role group, then fill by score."""
    by_sid = {n.sid: n for n in nodes}
    selected: list[str] = []
    if reservation and k >= 3 and role_groups:
        for roles in role_groups.values():
            eligible = [n for n in nodes if n.sid not in selected and n.dominant_role in roles]
            if eligible and len(selected) < k:
                selected.append(max(eligible, key=lambda n: (scores[n.sid], -n.position)).sid)
    for node in sorted(nodes, key=lambda n: (-scores[n.sid], n.position, n.sid)):
        if len(selected) >= k:
            break
        if node.sid not in selected:
            selected.append(node.sid)
    ordered = sorted((by_sid[s] for s in selected), key=lambda n: n.position)
    return ordered


def lead_scores(nodes):
    return {node.sid: -float(node.position) for node in nodes}


def run_condition(prepared, condition: str, budget_kind: str, budget: int, textrank_settings):
    nodes = prepared["graph"].nodes
    if condition == "Lead":
        scores = lead_scores(nodes)
        if budget_kind == "word":
            ordered, _ = R.select_ranking_word_budget(nodes, scores, budget)
        else:
            ordered = select_units(nodes, scores, budget, reservation=False)
    elif condition == "TextRank":
        scores = R.textrank_scores(nodes, textrank_settings)
        if budget_kind == "word":
            ordered, _ = R.select_ranking_word_budget(nodes, scores, budget)
        else:
            ordered = select_units(nodes, scores, budget, reservation=False)
    elif condition == "AB0":
        scores = base_scores(prepared, WEIGHTS["AB0"])
        if budget_kind == "word":
            ordered, _ = R.select_word_budget(nodes, scores, budget, reservation=False, redundancy_penalty=0.50)
        else:
            ordered = select_units(nodes, scores, budget, reservation=False)
    elif condition == "AB1":
        scores = base_scores(prepared, WEIGHTS["AB1"])
        if budget_kind == "word":
            ordered, _ = R.select_word_budget(nodes, scores, budget, reservation=False, redundancy_penalty=0.50)
        else:
            ordered = select_units(nodes, scores, budget, reservation=False)
    elif condition == "AB2":
        scores = base_scores(prepared, WEIGHTS["AB1"])
        if budget_kind == "word":
            ordered, _ = R.select_word_budget(nodes, scores, budget, reservation=True, redundancy_penalty=0.50)
        else:
            ordered = select_units(nodes, scores, budget, reservation=True, role_groups=R.ROLE_GROUPS)
    elif condition == "no_path":
        scores = base_scores(prepared, WEIGHTS["no_path"])
        if budget_kind == "word":
            ordered, _ = R.select_word_budget(nodes, scores, budget, reservation=True, redundancy_penalty=0.50)
        else:
            ordered = select_units(nodes, scores, budget, reservation=True, role_groups=R.ROLE_GROUPS)
    elif condition == "Full":
        scores = base_scores(prepared, WEIGHTS["no_path"], path_weight=PATH_WEIGHT)
        if budget_kind == "word":
            ordered, _ = R.select_word_budget(nodes, scores, budget, reservation=True, redundancy_penalty=0.50)
        else:
            ordered = select_units(nodes, scores, budget, reservation=True, role_groups=R.ROLE_GROUPS)
    else:
        raise ValueError(condition)
    text = " ".join(node.text for node in ordered)
    return {"rougeL_f1": R.rouge_l_f1(text, prepared["reference"]), "units": len(ordered),
            "words": R.word_count(text)}


def randomized_signflip(values, draws: int = 100000, seed: int = 20260926):
    rng = random.Random(seed)
    observed = abs(statistics.fmean(values))
    hits = sum(
        1
        for _ in range(draws)
        if abs(statistics.fmean(v if rng.random() < 0.5 else -v for v in values)) >= observed - 1e-12
    )
    return (hits + 1) / (draws + 1)


def exact_signflip(values):
    n = len(values)
    if n > 20:
        return None
    observed = abs(statistics.fmean(values))
    hits = total = 0
    for signs in itertools.product((1, -1), repeat=n):
        total += 1
        if abs(statistics.fmean(s * v for s, v in zip(signs, values))) >= observed - 1e-12:
            hits += 1
    return hits / total


def holm(pvalues):
    order = sorted(range(len(pvalues)), key=lambda i: pvalues[i])
    out = [0.0] * len(pvalues)
    run = 0.0
    for rank, idx in enumerate(order):
        run = max(run, (len(pvalues) - rank) * pvalues[idx])
        out[idx] = min(1.0, run)
    return out


def contrast(rows, ref, cand, key):
    docs = sorted({r["doc_id"] for r in rows if r["condition"] == ref and r["key"] == key})
    diffs = []
    for doc in docs:
        a = next((r for r in rows if r["doc_id"] == doc and r["condition"] == ref and r["key"] == key), None)
        b = next((r for r in rows if r["doc_id"] == doc and r["condition"] == cand and r["key"] == key), None)
        if a and b:
            diffs.append(b["rougeL_f1"] - a["rougeL_f1"])
    if not diffs:
        return None
    neg = sum(1 for d in diffs if d < -1e-12)
    pos = sum(1 for d in diffs if d > 1e-12)
    zero = len(diffs) - neg - pos
    p = exact_signflip(diffs)
    if p is None:
        p = randomized_signflip(diffs)
    return {
        "contrast": f"{cand} - {ref}",
        "budget": key,
        "n": len(diffs),
        "mean": round(statistics.fmean(diffs), 6),
        "median": round(statistics.median(diffs), 6),
        "sd": round(statistics.pstdev(diffs), 6),
        "negative": neg,
        "positive": pos,
        "zero": zero,
        "positive_share_of_discordant": round(pos / (neg + pos), 3) if (neg + pos) else None,
        "p": round(p, 6),
        "min_attainable_p_holm": round(min(1.0, 4 * (2 / 2 ** len(diffs))), 6),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument(
        "--corpus-dir",
        type=Path,
        default=None,
        help="directory holding the converted Markdown reports (third-party text is not shipped)",
    )
    args = parser.parse_args()

    settings = R.load_protocol()["textrank"]
    corpus = args.corpus_dir or (HERE / "markdown")
    if not any(Path(corpus).glob("*.md")):
        raise SystemExit(f"no Markdown reports under {corpus}; pass --corpus-dir")
    built = []
    for md in sorted(Path(corpus).glob("*.md")):
        row = V2.build_report(md)
        if row:
            built.append(row)
    built.sort(key=lambda r: (-len(r["candidate_sentences"]), -len(r["reference_summary"].split()), r["doc_id"]))
    reports = []
    for row in built:
        if any(V2.is_same_incident(row["doc_id"], kept["doc_id"]) for kept in reports):
            continue
        reports.append(row)

    rows = []
    for row in reports:
        prepared = R.prepare_report(row)
        for kind, budget in (("word", 110), ("word", 260), ("unit", 5), ("unit", 10)):
            for condition in ("AB0", "AB1", "AB2", "no_path", "Full", "TextRank", "Lead"):
                result = run_condition(prepared, condition, kind, budget, settings)
                rows.append(
                    {
                        "doc_id": row["doc_id"],
                        "family": row["report_series_id"],
                        "condition": condition,
                        "kind": kind,
                        "budget": budget,
                        "key": f"{kind}:{budget}",
                        "rougeL_f1": result["rougeL_f1"],
                        "units": result["units"],
                    }
                )

    contrasts = []
    for kind, budget in (("word", 110), ("word", 260), ("unit", 5), ("unit", 10)):
        key = f"{kind}:{budget}"
        for cand, ref in (("AB2", "AB0"), ("AB1", "AB0"), ("Full", "no_path"), ("TextRank", "no_path"), ("Lead", "no_path")):
            item = contrast(rows, ref, cand, key)
            if item:
                contrasts.append(item)
    pvalues = [c["p"] for c in contrasts]
    for item, adjusted in zip(contrasts, holm(pvalues)):
        item["holm"] = round(adjusted, 6)

    means = {}
    for row in rows:
        key = f"{row['condition']}@{row['kind']}:{row['budget']}"
        means.setdefault(key, []).append(row["rougeL_f1"])
    summary = {k: {"n": len(v), "mean": round(statistics.fmean(v), 5)} for k, v in sorted(means.items())}

    payload = {
        "schema": "c2ges-external-arms-v3",
        "corpus": "same frozen external corpus as external_prospective_v2 (summary rule + date dedup)",
        "documents": len(reports),
        "families": sorted({r["report_series_id"] for r in reports}),
        "arms": {
            "AB0": "relevance + position",
            "AB1": "AB0 + role evidence",
            "AB2": "AB1 + role-group reservation (role layer = AB2-AB0)",
            "no_path": "AB2 + typed graph salience",
            "Full": "no_path + path deletion at weight 0.10 (path layer = Full-no_path)",
        },
        "means": summary,
        "contrasts": contrasts,
        "rows": rows,
    }
    Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"documents": payload["documents"], "families": payload["families"]}, indent=2))
    for item in contrasts:
        print(f"  {item['budget']:9s} {item['contrast']:22s} mean={item['mean']:+.5f} p={item['p']:.4f} "
              f"holm={item['holm']:.4f} neg/pos/zero={item['negative']}/{item['positive']}/{item['zero']} "
              f"pos_share={item['positive_share_of_discordant']}")


if __name__ == "__main__":
    main()
