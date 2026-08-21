#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build the C2GES sealed packet per C2GES-SEALED-SET-FREEZE-v1.0
(SHA-256 F1929EE62529D96794082A8868B628837ED51EF8A628FCCFAA812EFBD3D14EB0).

Selection: all agent_audit_40doc docs EXCEPT the 15 dev-visible blind_packet docs;
sort by doc_id; take the first 15 with >= 40 sentences and exactly 5 causal_questions.
doc_id falls back to the filename stem when the field is missing; manifest.json is skipped.
The packet contains ONLY doc_id/title/source_url/sentences[{sid,text}]/questions[{qid,role,question}]
-- audit answers and evidence labels are NOT copied (no-leakage discipline).

The freeze artifact (sealed_packet.jsonl + sealed_manifest.json with hashes) must be
written BEFORE any annotator call; the runner verifies the packet hash again at
annotation time.
"""
import glob
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_annotation_pilot import PILOT_DIR, C2GES_PACKET, utc_now  # noqa: E402

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

AUDIT_DIR = (Path("D:/aicoding/powergrid_benchmark/paper_projects/"
                  "2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc"))
OUT_DIR = PILOT_DIR / "runs/c2ges_stage3"
ROLES = ["root_cause", "trigger_event", "propagation_or_response", "impact", "mitigation"]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    dev_ids = set()
    with open(C2GES_PACKET, encoding="utf-8") as f:
        for line in f:
            dev_ids.add(json.loads(line)["doc_id"])
    print(f"[ok] dev-visible docs excluded: {len(dev_ids)}")

    candidates = {}
    for path in sorted(glob.glob(str(AUDIT_DIR / "*.json"))):
        name = Path(path).name
        if name == "manifest.json":
            continue
        raw = Path(path).read_bytes()
        d = json.loads(raw.decode("utf-8"))
        doc_id = d.get("doc_id") or Path(path).stem  # filename fallback per protocol note
        if doc_id in dev_ids:
            continue
        candidates[doc_id] = (d, raw, name)
    print(f"[ok] unused candidate docs: {len(candidates)}")

    selected, skipped = [], []
    for doc_id in sorted(candidates):
        d, raw, name = candidates[doc_id]
        n_sent = len(d.get("sentences", []))
        n_q = len(d.get("causal_questions", []))
        if n_sent >= 40 and n_q == 5:
            selected.append((doc_id, d, raw, name))
        else:
            skipped.append({"doc_id": doc_id, "sentences": n_sent, "questions": n_q})
        if len(selected) == 15:
            break
    # count how many more would have qualified (for the record)
    remaining_qualified = sum(
        1 for doc_id in sorted(candidates)
        if doc_id not in {s[0] for s in selected}
        and len(candidates[doc_id][0].get("sentences", [])) >= 40
        and len(candidates[doc_id][0].get("causal_questions", [])) == 5)
    print(f"[ok] selected {len(selected)} docs; skipped-before-quota: {len(skipped)}; "
          f"qualified-but-not-needed: {remaining_qualified}")
    if len(selected) < 15:
        raise SystemExit("FATAL: fewer than 15 qualifying docs")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    packet_path = OUT_DIR / "sealed_packet.jsonl"
    per_doc = []
    packet_lines = []
    for doc_id, d, raw, name in selected:
        questions = [{"qid": q.get("qid") or f"{doc_id}::{q['role']}",
                      "role": q["role"], "question": q["question"]}
                     for q in d["causal_questions"]]
        roles_present = sorted(q["role"] for q in questions)
        if roles_present != sorted(ROLES):
            raise SystemExit(f"FATAL: {doc_id} roles mismatch: {roles_present}")
        rec = {"doc_id": doc_id, "title": d.get("title", ""),
               "source_url": d.get("source_url", ""),
               "sentences": [{"sid": s["sid"], "text": s["text"]} for s in d["sentences"]],
               "questions": questions}
        line = json.dumps(rec, ensure_ascii=False)
        packet_lines.append(line)
        per_doc.append({"doc_id": doc_id, "source_file": name,
                        "n_sentences": len(rec["sentences"]),
                        "sha256": sha256_bytes((line + "\n").encode("utf-8"))})
    packet_text = "\n".join(packet_lines) + "\n"
    packet_path.write_bytes(packet_text.encode("utf-8"))  # bytes: no CRLF translation
    packet_sha = sha256_bytes(packet_text.encode("utf-8"))

    manifest = {
        "protocol_id": "C2GES-SEALED-SET-FREEZE-v1.0",
        "protocol_sha256": "F1929EE62529D96794082A8868B628837ED51EF8A628FCCFAA812EFBD3D14EB0",
        "frozen_at": utc_now(),
        "custodian": "annotation-pipeline",
        "selection_rule": "unused docs (excl. 15 dev-visible) sorted by doc_id; first 15 with "
                          ">=40 sentences and 5 causal_questions; doc_id falls back to filename "
                          "stem (not needed: all files carried doc_id); manifest.json skipped",
        "dev_docs_excluded": sorted(dev_ids),
        "skipped_before_quota": skipped,
        "qualified_but_not_needed": remaining_qualified,
        "n_docs": len(selected),
        "n_questions": sum(len(s[1]["causal_questions"]) for s in selected),
        "per_doc": per_doc,
        "packet_file": "sealed_packet.jsonl",
        "packet_sha256": packet_sha,
        "no_leakage_declaration": (
            "This packet was assembled from agent_audit_40doc JSONs of public NERC reports. "
            "Only doc_id/title/source_url/sentences/questions(qid,role,question) were copied; "
            "audit answers, evidence_sentence_ids, verification fields and all label-like "
            "content were NOT copied and will NOT be shown to annotators or the adjudicator. "
            "The 15 dev-visible blind_packet docs are excluded. Annotator calls may only start "
            "after this manifest with packet_sha256 is written."),
    }
    with open(OUT_DIR / "sealed_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f"[ok] FROZEN: {packet_path} sha256={packet_sha}")
    print(f"[ok] manifest -> {OUT_DIR / 'sealed_manifest.json'}")
    print("[ok] selected doc_ids:")
    for doc_id, d, raw, name in selected:
        print(f"  {doc_id}  sents={len(d['sentences'])}")


if __name__ == "__main__":
    main()
