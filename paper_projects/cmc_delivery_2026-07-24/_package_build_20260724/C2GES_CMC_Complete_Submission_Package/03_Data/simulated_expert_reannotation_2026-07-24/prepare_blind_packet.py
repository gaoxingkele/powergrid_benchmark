#!/usr/bin/env python3
"""Create a frozen, label-blind packet for the 15-document/75-question subset."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parent
DATASET = WORKSPACE / "verification_pilot" / "agent_audit_40doc"
MANIFEST = DATASET / "manifest.json"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = list(manifest["new_documents"])
    packet = []
    selection_rows = []

    for doc_id in selected:
        doc = json.loads((DATASET / f"{doc_id}.json").read_text(encoding="utf-8"))
        questions = [
            {
                "qid": q["qid"],
                "role": q["role"],
                "question": q["question"],
            }
            for q in doc["causal_questions"]
        ]
        packet.append(
            {
                "doc_id": doc["doc_id"],
                "title": doc.get("title", ""),
                "source_url": doc.get("source_url", ""),
                "sentences": doc["sentences"],
                "questions": questions,
            }
        )
        selection_rows.extend(
            {"doc_id": doc_id, "qid": q["qid"], "role": q["role"]}
            for q in questions
        )

    if len(packet) != 15 or len(selection_rows) != 75:
        raise RuntimeError(
            f"Expected 15 documents and 75 questions, got "
            f"{len(packet)} and {len(selection_rows)}"
        )

    (HERE / "blind_packet.jsonl").write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in packet) + "\n",
        encoding="utf-8",
    )
    (HERE / "selection_manifest.json").write_text(
        json.dumps(
            {
                "source_manifest": str(MANIFEST),
                "selection_rule": "all manifest.new_documents",
                "document_count": len(packet),
                "question_count": len(selection_rows),
                "documents": selected,
                "questions": selection_rows,
                "label_status": "simulated_expert_reannotation_planned",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
