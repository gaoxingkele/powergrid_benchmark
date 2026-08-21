#!/usr/bin/env python3
"""Build auditable mixed-40doc and simulated-expert-only 15doc datasets."""

from __future__ import annotations

import json
import shutil
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
SOURCE = WORKSPACE / "verification_pilot" / "agent_audit_40doc"
MIXED = WORKSPACE / "verification_pilot" / "agent_audit_40doc_simexpert75"
SUBSET = WORKSPACE / "verification_pilot" / "simulated_expert_subset_15doc"


def main() -> None:
    labels = {
        row["qid"]: row
        for row in (
            json.loads(line)
            for line in (HERE / "adjudicated_labels.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line.strip()
        )
    }
    selection = json.loads(
        (HERE / "selection_manifest.json").read_text(encoding="utf-8")
    )
    selected_docs = set(selection["documents"])
    if len(labels) != 75 or len(selected_docs) != 15:
        raise RuntimeError("Expected 75 adjudicated labels across 15 documents")

    for output in [MIXED, SUBSET]:
        output.mkdir(parents=True, exist_ok=True)

    source_manifest = json.loads((SOURCE / "manifest.json").read_text(encoding="utf-8"))
    replacement_count = 0
    for path in sorted(SOURCE.glob("nerc_*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        for question in doc["causal_questions"]:
            label = labels.get(question["qid"])
            if label is None:
                continue
            question["evidence_sentence_ids_original_agent_candidate"] = question[
                "evidence_sentence_ids"
            ]
            question["answer_original_agent_candidate"] = question.get("answer", "")
            question["evidence_sentence_ids"] = label["evidence_sentence_ids"]
            question["answer"] = label["answer_summary"]
            question["verification_status"] = "simulated_expert_adjudicated"
            question["verification"] = "simulated_expert_adjudicated"
            question["source_annotation"] = (
                "three_independent_AI_simulated_experts_sentence_majority_adjudicated"
            )
            question["simulated_expert_disclosure"] = (
                "AI simulated-expert labels; not human or expert gold"
            )
            question["simulated_expert_confidence"] = label["confidence"]
            question["simulated_expert_adjudication"] = label["adjudication"]
            replacement_count += 1
        if doc["doc_id"] in selected_docs:
            doc["dataset_status"] = "simulated_expert_adjudicated_not_human_gold"
        text = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
        (MIXED / path.name).write_text(text, encoding="utf-8")
        if doc["doc_id"] in selected_docs:
            (SUBSET / path.name).write_text(text, encoding="utf-8")

    if replacement_count != 75:
        raise RuntimeError(f"Expected 75 replacements, got {replacement_count}")

    mixed_manifest = {
        **source_manifest,
        "name": "nerc_causal_qa_40doc_mixed_simexpert75",
        "status": "mixed_label_provenance",
        "label_provenance": (
            "75 questions replaced by three-AI simulated-expert majority "
            "adjudication; 125 questions retain agent-verified candidate labels; "
            "no human-gold labels"
        ),
        "simulated_expert_question_count": 75,
        "agent_candidate_question_count": 125,
        "simulated_expert_documents": selection["documents"],
        "annotation_protocol": str(HERE / "PROTOCOL.md"),
        "agreement_summary": str(HERE / "agreement_summary.json"),
    }
    (MIXED / "manifest.json").write_text(
        json.dumps(mixed_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    subset_manifest = {
        "name": "nerc_causal_qa_15doc_simulated_expert_subset",
        "status": "simulated_expert_adjudicated_not_human_gold",
        "document_count": 15,
        "question_count": 75,
        "evidence_id_count": sum(
            len(row["evidence_sentence_ids"]) for row in labels.values()
        ),
        "questions_per_document": 5,
        "documents": selection["documents"],
        "label_provenance": (
            "three independent AI simulated-expert annotations with "
            "sentence-level majority adjudication; not human/expert gold"
        ),
        "annotation_protocol": str(HERE / "PROTOCOL.md"),
        "agreement_summary": str(HERE / "agreement_summary.json"),
        "frozen_prediction_rescore": str(HERE / "rescore_results.json"),
    }
    (SUBSET / "manifest.json").write_text(
        json.dumps(subset_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
