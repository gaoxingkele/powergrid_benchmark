#!/usr/bin/env python3
"""Generate non-confirmatory C2GES synthetic stress data.

DeepSeek supplies a compact fictional semantic core. All layout expansion,
reference construction, validation, distribution assignment, and acceptance
bookkeeping are deterministic local operations. No real report text is sent.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import urllib.error
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

MODEL_DEFAULT = "deepseek-v4-flash"
CORE_ROLES = ("trigger_event", "root_cause", "propagation_or_response", "impact", "mitigation")
ROLES = set(CORE_ROLES) | {"distractor"}
UNIT_TYPES = ("body", "heading", "list_item", "table_unit", "caption", "footnote")
REAL_MARKERS = ("NERC", "FERC", "WECC", "ERCOT", "PJM", "CAISO", "MISO", "ENTSO-E", "State Grid")
THEMES = (
    "protection-setting mismatch during feeder restoration",
    "transformer cooling-control failure during a heat wave",
    "inverter ride-through response to a fictional voltage depression",
    "telemetry delay during reserve activation",
    "substation auxiliary-power loss after a fictional cable fault",
    "frequency response following fictional generator separation",
    "distribution automation loop during storm restoration",
    "reactive-power controller saturation in a weak corridor",
    "battery dispatch conflict during peak shaving",
    "islanding detection delay at a fictional microgrid",
    "load-shedding threshold coordination failure",
    "maintenance-tag mismatch during bus transfer",
)
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest().upper()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def contains_real_marker(text: str) -> bool:
    """Match organization tokens, not substrings such as ``misoperation``."""
    return any(re.search(rf"(?<![A-Za-z0-9]){re.escape(marker)}(?![A-Za-z0-9])", text, re.I)
               for marker in REAL_MARKERS)


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*$", line)
        if match and not line.lstrip().startswith("#"):
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return values


def api_url(base: str) -> str:
    clean = base.rstrip("/")
    return f"{clean}/chat/completions" if clean.endswith("/v1") else f"{clean}/v1/chat/completions"


def read_numeric_rows(metadata_csv: Path, layout_csv: Path) -> list[dict[str, int]]:
    """Create rights-safe empirical profiles without reading report text."""
    metadata: dict[str, dict[str, str]] = {}
    with metadata_csv.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.DictReader(stream):
            if row.get("inclusion_status") == "included":
                metadata[row["doc_id"]] = row
    profiles: list[dict[str, int]] = []
    with layout_csv.open(encoding="utf-8-sig", newline="") as stream:
        for layout in csv.DictReader(stream):
            meta = metadata.get(layout["doc_id"], {})
            counts = {kind: int(layout.get(f"units_{kind}") or 0) for kind in UNIT_TYPES}
            profiles.append({
                "page_count": int(meta.get("page_count") or layout.get("source_pages") or 1),
                "candidate_count": int(layout["candidate_count"]),
                "reference_words": int(meta.get("reference_words") or 145),
                "units_over_256_tokens": int(layout.get("units_over_256_tokens") or 0),
                **counts,
            })
    if not profiles:
        raise ValueError("no rights-safe development profiles found")
    return profiles


def prompt(series_number: int, theme: str, regime: str, seed: int, critic_amendment: str = "") -> str:
    amendment = critic_amendment.strip()
    return f"""Create exactly two entirely fictional technical incident semantic cores for a synthetic extraction benchmark.
Series ID synthetic_series_{series_number:02d}; fictional theme: {theme}; lexical regime: {regime}; seed label: {seed}.
Never name or imitate a real organization, utility, jurisdiction, person, report, or real event. Facilities must begin with Synthetic.
Return one JSON object only with key reports (array length 2). Each report has title, core_units, and distractor_seeds.
Each core_units array has 18--26 objects. Each role trigger_event, root_cause, propagation_or_response, impact, and mitigation must occur 2--6 times, and role counts must vary rather than using an equal template.
Each object has text, role, causal_predecessors, and summary_priority (integer 0, 1, or 2). Text must be a standalone 12--24 English-word technical statement with concrete but fictional quantities where useful. causal_predecessors may reference any other zero-based unit indices, regardless of document order, but the complete directed graph must be acyclic. Assign priority 2 to exactly one indispensable statement per role, priority 1 to useful context, and priority 0 to optional complications.
Each distractor_seeds array has 24--36 distinct, topic-specific 10--24-word technical background statements unrelated to the incident outcome. Vary syntax and subject matter; avoid numbered boilerplate and recurring sentence frames.
Before returning JSON, count the English words in every distractor seed and rewrite any seed outside 10--24 words; do not merely assume compliance.
Build each incident from explicit timestamps and state transitions. Use exactly one primary cause and no more than two contributing conditions. Recompute thresholds, currents, power, energy, durations, and device actions so all quantities and protection behavior are internally consistent. Do not assert exact damage, life reduction, or availability effects without a stated calculation basis.
Across each report include a coherent causal chain, at least one condition, one negated non-cause, one corrective action, nonchronological exposition, and internally consistent quantities. Device names and functions must follow ordinary power-system usage.
Use component-specific physics and ordinary power-system terminology. Do not introduce ANSI device numbers, triacs, lockout relays, or dissolved-gas diagnostics unless naturally required by the assigned theme. When such concepts are used, verify their standard function and terminology. Distinguish measured physical values from controller-indicated values and name the independent channel when they differ.
For explicit regime use ordinary causal terms. For paraphrased regime express functions with fewer conventional cue words. For ambiguous regime allow several plausible secondary functions while retaining one best role.
Do not create layout units, summaries, citations, URLs, markdown, or commentary; local deterministic code expands the semantic and distractor seeds.
Critic-guided amendment for this candidate version: {amendment or 'none; parent baseline'}"""


def call_api(url: str, key: str, model: str, content: str) -> tuple[dict[str, Any], dict[str, Any], bytes]:
    payload = {"model": model, "messages": [
        {"role": "system", "content": "Generate fictional research fixtures as strict JSON. Never claim they are real observations."},
        {"role": "user", "content": content}], "temperature": 0.65,
        "response_format": {"type": "json_object"}}
    request = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            raw = response.read()
            request_id = response.headers.get("x-request-id", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read(1000).decode("utf-8", errors="replace")
        raise RuntimeError(f"DeepSeek HTTP {exc.code}: {detail}") from exc
    envelope = json.loads(raw)
    text = envelope["choices"][0]["message"]["content"].strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.I | re.S)
    return json.loads(text), {"request_id": request_id, "response_sha256": hash_bytes(raw),
                              "usage": envelope.get("usage", {})}, raw


def causal_graph_is_acyclic(units: list[dict[str, Any]]) -> bool:
    """Validate semantic direction independently of nonchronological prose order."""
    state = [0] * len(units)

    def visit(node: int) -> bool:
        if state[node] == 1:
            return False
        if state[node] == 2:
            return True
        state[node] = 1
        for predecessor in units[node]["causal_predecessors"]:
            if not visit(predecessor):
                return False
        state[node] = 2
        return True

    return all(visit(node) for node in range(len(units)))


def validate_core(value: dict[str, Any], require_distractor_seeds: bool = False) -> list[dict[str, Any]]:
    reports = value.get("reports")
    if not isinstance(reports, list) or len(reports) != 2:
        raise ValueError("API output must contain exactly two reports")
    clean: list[dict[str, Any]] = []
    for report in reports:
        units = report.get("core_units")
        distractor_seeds = report.get("distractor_seeds", [])
        if not isinstance(units, list) or not 18 <= len(units) <= 26:
            raise ValueError("each semantic core requires 18--26 units")
        normalized = []
        for index, unit in enumerate(units):
            text, role = str(unit.get("text", "")).strip(), unit.get("role")
            predecessors = unit.get("causal_predecessors", [])
            if role not in CORE_ROLES or not 10 <= words(text) <= 28:
                raise ValueError(f"invalid core unit at index {index}")
            if contains_real_marker(text):
                raise ValueError("real-entity marker in synthetic core")
            if not isinstance(predecessors, list) or any(not isinstance(p, int) or p < 0 or p >= len(units) or p == index for p in predecessors):
                raise ValueError(f"invalid causal_predecessors at index {index}")
            priority = unit.get("summary_priority", 1)
            if not isinstance(priority, int) or priority not in {0, 1, 2}:
                raise ValueError(f"invalid summary_priority at index {index}")
            normalized.append({"text": text, "role": role, "causal_predecessors": predecessors,
                               "summary_priority": priority})
        counts = Counter(row["role"] for row in normalized)
        if any(not 2 <= counts[role] <= 6 for role in CORE_ROLES):
            raise ValueError(f"core role balance failed: {dict(counts)}")
        if require_distractor_seeds and any(sum(row["role"] == role and row["summary_priority"] == 2 for row in normalized) != 1
                                            for role in CORE_ROLES):
            raise ValueError("each role requires exactly one priority-2 unit")
        if not causal_graph_is_acyclic(normalized):
            raise ValueError("causal predecessor graph contains a cycle")
        if require_distractor_seeds and (not isinstance(distractor_seeds, list) or not 24 <= len(distractor_seeds) <= 36):
            raise ValueError("each child report requires 24--36 distractor seeds")
        clean_distractors = []
        for distractor_index, text in enumerate(distractor_seeds):
            text = str(text).strip()
            length = words(text)
            if not 8 <= length <= 28 or contains_real_marker(text):
                raise ValueError(f"invalid distractor seed at index {distractor_index}: words={length}, real_marker={contains_real_marker(text)}")
            clean_distractors.append(text)
        if len(clean_distractors) != len(set(text.casefold() for text in clean_distractors)):
            raise ValueError("distractor seeds must be distinct")
        clean.append({"title": str(report.get("title") or "Synthetic Incident"), "core_units": normalized,
                      "distractor_seeds": clean_distractors})
    return clean


def allocate_types(profile: dict[str, int], total: int) -> list[str]:
    observed = [profile[kind] for kind in UNIT_TYPES]
    denominator = sum(observed) or 1
    raw = [total * count / denominator for count in observed]
    counts = [math.floor(value) for value in raw]
    for index in sorted(range(len(raw)), key=lambda i: raw[i] - counts[i], reverse=True)[: total - sum(counts)]:
        counts[index] += 1
    return [kind for kind, count in zip(UNIT_TYPES, counts) for _ in range(count)]


def filler_text(index: int, theme: str, kind: str, doc_id: str, distractor_seeds: list[str]) -> str:
    facility = f"Synthetic Node {index % 17 + 1}"
    salt = int(hash_bytes(doc_id.encode("utf-8"))[:8], 16)
    hour, minute = (salt + index * 7) % 24, (salt // 24 + index * 11) % 60
    if distractor_seeds:
        base = distractor_seeds[index % len(distractor_seeds)]
        if kind == "heading":
            return " ".join(base.rstrip(".").split()[:9]).title() + f" - Background Interval {index + 1}"
        if kind == "caption":
            return f"Auxiliary trend at {facility} for archive interval {index + 1}, sampled at {hour:02d}:{minute:02d}."
        if kind == "footnote":
            return f"Values for {facility} in sample {index + 1} were rounded to the displayed precision."
        if kind == "table_unit":
            return f"Sample {index + 1}; {facility}; auxiliary channel {(salt + index) % 41 + 1}; nominal status; {5 + index % 12}-second interval."
        suffixes = (
            f"Archive sequence {index + 1} recorded the scan at {hour:02d}:{minute:02d}.",
            f"Auxiliary channel {(salt + index) % 41 + 1} retained entry {index + 1} at {hour:02d}:{minute:02d}.",
            f"The shift log filed the observation under routine interval {index + 1}.",
            f"The observation was timestamped {hour:02d}:{minute:02d} under archive key {index + 1}.",
            f"Maintenance index {index + 1} linked the reading to its scheduled inspection window.",
            f"Channel {(salt + index) % 41 + 1} stored the reading as sequence {index + 1} for trend review.",
        )
        prefix = "Checklist context: " if kind == "list_item" else ""
        return f"{prefix}{base} {suffixes[index % len(suffixes)]}"
    observation = f"observation {index + 1:04d}"
    variants = (
        f"{facility} logged {observation} during the fictional {theme} study window, with no causal attribution assigned.",
        f"A scheduled inspection at {facility} recorded {observation} with stable auxiliary readings and was retained only as a layout distractor.",
        f"The fictional monitoring table labels {observation}, channel {index % 31 + 1}, interval {5 + index % 12} seconds, and a nominal status flag.",
        f"Background documentation for {facility} describes {observation}, an unrelated seasonal test outside the synthetic incident window.",
    )
    text = variants[index % len(variants)]
    prefixes = {"heading": f"Synthetic Section {index % 9 + 1}: ", "caption": "Synthetic figure caption: ",
                "footnote": "Synthetic note: "}
    return prefixes.get(kind, "") + text


def select_reference(core: list[dict[str, Any]], low: int = 110, high: int = 180) -> list[int]:
    selected = sorted({max((i for i, row in enumerate(core) if row["role"] == role),
                           key=lambda i: (core[i].get("summary_priority", 1), -i)) for role in CORE_ROLES}
                      | {i for i, row in enumerate(core) if row.get("summary_priority", 1) == 2})
    while words(" ".join(core[i]["text"] for i in selected)) > high:
        removable = [i for i in selected if core[i].get("summary_priority", 1) < 2 and
                     sum(core[j]["role"] == core[i]["role"] for j in selected) > 1]
        if not removable:
            break
        selected.remove(max(removable, key=lambda i: (words(core[i]["text"]), -core[i].get("summary_priority", 1))))
    order = sorted(range(len(core)), key=lambda i: (-core[i].get("summary_priority", 1), i))
    for i in order:
        if words(" ".join(core[j]["text"] for j in selected)) >= low:
            break
        if i not in selected:
            selected.append(i)
            selected.sort()
    length = words(" ".join(core[i]["text"] for i in selected))
    if not low <= length <= high:
        raise ValueError(f"deterministic reference construction failed: {length} words")
    return selected


def expand_report(core_report: dict[str, Any], profile: dict[str, int], doc_id: str, series_id: str,
                  regime: str, theme: str, rng: random.Random) -> dict[str, Any]:
    target_count = max(40, profile["candidate_count"])
    types = allocate_types(profile, target_count)
    rng.shuffle(types)
    core = core_report["core_units"]
    reference_indices = select_reference(core)
    semantic_slots = [i for i, kind in enumerate(types) if kind in {"body", "list_item"}]
    if len(semantic_slots) < len(core):
        raise ValueError("empirical profile has too few body/list slots for semantic core")
    core_slots = sorted(rng.sample(semantic_slots, len(core)))
    core_by_slot = dict(zip(core_slots, range(len(core))))
    units, core_sid = [], {}
    for slot in range(target_count):
        sid, unit_type = f"u{slot + 1:05d}", types[slot]
        page = 1 + (slot * max(1, profile["page_count"]) // target_count)
        if slot in core_by_slot:
            core_index = core_by_slot[slot]
            item = core[core_index]
            text, role, tags = item["text"], item["role"], ["deepseek_semantic_core"]
            core_sid[core_index] = sid
        else:
            text, role, tags = filler_text(slot, theme, unit_type, doc_id, core_report.get("distractor_seeds", [])), "distractor", ["deterministic_layout_distractor"]
        units.append({"sid": sid, "text": text, "page": page, "unit_type": unit_type,
                      "synthetic_ground_truth_role": role, "synthetic_stress_tags": tags})
    reference_ids = [core_sid[index] for index in reference_indices]
    lookup = {unit["sid"]: unit["text"] for unit in units}
    return {"doc_id": doc_id, "report_series_id": series_id, "split": "synthetic_stress",
            "synthetic": True, "confirmatory_claims_allowed": False, "lexical_regime": regime,
            "title": core_report["title"], "candidate_sentences": units,
            "reference_summary": " ".join(lookup[sid] for sid in reference_ids),
            "reference_unit_ids": reference_ids, "target_profile": profile}


def validate_dataset(reports: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(reports)
    ids = [row["doc_id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate document identifiers")
    series = Counter(row["report_series_id"] for row in rows)
    for row in rows:
        if not row.get("synthetic") or row.get("confirmatory_claims_allowed") is not False:
            raise ValueError("synthetic claim boundary missing")
        units = row["candidate_sentences"]
        lookup = {unit["sid"]: unit for unit in units}
        if len(lookup) != len(units):
            raise ValueError("duplicate unit identifiers")
        if any(sid not in lookup for sid in row["reference_unit_ids"]):
            raise ValueError("reference points outside candidates")
        exact = " ".join(lookup[sid]["text"] for sid in row["reference_unit_ids"])
        if exact != row["reference_summary"] or not 110 <= words(exact) <= 180:
            raise ValueError("reference is not valid extractive text")
        role_counts = Counter(unit["synthetic_ground_truth_role"] for unit in units)
        if any(role_counts[role] < 1 for role in CORE_ROLES):
            raise ValueError("role coverage failed")
        if any(contains_real_marker(unit["text"]) for unit in units):
            raise ValueError("real organization marker found")
    return {"reports": len(rows), "series": len(series), "two_reports_per_series": all(v == 2 for v in series.values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", type=Path, required=True)
    parser.add_argument("--metadata-csv", type=Path, required=True)
    parser.add_argument("--layout-csv", type=Path, required=True)
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--series", type=int, default=4, choices=range(1, 13))
    parser.add_argument("--version-id", default="parent-v2")
    parser.add_argument("--critic-amendment", default="")
    parser.add_argument("--critic-amendment-file", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(f"refusing existing output directory: {args.output}")
    env = load_env(args.env)
    key, base = env.get("DEEPSEEK_API_KEY", ""), env.get("DEEPSEEK_BASE_URL", "")
    if not key or not base:
        raise RuntimeError("DEEPSEEK_API_KEY and DEEPSEEK_BASE_URL are required")
    profiles = read_numeric_rows(args.metadata_csv, args.layout_csv)
    args.output.mkdir(parents=True)
    log_path, raw_dir = args.output / "generation_log.jsonl", args.output / "raw_synthetic_responses"
    raw_dir.mkdir()
    rng = random.Random(args.seed)
    scheduled = list(enumerate(THEMES, 1))
    rng.shuffle(scheduled)
    scheduled = scheduled[: args.series]
    all_reports, started = [], utc_now()
    report_total = 2 * args.series
    selected_profiles = [profiles[min(len(profiles) - 1, math.floor((i + 0.5) * len(profiles) / report_total))]
                         for i in range(report_total)]
    critic_amendment = args.critic_amendment
    if args.critic_amendment_file:
        critic_value = json.loads(args.critic_amendment_file.read_text(encoding="utf-8"))
        critic_amendment = str(critic_value.get("mutation_amendment", ""))
        if not critic_amendment:
            raise ValueError("critic result contains no mutation_amendment")
    for call_number, (series_number, theme) in enumerate(scheduled, 1):
        regime = ("explicit", "paraphrased", "ambiguous")[(series_number - 1) % 3]
        content = prompt(series_number, theme, regime, args.seed, critic_amendment)
        print(f"[{call_number}/{args.series}] generating synthetic_series_{series_number:02d} regime={regime}", flush=True)
        value, metadata, raw = call_api(api_url(base), key, args.model, content)
        raw_path = raw_dir / f"call_{call_number:02d}.json"
        raw_path.write_bytes(raw)
        try:
            cores = validate_core(value, require_distractor_seeds=True)
            for report_number, core_report in enumerate(cores, 1):
                profile = selected_profiles[2 * (call_number - 1) + report_number - 1]
                all_reports.append(expand_report(core_report, profile,
                    f"synthetic_s{series_number:02d}_r{report_number:02d}", f"synthetic_series_{series_number:02d}",
                    regime, theme, rng))
            status, error = "accepted", None
        except Exception as exc:
            status, error = "rejected_stop_no_retry", f"{type(exc).__name__}: {exc}"
        record = {"call_number": call_number, "series_id": f"synthetic_series_{series_number:02d}",
                  "model": args.model, "version_id": args.version_id, "prompt_sha256": hash_bytes(content.encode()),
                  "raw_file": raw_path.name, "raw_file_sha256": sha256(raw_path), "status": status, "error": error, **metadata}
        with log_path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        if error:
            failure = {"schema": "c2ges-synthetic-failure-v2", "status": status, "record": record,
                       "partial_reports": len(all_reports), "confirmatory_claims_allowed": False}
            (args.output / "FAILURE_RECORD.json").write_text(json.dumps(failure, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            raise RuntimeError(error)
    validation = validate_dataset(all_reports)
    if not validation["two_reports_per_series"]:
        raise ValueError("series cardinality gate failed")
    dataset_path = args.output / "synthetic_reports.jsonl"
    with dataset_path.open("x", encoding="utf-8", newline="\n") as stream:
        for report in sorted(all_reports, key=lambda row: row["doc_id"]):
            stream.write(json.dumps(report, ensure_ascii=False, sort_keys=True) + "\n")
    manifest = {"schema": "c2ges-deepseek-synthetic-stress-v2", "synthetic": True,
        "external_test_accessed": False, "confirmatory_claims_allowed": False, "provider": "DeepSeek",
        "model": args.model, "version_id": args.version_id, "seed": args.seed, "started_at": started,
        "completed_at": utc_now(), **validation, "api_calls": args.series, "dataset_sha256": sha256(dataset_path),
        "generation_log_sha256": sha256(log_path),
        "content_sent": "synthetic prompts only; no manuscript, real report text, author data, or unpublished inputs",
        "distribution_anchor": "rights-safe aggregate metadata and development layout counts only"}
    (args.output / "SYNTHETIC_RUN_MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "output": str(args.output), **validation}, ensure_ascii=False))


if __name__ == "__main__":
    main()
