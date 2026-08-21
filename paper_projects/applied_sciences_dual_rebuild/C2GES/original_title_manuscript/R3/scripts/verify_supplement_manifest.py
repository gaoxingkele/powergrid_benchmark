"""Fresh hash and exact-set verifier for the R3 supplementary allowlist."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R3 = HERE.parent
SUPP = R3 / "supplementary"
MANIFEST = R3 / "SUPPLEMENT_ALLOWLIST.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    recorded = {entry["path"]: entry for entry in data["files"]}
    actual = {p.relative_to(R3).as_posix(): p for p in SUPP.rglob("*") if p.is_file()}
    if set(recorded) != set(actual):
        failures.append({"set_mismatch": {"missing": sorted(set(recorded) - set(actual)), "extra": sorted(set(actual) - set(recorded))}})
    for rel in sorted(set(recorded) & set(actual)):
        path = actual[rel]
        entry = recorded[rel]
        if path.stat().st_size != entry["bytes"]:
            failures.append({"size_mismatch": rel})
        if sha256(path) != entry["sha256"]:
            failures.append({"hash_mismatch": rel})
    status = "PASS" if not failures and data.get("status") == "PASS" else "FAIL"
    print(json.dumps({"status": status, "verified_files": len(actual), "failures": failures}, indent=2))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()

