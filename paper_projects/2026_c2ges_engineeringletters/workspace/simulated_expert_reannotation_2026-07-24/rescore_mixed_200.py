#!/usr/bin/env python3
"""Rescore frozen predictions on the mixed 200-question versioned dataset."""

from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean

import rescore_existing_predictions as common


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DATASET = (
    PROJECT
    / "workspace"
    / "verification_pilot"
    / "agent_audit_40doc_simexpert75"
)


def main() -> None:
    gold = {}
    qmeta = {}
    for path in sorted(DATASET.glob("nerc_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for q in doc["causal_questions"]:
            gold[q["qid"]] = {
                "qid": q["qid"],
                "doc_id": doc["doc_id"],
                "role": q["role"],
                "evidence_sentence_ids": q["evidence_sentence_ids"],
                "label_status": q["verification_status"],
            }
            qmeta[q["qid"]] = {
                "question": q["question"],
                "sentences": doc["sentences"],
            }
    if len(gold) != 200:
        raise RuntimeError(f"Expected 200 questions, got {len(gold)}")

    predictions = defaultdict(dict)
    for row in common.read_jsonl(common.MAIN_DETAILS):
        if row["condition"] in common.CONDITIONS:
            predictions[row["condition"]][row["qid"]] = row["predicted_sentence_ids"]
    for condition, path in common.EXTRA_DETAILS.items():
        for row in common.read_jsonl(path):
            predictions[condition][row["qid"]] = row["predicted_sentence_ids"]
    for qid, meta in qmeta.items():
        predictions["bm25_query"][qid] = common.bm25_scores(
            meta["question"], meta["sentences"]
        )

    details = []
    for condition in common.CONDITIONS:
        if set(gold) - set(predictions[condition]):
            raise RuntimeError(f"Missing predictions for {condition}")
        for qid, label in gold.items():
            pred = predictions[condition][qid]
            p, r, f = common.prf(pred, label["evidence_sentence_ids"])
            hit, mrr, ndcg = common.rank_metrics(
                pred, label["evidence_sentence_ids"]
            )
            details.append(
                {
                    "condition": condition,
                    **label,
                    "predicted_sentence_ids": pred,
                    "evidence_precision": p,
                    "evidence_recall": r,
                    "evidence_f1": f,
                    "hit_at_3": hit,
                    "mrr_at_3": mrr,
                    "ndcg_at_3": ndcg,
                }
            )
    by_condition = defaultdict(list)
    for row in details:
        by_condition[row["condition"]].append(row)
    metrics = {
        condition: {
            metric: mean(row[metric] for row in by_condition[condition])
            for metric in [
                "evidence_precision",
                "evidence_recall",
                "evidence_f1",
                "hit_at_3",
                "mrr_at_3",
                "ndcg_at_3",
            ]
        }
        for condition in common.CONDITIONS
    }

    docs = sorted({row["doc_id"] for row in gold.values()})
    by_cond_doc = defaultdict(lambda: defaultdict(list))
    for row in details:
        by_cond_doc[row["condition"]][row["doc_id"]].append(row["evidence_f1"])
    rng = random.Random(common.BOOTSTRAP_SEED)
    comparisons = {}
    for other in [c for c in common.CONDITIONS if c != "c2ges_full"]:
        delta = {
            doc: mean(by_cond_doc["c2ges_full"][doc])
            - mean(by_cond_doc[other][doc])
            for doc in docs
        }
        samples = [
            mean(delta[rng.choice(docs)] for _ in docs)
            for _ in range(common.BOOTSTRAP_SAMPLES)
        ]
        comparisons[f"c2ges_full_vs_{other}"] = {
            "mean_f1_difference": mean(delta.values()),
            "ci95": [
                common.percentile(samples, 0.025),
                common.percentile(samples, 0.975),
            ],
            "bootstrap_two_sided_p": 2
            * min(
                sum(value <= 0 for value in samples) / len(samples),
                sum(value >= 0 for value in samples) / len(samples),
            ),
        }
    output = {
        "label_provenance": (
            "75 simulated-expert-adjudicated labels plus 125 original "
            "agent-verified candidate labels; no human gold"
        ),
        "documents": 40,
        "questions": 200,
        "aggregate_metrics": metrics,
        "paired_document_bootstrap": comparisons,
    }
    (HERE / "mixed_200_rescore_results.json").write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (HERE / "mixed_200_rescored_details.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in details) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# Mixed-Label 200-Question Rescore",
        "",
        "75 labels are AI simulated-expert adjudications; 125 retain the original",
        "agent-verified candidate labels. No label is human gold.",
        "",
        "| Method | F1 | Precision | Recall | Hit@3 | MRR@3 | nDCG@3 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for condition in common.CONDITIONS:
        m = metrics[condition]
        lines.append(
            f"| {condition} | {m['evidence_f1']:.4f} | "
            f"{m['evidence_precision']:.4f} | {m['evidence_recall']:.4f} | "
            f"{m['hit_at_3']:.4f} | {m['mrr_at_3']:.4f} | {m['ndcg_at_3']:.4f} |"
        )
    lines.extend(["", "## Full C2GES paired document bootstrap", ""])
    for name, comp in comparisons.items():
        lines.append(
            f"- {name}: {comp['mean_f1_difference']:+.4f}, "
            f"95% CI [{comp['ci95'][0]:+.4f}, {comp['ci95'][1]:+.4f}], "
            f"p={comp['bootstrap_two_sided_p']:.4f}"
        )
    (HERE / "mixed_200_rescore_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
