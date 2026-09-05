#!/usr/bin/env python3
"""Blinded, stage-locked analysis for the C2GES human-validation study.

This utility never creates scientific labels.  It prepares label-only packets,
freezes pre-adjudication agreement, and analyses adjudicated human labels.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path


FORM_FIELDS = [
    "sample_id", "task", "annotator_id", "unit_validity", "role_label",
    "edge_supported", "edge_direction_correct", "lexical_only_false_relation",
    "context_sufficient", "path_validity", "path_adds_beyond_reservation",
    "source_faithful", "critical_omission", "page_locator_correct",
    "notes_nonverbatim",
]
MANIFEST_REQUIRED = {"sample_id", "task", "report_series_id", "automated_role_label"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        return reader.fieldnames, list(reader)


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def validate_manifest(path: Path, schema):
    fields, rows = load_csv(path)
    missing = MANIFEST_REQUIRED - set(fields)
    if missing:
        raise ValueError(f"sampling manifest missing columns: {sorted(missing)}")
    seen = set()
    for line, row in enumerate(rows, 2):
        key = (row["sample_id"].strip(), row["task"].strip())
        if not all(key) or key in seen:
            raise ValueError(f"invalid or duplicate sample key at line {line}: {key}")
        seen.add(key)
        if key[1] not in schema["tasks"]:
            raise ValueError(f"unknown task at line {line}: {key[1]}")
    if not rows:
        raise ValueError("sampling manifest is empty")
    return rows


def validate_annotation(path: Path, schema, manifest_rows):
    fields, rows = load_csv(path)
    if fields != FORM_FIELDS:
        raise ValueError(f"annotation header differs from locked schema: {path}")
    expected = {(r["sample_id"].strip(), r["task"].strip()) for r in manifest_rows}
    observed = set()
    annotators = set()
    all_label_fields = set(FORM_FIELDS[3:-1])
    by_key = {}
    for line, row in enumerate(rows, 2):
        key = (row["sample_id"].strip(), row["task"].strip())
        if key in observed:
            raise ValueError(f"duplicate annotation key at line {line}: {key}")
        observed.add(key)
        annotator = row["annotator_id"].strip()
        if not annotator:
            raise ValueError(f"missing annotator_id at line {line}")
        annotators.add(annotator)
        task = key[1]
        if task not in schema["tasks"]:
            raise ValueError(f"unknown task at line {line}: {task}")
        required = set(schema["tasks"][task]["fields"])
        for field in required:
            value = row[field].strip()
            if value not in schema["tasks"][task]["labels"][field]:
                raise ValueError(f"invalid or missing {field} at line {line}: {value!r}")
        for field in all_label_fields - required:
            if row[field].strip():
                raise ValueError(f"irrelevant field {field} must be blank at line {line}")
        note = row["notes_nonverbatim"]
        if len(note) > 240 or "\n" in note or "\r" in note:
            raise ValueError(f"notes policy violation at line {line}")
        by_key[key] = row
    if observed != expected:
        missing = sorted(expected - observed)[:10]
        extra = sorted(observed - expected)[:10]
        raise ValueError(f"annotation/sample mismatch; missing={missing}, extra={extra}")
    if len(annotators) != 1:
        raise ValueError(f"each file must contain exactly one annotator_id: {sorted(annotators)}")
    return by_key, next(iter(annotators))


def cohen_kappa(a, b):
    if len(a) != len(b) or not a:
        return None
    labels = set(a) | set(b)
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    expected = sum((ca[x] / n) * (cb[x] / n) for x in labels)
    if math.isclose(expected, 1.0):
        return None
    return (observed - expected) / (1.0 - expected)


def prepare_packets(manifest: Path, schema_path: Path, out_dir: Path, annotator_a: str, annotator_b: str):
    schema = load_json(schema_path)
    rows = validate_manifest(manifest, schema)
    if not annotator_a.strip() or not annotator_b.strip() or annotator_a == annotator_b:
        raise ValueError("two distinct non-empty pseudonymous annotator IDs are required")
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, annotator in (("annotator_a_blinded.csv", annotator_a), ("annotator_b_blinded.csv", annotator_b)):
        packet = []
        for source in rows:
            row = {field: "" for field in FORM_FIELDS}
            row.update(sample_id=source["sample_id"].strip(), task=source["task"].strip(), annotator_id=annotator)
            packet.append(row)
        write_csv(out_dir / filename, FORM_FIELDS, packet)
    receipt = {
        "status": "PACKETS_PREPARED_NOT_LABELED",
        "schema_sha256": sha256(schema_path),
        "sampling_manifest_sha256": sha256(manifest),
        "sample_count": len(rows),
        "blinded_columns": FORM_FIELDS,
        "excluded_manifest_columns": sorted(set(rows[0]) - {"sample_id", "task"}),
    }
    (out_dir / "packet_preparation_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")


def paired_fields(schema, keys, ann_a, ann_b):
    for key in sorted(keys):
        task = key[1]
        for field in schema["tasks"][task]["fields"]:
            yield key, field, ann_a[key][field].strip(), ann_b[key][field].strip()


def freeze_pre(schema_path: Path, manifest: Path, a_path: Path, b_path: Path, output: Path):
    schema = load_json(schema_path)
    manifest_rows = validate_manifest(manifest, schema)
    ann_a, id_a = validate_annotation(a_path, schema, manifest_rows)
    ann_b, id_b = validate_annotation(b_path, schema, manifest_rows)
    if id_a == id_b:
        raise ValueError("annotator A and B IDs must differ")
    grouped = defaultdict(lambda: [[], []])
    disagreements = []
    for key, field, va, vb in paired_fields(schema, ann_a, ann_a, ann_b):
        grouped[(key[1], field)][0].append(va)
        grouped[(key[1], field)][1].append(vb)
        if va != vb:
            disagreements.append({"sample_id": key[0], "task": key[1], "field": field,
                                  "annotator_a_value": va, "annotator_b_value": vb})
    agreement = {}
    for (task, field), (va, vb) in sorted(grouped.items()):
        agreement[f"{task}.{field}"] = {
            "n": len(va),
            "raw_agreement": sum(x == y for x, y in zip(va, vb)) / len(va),
            "cohen_kappa": cohen_kappa(va, vb),
        }
    result = {
        "status": "PRE_ADJUDICATION_FROZEN",
        "schema": schema["schema"],
        "file_sha256": {"schema": sha256(schema_path), "sampling_manifest": sha256(manifest),
                        "annotator_a": sha256(a_path), "annotator_b": sha256(b_path)},
        "annotator_ids": {"a": id_a, "b": id_b},
        "sample_count": len(manifest_rows),
        "agreement": agreement,
        "disagreement_count": len(disagreements),
        "disagreements": disagreements,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")


def validate_adjudication(path: Path, pre, schema):
    fields, rows = load_csv(path)
    expected_header = ["sample_id", "task", "field", "annotator_a_value", "annotator_b_value",
                       "adjudicated_value", "reason_code", "adjudicator_id", "notes_nonverbatim"]
    if fields != expected_header:
        raise ValueError("adjudication header differs from locked template")
    expected = {(d["sample_id"], d["task"], d["field"]): d for d in pre["disagreements"]}
    observed = {}
    for line, row in enumerate(rows, 2):
        key = (row["sample_id"].strip(), row["task"].strip(), row["field"].strip())
        if key in observed or key not in expected:
            raise ValueError(f"unexpected or duplicate adjudication key at line {line}: {key}")
        original = expected[key]
        if row["annotator_a_value"].strip() != original["annotator_a_value"] or row["annotator_b_value"].strip() != original["annotator_b_value"]:
            raise ValueError(f"adjudication does not preserve frozen labels at line {line}")
        allowed = schema["tasks"][key[1]]["labels"][key[2]]
        if row["adjudicated_value"].strip() not in allowed:
            raise ValueError(f"invalid adjudicated value at line {line}")
        if not row["reason_code"].strip() or not row["adjudicator_id"].strip():
            raise ValueError(f"reason_code and adjudicator_id required at line {line}")
        if len(row["notes_nonverbatim"]) > 240 or "\n" in row["notes_nonverbatim"] or "\r" in row["notes_nonverbatim"]:
            raise ValueError(f"notes policy violation at line {line}")
        observed[key] = row["adjudicated_value"].strip()
    if set(observed) != set(expected):
        raise ValueError(f"adjudication must cover exactly all disagreements; missing={len(set(expected)-set(observed))}")
    return observed


def rate_ci(records, positive, seed=20260829, reps=2000):
    judgeable = [(series, value) for series, value in records if value != "cannot_judge"]
    if not judgeable:
        return None, None, None, 0
    by_series = defaultdict(list)
    for series, value in judgeable:
        by_series[series].append(1.0 if value in positive else 0.0)
    series_means = {s: sum(v) / len(v) for s, v in by_series.items()}
    estimate = sum(series_means.values()) / len(series_means)
    rng = random.Random(seed)
    keys = sorted(series_means)
    draws = []
    for _ in range(reps):
        sample = [series_means[rng.choice(keys)] for _ in keys]
        draws.append(sum(sample) / len(sample))
    draws.sort()
    return estimate, draws[int(0.025 * reps)], draws[min(reps - 1, int(0.975 * reps))], len(judgeable)


def role_metrics(manifest_rows, final_values):
    classes = ["root_cause", "trigger_event", "propagation_response", "impact", "mitigation", "none_other"]
    human, predicted = [], []
    excluded = Counter()
    for row in manifest_rows:
        if row["task"] != "role":
            continue
        truth = final_values[(row["sample_id"], "role", "role_label")]
        pred = row["automated_role_label"].strip()
        if truth in {"cannot_judge", "ambiguous_multiple"}:
            excluded[truth] += 1
            continue
        if pred not in classes:
            raise ValueError(f"invalid automated_role_label for {row['sample_id']}: {pred!r}")
        human.append(truth); predicted.append(pred)
    matrix = []
    precisions, recalls, f1s = [], [], []
    for actual in classes:
        for pred in classes:
            matrix.append({"human_role": actual, "automated_role": pred,
                           "count": sum(h == actual and p == pred for h, p in zip(human, predicted))})
    for label in classes:
        tp = sum(h == label and p == label for h, p in zip(human, predicted))
        fp = sum(h != label and p == label for h, p in zip(human, predicted))
        fn = sum(h == label and p != label for h, p in zip(human, predicted))
        precision = tp / (tp + fp) if tp + fp else 0.0
        recall = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        precisions.append(precision); recalls.append(recall); f1s.append(f1)
    metrics = {"role_evaluable_n": len(human), "role_excluded": dict(excluded),
               "role_macro_precision": sum(precisions) / len(classes),
               "role_macro_recall": sum(recalls) / len(classes),
               "role_macro_f1": sum(f1s) / len(classes)}
    return metrics, matrix


def final_analysis(schema_path: Path, manifest: Path, a_path: Path, b_path: Path, pre_path: Path,
                   adjudication: Path, output_dir: Path):
    schema = load_json(schema_path)
    pre = load_json(pre_path)
    current = {"schema": sha256(schema_path), "sampling_manifest": sha256(manifest),
               "annotator_a": sha256(a_path), "annotator_b": sha256(b_path)}
    if pre.get("status") != "PRE_ADJUDICATION_FROZEN" or pre.get("file_sha256") != current:
        raise ValueError("pre-adjudication lock missing or input hashes changed")
    manifest_rows = validate_manifest(manifest, schema)
    ann_a, _ = validate_annotation(a_path, schema, manifest_rows)
    ann_b, _ = validate_annotation(b_path, schema, manifest_rows)
    resolutions = validate_adjudication(adjudication, pre, schema)
    final_values = {}
    for key, field, va, vb in paired_fields(schema, ann_a, ann_a, ann_b):
        final_values[(key[0], key[1], field)] = va if va == vb else resolutions[(key[0], key[1], field)]

    role, matrix = role_metrics(manifest_rows, final_values)
    records = defaultdict(list)
    manifest_by_key = {(r["sample_id"], r["task"]): r for r in manifest_rows}
    for (sample, task, field), value in final_values.items():
        records[(task, field)].append((manifest_by_key[(sample, task)]["report_series_id"], value))
    specs = {
        "unit_validity_rate": (("unit", "unit_validity"), {"standalone"}),
        "supported_edge_precision": (("edge", "edge_supported"), {"yes"}),
        "edge_direction_accuracy": (("edge", "edge_direction_correct"), {"yes"}),
        "path_coherent_or_partial_rate": (("path", "path_validity"), {"coherent", "partially_coherent"}),
        "path_adds_beyond_reservation_rate": (("path", "path_adds_beyond_reservation"), {"yes"}),
        "source_faithfulness_rate": (("summary", "source_faithful"), {"yes"}),
        "critical_omission_rate": (("summary", "critical_omission"), {"yes"}),
        "page_locator_accuracy": (("summary", "page_locator_correct"), {"yes"}),
    }
    metric_rows = []
    computed = dict(role)
    for name, (key, positive) in specs.items():
        estimate, low, high, n = rate_ci(records[key], positive)
        computed[name] = estimate
        metric_rows.append({"metric": name, "estimate": estimate, "cluster_ci_low": low,
                            "cluster_ci_high": high, "judgeable_n": n})
    for name in ("role_macro_precision", "role_macro_recall", "role_macro_f1"):
        metric_rows.append({"metric": name, "estimate": role[name], "cluster_ci_low": "",
                            "cluster_ci_high": "", "judgeable_n": role["role_evaluable_n"]})

    agreement_lookup = pre["agreement"]
    gates = {
        "role_macro_f1": computed["role_macro_f1"] >= schema["thresholds"]["role_macro_f1"],
        "role_kappa": agreement_lookup["role.role_label"]["cohen_kappa"] is not None and agreement_lookup["role.role_label"]["cohen_kappa"] >= schema["thresholds"]["role_kappa"],
        "edge_support_kappa": agreement_lookup["edge.edge_supported"]["cohen_kappa"] is not None and agreement_lookup["edge.edge_supported"]["cohen_kappa"] >= schema["thresholds"]["edge_support_kappa"],
        "edge_direction_kappa": agreement_lookup["edge.edge_direction_correct"]["cohen_kappa"] is not None and agreement_lookup["edge.edge_direction_correct"]["cohen_kappa"] >= schema["thresholds"]["edge_direction_kappa"],
        "supported_edge_precision": computed["supported_edge_precision"] is not None and computed["supported_edge_precision"] >= schema["thresholds"]["supported_edge_precision"],
        "coherent_or_partial_path_rate": computed["path_coherent_or_partial_rate"] is not None and computed["path_coherent_or_partial_rate"] >= schema["thresholds"]["coherent_or_partial_path_rate"],
        "page_locator_accuracy": computed["page_locator_accuracy"] is not None and computed["page_locator_accuracy"] >= schema["thresholds"]["page_locator_accuracy"],
        "source_faithfulness_rate": computed["source_faithfulness_rate"] is not None and computed["source_faithfulness_rate"] >= schema["thresholds"]["source_faithfulness_rate"],
    }
    decisions = {
        "status": "ANALYSIS_COMPLETE_RESULTS_REQUIRE_AUTHOR_INTERPRETATION",
        "gates": gates,
        "all_structure_claim_gates_pass": all(gates.values()),
        "required_action_if_false": "Downgrade the associated construct to a heuristic proxy; do not claim validation.",
        "role_exclusion_rule": "cannot_judge and ambiguous_multiple are excluded from single-label macro metrics and reported separately",
        "file_sha256": {**current, "pre_adjudication": sha256(pre_path), "adjudication": sha256(adjudication)},
    }
    taxonomy = []
    for (task, field), values in sorted(records.items()):
        counts = Counter(value for _, value in values)
        for label, count in sorted(counts.items()):
            taxonomy.append({"task": task, "field": field, "label": label, "count": count})
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "human_structure_results.csv",
              ["metric", "estimate", "cluster_ci_low", "cluster_ci_high", "judgeable_n"], metric_rows)
    write_csv(output_dir / "confusion_matrix_roles.csv", ["human_role", "automated_role", "count"], matrix)
    write_csv(output_dir / "edge_path_error_taxonomy.csv", ["task", "field", "label", "count"], taxonomy)
    (output_dir / "claim_gate_decisions.json").write_text(json.dumps(decisions, indent=2), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    prep = sub.add_parser("prepare")
    prep.add_argument("--schema", type=Path, required=True); prep.add_argument("--manifest", type=Path, required=True)
    prep.add_argument("--output-dir", type=Path, required=True); prep.add_argument("--annotator-a", required=True); prep.add_argument("--annotator-b", required=True)
    pre = sub.add_parser("pre")
    for name in ("schema", "manifest", "annotator-a", "annotator-b", "output"):
        pre.add_argument(f"--{name}", type=Path, required=True)
    final = sub.add_parser("final")
    for name in ("schema", "manifest", "annotator-a", "annotator-b", "pre", "adjudication", "output-dir"):
        final.add_argument(f"--{name}", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        prepare_packets(args.manifest, args.schema, args.output_dir, args.annotator_a, args.annotator_b)
    elif args.command == "pre":
        freeze_pre(args.schema, args.manifest, args.annotator_a, args.annotator_b, args.output)
    else:
        final_analysis(args.schema, args.manifest, args.annotator_a, args.annotator_b, args.pre, args.adjudication, args.output_dir)


if __name__ == "__main__":
    main()
