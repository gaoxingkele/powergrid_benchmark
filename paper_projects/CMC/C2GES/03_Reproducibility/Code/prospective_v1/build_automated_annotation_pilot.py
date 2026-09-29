#!/usr/bin/env python3
"""Create a deterministic, verbatim-private unit-validation pilot packet."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = next(parent for parent in (HERE, *HERE.parents) if (parent / "C2GES_RELEASE_MARKER.json").is_file())
for import_root in (PROJECT / "03_Reproducibility/Code/core", PROJECT / "03_Reproducibility/Code/core/R2_v0_3"):
    sys.path.insert(0, str(import_root))

from v031_methods import build_graph_v03


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, required=True)
    parser.add_argument("--selected", type=Path, required=True)
    parser.add_argument("--private-packet", type=Path, required=True)
    parser.add_argument("--public-manifest", type=Path, required=True)
    args = parser.parse_args()
    reports = [json.loads(line) for line in args.dataset.read_text(encoding="utf-8").splitlines() if line.strip()]
    chosen = {}
    for line in args.selected.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row["condition"] == "AB-6" and int(row["word_budget"]) == 110:
            chosen[row["doc_id"]] = list(row["selected_sentence_ids"])
    samples = []
    for report in reports:
        graph = build_graph_v03(report["candidate_sentences"], max_distance=12)
        graph_nodes = {node.sid: node for node in graph.nodes}
        lookup = {row["sid"]: row for row in report["candidate_sentences"]}
        ordered = list(report["candidate_sentences"])
        positions = {row["sid"]: index for index, row in enumerate(ordered)}
        ids = chosen[report["doc_id"]][:5]
        for local_index, sid in enumerate(ids, 1):
            position = positions[sid]
            node = graph_nodes[sid]
            samples.append({
                "sample_id": f"{report['doc_id']}_u{local_index:02d}",
                "doc_id": report["doc_id"], "report_series_id": report["report_series_id"],
                "page": int(lookup[sid]["page"]), "unit_type": lookup[sid]["unit_type"],
                "heuristic_role": node.dominant_role or "none_other",
                "previous_text": ordered[position - 1]["text"] if position else "",
                "target_text": lookup[sid]["text"],
                "next_text": ordered[position + 1]["text"] if position + 1 < len(ordered) else "",
            })
    packet = {
        "schema": "c2ges-automated-unit-audit-pilot-v1", "contains_public_real_report_text": True,
        "counts_as_human_validation": False, "task": "independent unit-validity and role labeling",
        "samples": samples,
    }
    args.private_packet.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["sample_id", "doc_id", "report_series_id", "page", "unit_type", "heuristic_role"]
    with args.public_manifest.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields); writer.writeheader()
        writer.writerows([{key: row[key] for key in fields} for row in samples])
    print(json.dumps({"samples": len(samples), "series": len({row['report_series_id'] for row in samples}),
                      "packet_sha256": hashlib.sha256(args.private_packet.read_bytes()).hexdigest().upper()}))


if __name__ == "__main__":
    main()
