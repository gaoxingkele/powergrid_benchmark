#!/usr/bin/env python3
"""Build a small QMSum-style causal-QA pilot from existing NERC assets.

The output is an agent-audited candidate dataset, not human gold.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


DOC_IDS = [
    "nerc_001_november_13_wyoming_disturbance_report",
    "nerc_005_nerc_2023_southwest_ut_disturbance_report",
    "nerc_006_june_2022_odessa_disturbance_report",
    "nerc_007_panhandle_wind_disturbance_report",
    "nerc_009_odessa_disturbance_report",
]

ROLE_TO_QUERY = {
    "root_cause": (
        "What root cause or contributing factor does the report identify for the incident?",
        ["cause_or_contributing_factor"],
    ),
    "trigger_event": (
        "What initiating grid event or disturbance is described?",
        ["grid_event"],
    ),
    "propagation_or_response": (
        "How did the disturbance propagate or how did the system respond?",
        ["impact_or_system_response", "grid_event"],
    ),
    "impact": (
        "What operational impact or consequence did the incident have?",
        ["impact_or_system_response"],
    ),
    "mitigation": (
        "What mitigation, recommendation, or corrective action is described?",
        ["mitigation_or_recommendation"],
    ),
}


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sentence_map(processed: dict) -> dict[str, str]:
    out: dict[str, str] = {}
    for idx, sent in enumerate(processed.get("sentences", []), start=1):
        if isinstance(sent, dict):
            sid = sent.get("sid") or sent.get("sentence_id") or f"s{idx:03d}"
            text = sent.get("text") or sent.get("sentence") or sent.get("content") or ""
        else:
            sid = f"s{idx:03d}"
            text = str(sent)
        text = clean_text(text)
        if text:
            out[sid] = text
    return out


def select_evidence(annotation: dict, wanted_types: list[str], sent_by_id: dict[str, str]) -> list[str]:
    scores: dict[str, int] = {}
    for event in annotation.get("events", []):
        sid = event.get("sid")
        if sid in sent_by_id and event.get("type") in wanted_types:
            scores[sid] = scores.get(sid, 0) + 3
    for link in annotation.get("links", []):
        sid = link.get("evidence_sid")
        if sid in sent_by_id:
            scores[sid] = scores.get(sid, 0) + 1
    ranked = sorted(scores, key=lambda sid: (-scores[sid], sid))
    if ranked:
        return ranked[:3]
    # Conservative fallback: choose early non-short sentences so every query is runnable.
    return [sid for sid, text in sent_by_id.items() if len(text) >= 60][:2]


def answer_from_evidence(evidence_ids: list[str], sent_by_id: dict[str, str]) -> str:
    return " ".join(sent_by_id[sid] for sid in evidence_ids if sid in sent_by_id)


def build_doc(asset_root: Path, doc_id: str) -> dict:
    processed = load_json(asset_root / "processed" / f"{doc_id}.json")
    annotation = load_json(asset_root / "annotations" / f"{doc_id}.json")
    sent_by_id = sentence_map(processed)
    questions = []
    for role, (question, wanted_types) in ROLE_TO_QUERY.items():
        evidence_ids = select_evidence(annotation, wanted_types, sent_by_id)
        questions.append(
            {
                "qid": f"{doc_id}::{role}",
                "role": role,
                "question": question,
                "answer": answer_from_evidence(evidence_ids, sent_by_id),
                "evidence_sentence_ids": evidence_ids,
                "verification_status": "agent_audited_candidate_not_human_gold",
                "source_annotation": annotation.get("annotation_method", "unknown"),
                "notes": "Evidence IDs are derived from prior weak annotations and require human verification before gold-label claims.",
            }
        )
    return {
        "doc_id": doc_id,
        "title": processed.get("title", ""),
        "source_url": processed.get("source_url", ""),
        "source_page": processed.get("source_page", ""),
        "sentences": [{"sid": sid, "text": text} for sid, text in sent_by_id.items()],
        "causal_questions": questions,
        "dataset_status": "agent_audited_candidate_not_human_gold",
    }


def main() -> None:
    workspace = Path(__file__).resolve().parents[1]
    repo = workspace.parents[3]
    asset_root = repo / "paper_workspace/workspaces/c2ges-evidence-audit-krill/datasets/gridmaint_causalsum_pilot"
    out_dir = workspace / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    docs = [build_doc(asset_root, doc_id) for doc_id in DOC_IDS]
    for doc in docs:
        (out_dir / f"{doc['doc_id']}.json").write_text(json.dumps(doc, indent=2), encoding="utf-8")
    manifest = {
        "name": "nerc_causal_qa_5doc_pilot",
        "schema_anchor": "QMSum-style query/answer/evidence spans",
        "status": "agent_audited_candidate_not_human_gold",
        "documents": [doc["doc_id"] for doc in docs],
        "question_count": sum(len(doc["causal_questions"]) for doc in docs),
        "questions_per_document": 5,
        "source_asset_root": str(asset_root),
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
