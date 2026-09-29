#!/usr/bin/env python3
"""stdio MCP server for C2GES synthetic-stress tools.

Human annotation, ethics approval, and promoting LLM labels to expert gold
are not implemented and are refused by claim_gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROSPECTIVE = HERE.parent / "prospective_v1"
if str(PROSPECTIVE) not in sys.path:
    sys.path.insert(0, str(PROSPECTIVE))


def find_c2ges_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "C2GES_RELEASE_MARKER.json").is_file():
            return candidate
    raise RuntimeError("C2GES_RELEASE_MARKER.json not found")


PROJECT = find_c2ges_root(HERE)
SYN_ROOT = PROJECT / "03_Reproducibility" / "Data" / "synthetic_stress_v1"
V8 = SYN_ROOT / "run_20260918_heldout_v8"
META = PROJECT / "03_Reproducibility" / "Data" / "rights_safe_metadata" / "rights_safe_report_metadata.csv"
LAYOUT = (
    PROJECT
    / "03_Reproducibility"
    / "Data"
    / "prospective_external_v1"
    / "layout_dev_pilot_v2"
    / "layout_candidate_audit.csv"
)

PROTOCOL = "2024-11-05"


def write_message(payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    sys.stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    sys.stdout.buffer.flush()


def read_message() -> dict | None:
    headers: dict[str, str] = {}
    while True:
        line = sys.stdin.buffer.readline()
        if not line:
            return None
        if line in (b"\r\n", b"\n"):
            break
        key, _, value = line.decode("ascii").partition(":")
        headers[key.strip().lower()] = value.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = sys.stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def ok_text(text: str, extra: dict | None = None) -> dict:
    payload = {"content": [{"type": "text", "text": text}]}
    if extra:
        payload["structuredContent"] = extra
    return payload


def err_text(text: str) -> dict:
    return {"content": [{"type": "text", "text": text}], "isError": True}


def tool_synthetic_status(_args: dict) -> dict:
    runs = []
    if SYN_ROOT.is_dir():
        for path in sorted(SYN_ROOT.glob("run_*/SYNTHETIC_RUN_MANIFEST.json")):
            manifest = json.loads(path.read_text(encoding="utf-8"))
            runs.append(
                {
                    "run": path.parent.name,
                    "version_id": manifest.get("version_id"),
                    "reports": manifest.get("reports"),
                    "series": manifest.get("series"),
                    "synthetic": True,
                    "confirmatory_claims_allowed": False,
                }
            )
    v8_eval = V8 / "evaluation" / "distribution_evaluation.json"
    extra = {
        "runs": runs,
        "v8_exists": V8.is_dir(),
        "v8_gates_pass": json.loads(v8_eval.read_text(encoding="utf-8")).get("deterministic_gate_pass")
        if v8_eval.is_file()
        else None,
        "confirmatory_claims_allowed": False,
    }
    return ok_text(json.dumps(extra, ensure_ascii=False, indent=2), extra)


def tool_evaluate_synthetic(args: dict) -> dict:
    from evaluate_synthetic_distribution import evaluate, load_jsonl, read_numeric_rows

    dataset = Path(args.get("dataset") or (V8 / "synthetic_reports.jsonl"))
    if not dataset.is_file():
        return err_text(f"dataset not found: {dataset}")
    result = evaluate(load_jsonl(dataset), read_numeric_rows(META, LAYOUT))
    result["confirmatory_claims_allowed"] = False
    result["human_or_expert_gold"] = False
    return ok_text(json.dumps({"deterministic_gate_pass": result["deterministic_gate_pass"],
                               "exact_duplicate_rate": result["exact_duplicate_rate"],
                               "gate_ledger": result["gate_ledger"],
                               "confirmatory_claims_allowed": False}, indent=2), result)


def tool_build_synthetic(args: dict) -> dict:
    from build_heldout_synthetic_v8 import main as build_main
    import sys as _sys

    output = Path(args.get("output") or (SYN_ROOT / "run_mcp_heldout"))
    if output.exists():
        return err_text(f"refusing existing output directory: {output}")
    argv = [
        "build_heldout_synthetic_v8.py",
        "--metadata-csv",
        str(META),
        "--layout-csv",
        str(LAYOUT),
        "--output",
        str(output),
        "--seed",
        str(int(args.get("seed", 20260918))),
    ]
    old = _sys.argv
    try:
        _sys.argv = argv
        build_main()
    finally:
        _sys.argv = old
    extra = {"output": str(output), "synthetic": True, "confirmatory_claims_allowed": False}
    return ok_text(json.dumps(extra, indent=2), extra)


def tool_claim_gate(args: dict) -> dict:
    action = str(args.get("action", ""))
    refused = {
        "complete_human_annotation",
        "issue_ethics_approval",
        "upgrade_llm_to_expert",
        "promote_synthetic_to_real",
    }
    extra = {
        "action": action,
        "allowed": False,
        "reason": (
            "This MCP does not create human annotators, ethics determinations, "
            "or expert gold. LLM and synthetic outputs stay machine/fictional."
        ),
        "confirmatory_claims_allowed": False,
    }
    if action in refused or action:
        return ok_text(json.dumps(extra, indent=2), extra)
    extra["action"] = "(none)"
    extra["allowed"] = False
    return ok_text(json.dumps(extra, indent=2), extra)


def tool_debug_kappa(args: dict) -> dict:
    from human_validation import cohen_kappa

    a = list(args.get("a") or ["yes", "yes", "no", "no"])
    b = list(args.get("b") or ["yes", "yes", "no", "no"])
    extra = {"kappa": cohen_kappa(a, b), "n": len(a), "debug_fixture": True, "human_or_expert_gold": False}
    return ok_text(json.dumps(extra), extra)


TOOLS = {
    "synthetic_status": {
        "description": "List C2GES synthetic-stress runs. Fictional fixtures only.",
        "schema": {"type": "object", "properties": {}},
        "handler": tool_synthetic_status,
    },
    "evaluate_synthetic": {
        "description": "Run frozen distribution gates on a synthetic JSONL dataset.",
        "schema": {
            "type": "object",
            "properties": {"dataset": {"type": "string"}},
        },
        "handler": tool_evaluate_synthetic,
    },
    "build_synthetic_heldout": {
        "description": "Build a new held-out fictional synthetic set. Refuses to overwrite.",
        "schema": {
            "type": "object",
            "properties": {
                "output": {"type": "string"},
                "seed": {"type": "integer"},
            },
        },
        "handler": tool_build_synthetic,
    },
    "claim_gate": {
        "description": "Refuse human-annotation, ethics-approval, and LLM-as-expert upgrades.",
        "schema": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "complete_human_annotation",
                        "issue_ethics_approval",
                        "upgrade_llm_to_expert",
                        "promote_synthetic_to_real",
                    ],
                }
            },
            "required": ["action"],
        },
        "handler": tool_claim_gate,
    },
    "debug_kappa": {
        "description": "Compute Cohen's kappa on debug label lists. Not human gold.",
        "schema": {
            "type": "object",
            "properties": {
                "a": {"type": "array", "items": {"type": "string"}},
                "b": {"type": "array", "items": {"type": "string"}},
            },
        },
        "handler": tool_debug_kappa,
    },
}


def tools_list() -> list[dict]:
    return [
        {
            "name": name,
            "description": spec["description"],
            "inputSchema": spec["schema"],
        }
        for name, spec in TOOLS.items()
    ]


def handle(message: dict) -> dict | None:
    method = message.get("method")
    msg_id = message.get("id")
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "result": {
                "protocolVersion": PROTOCOL,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "c2ges-synthetic", "version": "1.0.0"},
            },
        }
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {"tools": tools_list()}}
    if method == "tools/call":
        params = message.get("params") or {}
        name = params.get("name")
        arguments = params.get("arguments") or {}
        spec = TOOLS.get(name)
        if spec is None:
            result = err_text(f"unknown tool: {name}")
        else:
            try:
                result = spec["handler"](arguments)
            except Exception as exc:
                result = err_text(f"{type(exc).__name__}: {exc}")
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}
    if method == "ping":
        return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
    if msg_id is not None:
        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"method not found: {method}"},
        }
    return None


def main() -> None:
    while True:
        message = read_message()
        if message is None:
            break
        reply = handle(message)
        if reply is not None:
            write_message(reply)


if __name__ == "__main__":
    main()
