#!/usr/bin/env python3
"""Create/verify the immutable W3-to-W4 C2GES execution fingerprint."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


PROTOCOL_DIRS = ("oracle", "predicted", "label_blind")
ALLOWED_CONFIG_DIFFERENCES = {"out", "protocol", "predicted_labels", "protocol_definition", "seed"}


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tree_sha(root: Path) -> dict:
    digest = hashlib.sha256()
    files = [path for path in root.rglob("*") if path.is_file()]
    for path in sorted(files, key=lambda item: item.relative_to(root).as_posix()):
        rel = path.relative_to(root).as_posix()
        value = file_sha(path)
        digest.update(rel.encode("utf-8"))
        digest.update(value.encode("ascii"))
    return {"sha256": digest.hexdigest(), "file_count": len(files)}


def common_config(config: dict) -> dict:
    return {key: value for key, value in config.items() if key not in ALLOWED_CONFIG_DIFFERENCES}


def current_fingerprint(args) -> dict:
    w3_configs = {}
    starts = []
    for directory in PROTOCOL_DIRS:
        run_dir = args.w3_root / directory
        w3_configs[directory] = json.loads((run_dir / "run_config.json").read_text(encoding="utf-8"))
        starts.append(json.loads((run_dir / "resource_usage.json").read_text(encoding="utf-8"))["started_utc"])
    common = common_config(w3_configs["oracle"])
    if any(common_config(value) != common for value in w3_configs.values()):
        raise RuntimeError("W3 protocol run configurations differ outside the allowed protocol/seed/output fields")
    manifest = json.loads(args.dataset_manifest.read_text(encoding="utf-8"))
    model_ref = (args.encoder_cache / "refs" / "main").read_text(encoding="utf-8").strip()
    snapshot = args.encoder_cache / "snapshots" / model_ref
    if not snapshot.is_dir():
        raise FileNotFoundError(f"missing encoder snapshot {snapshot}")
    code_files = [args.code_dir / "c2ges_learnable.py", args.code_dir / "run_c2_protocol_pilot.py"]
    return {
        "w3_started_utc": min(starts),
        "base_run_config": common,
        "dataset_corpus_sha256": manifest["content_hashes"]["corpus_sha256"],
        "dataset_manifest_sha256": file_sha(args.dataset_manifest),
        "w3_input_data_hashes": {
            split: json.loads((args.w3_root / "oracle" / "provenance.json").read_text(encoding="utf-8"))["data_hashes"][split]["sha256"]
            for split in ("train", "dev", "test")
        },
        "predicted_labels_sha256": file_sha(args.predicted_labels),
        "core_code": {
            path.name: {"sha256": file_sha(path), "mtime_utc": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()}
            for path in code_files
        },
        "encoder": {
            "model_id": common["encoder"],
            "snapshot_ref": model_ref,
            **tree_sha(snapshot),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("create", "verify"))
    parser.add_argument("--freeze", type=Path, required=True)
    parser.add_argument("--w3-root", type=Path, required=True)
    parser.add_argument("--dataset-manifest", type=Path, required=True)
    parser.add_argument("--predicted-labels", type=Path, required=True)
    parser.add_argument("--code-dir", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument(
        "--encoder-cache",
        type=Path,
        default=Path.home() / ".cache/huggingface/hub/models--sentence-transformers--all-MiniLM-L6-v2",
    )
    args = parser.parse_args()
    current = current_fingerprint(args)
    if args.mode == "create":
        if args.freeze.exists():
            parser.error(f"refusing to overwrite existing freeze manifest: {args.freeze}")
        w3_start = datetime.fromisoformat(current["w3_started_utc"])
        late = {name: item for name, item in current["core_code"].items() if datetime.fromisoformat(item["mtime_utc"]) > w3_start}
        if late:
            raise RuntimeError(f"cannot prove W3 code identity: core files modified after W3 began: {late}")
        args.freeze.parent.mkdir(parents=True, exist_ok=True)
        payload = {"created_utc": datetime.now(timezone.utc).isoformat(), "status": "frozen", "fingerprint": current}
        args.freeze.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"status": "created", "freeze": str(args.freeze), "freeze_sha256": file_sha(args.freeze)}, indent=2))
        return 0
    expected = json.loads(args.freeze.read_text(encoding="utf-8"))["fingerprint"]
    if current != expected:
        differences = {key: {"expected": expected.get(key), "current": current.get(key)} for key in sorted(set(expected) | set(current)) if expected.get(key) != current.get(key)}
        print(json.dumps({"status": "mismatch", "differences": differences}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps({"status": "verified", "freeze_sha256": file_sha(args.freeze)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
