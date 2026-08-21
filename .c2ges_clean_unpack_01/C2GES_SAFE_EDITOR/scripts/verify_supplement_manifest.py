"""Fresh exact-set, bytes, hash, compartment and required-role verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SUPPLEMENT = ROOT / "supplementary"
MANIFEST = ROOT / "SUPPLEMENT_ALLOWLIST.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    recorded = {item["path"]: item for item in data["files"]}
    actual = {path.relative_to(ROOT).as_posix(): path for path in SUPPLEMENT.rglob("*") if path.is_file()}
    if set(recorded) != set(actual):
        failures.append({"exact_set_mismatch": {"missing": sorted(set(recorded) - set(actual)), "extra": sorted(set(actual) - set(recorded))}})
    roles = [item["required_role"] for item in data["files"] if item.get("required_role")]
    if len(roles) != data["required_role_count"] or len(roles) != len(set(roles)):
        failures.append({"required_role_cardinality": {"declared": data["required_role_count"], "observed": len(roles), "unique": len(set(roles))}})
    for rel in sorted(set(recorded) & set(actual)):
        item = recorded[rel]
        path = actual[rel]
        if path.stat().st_size != item["bytes"]:
            failures.append({"bytes_mismatch": rel})
        if digest(path) != item["sha256"]:
            failures.append({"hash_mismatch": rel})
        restricted = "restricted_local_only" in path.parts
        if item["external_transfer_allowed"] == restricted:
            failures.append({"compartment_transfer_flag_mismatch": rel})
    status = "PASS" if not failures and data.get("status") == "PASS" else "FAIL"
    result = {"status": status, "verified_files": len(actual), "verified_required_roles": len(roles), "failures": failures}
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
