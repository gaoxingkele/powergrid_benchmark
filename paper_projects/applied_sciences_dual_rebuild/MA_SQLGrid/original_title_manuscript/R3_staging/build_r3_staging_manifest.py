"""Verify the v3 freeze and hash additive R3 staging artifacts."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


STAGING = Path(__file__).resolve().parent
ROOT = STAGING.parents[4]
V3 = ROOT / "paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/original_title_rebuild/prospective_from_freeze_offline_study_v3"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


freeze = json.loads((V3 / "freeze_manifest.json").read_text(encoding="utf-8"))
checks = []
for key, record in freeze["files"].items():
    path = ROOT / record["path"]
    checks.append(
        {
            "key": key,
            "path": record["path"],
            "expected_sha256": record["sha256"],
            "actual_sha256": digest(path),
            "expected_bytes": record["bytes"],
            "actual_bytes": path.stat().st_size,
        }
    )
for row in checks:
    row["passed"] = row["expected_sha256"] == row["actual_sha256"] and row["expected_bytes"] == row["actual_bytes"]
report = {
    "schema_version": "ma-sqlgrid-r3-freeze-integrity-reverify-v1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "freeze_manifest_sha256": digest(V3 / "freeze_manifest.json"),
    "verified": sum(row["passed"] for row in checks),
    "expected": len(checks),
    "passed": all(row["passed"] for row in checks),
    "checks": checks,
}
(STAGING / "FREEZE_INTEGRITY_REVERIFY.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
if not report["passed"]:
    raise SystemExit("frozen file mismatch")

files = []
for path in sorted(STAGING.rglob("*")):
    if not path.is_file() or path.name == "R3_STAGING_MANIFEST.json" or "__pycache__" in path.parts:
        continue
    files.append({"path": path.relative_to(STAGING).as_posix(), "sha256": digest(path), "bytes": path.stat().st_size})
external = []
for path in [V3 / "SUPERSESSION_NOTICE.json", V3 / "SUPERSESSION_NOTICE.md", V3 / "INDEPENDENT_RELEASE_AUDIT_V3.md"]:
    external.append({"path": path.relative_to(ROOT).as_posix(), "sha256": digest(path), "bytes": path.stat().st_size})
manifest = {
    "schema_version": "ma-sqlgrid-r3-staging-manifest-v1",
    "generated_at_utc": datetime.now(timezone.utc).isoformat(),
    "evidence_class": "additive R3 staging; no modification of frozen v3 artifacts",
    "freeze_reverification": {"verified": report["verified"], "expected": report["expected"], "passed": report["passed"]},
    "files": files,
    "external_controlling_records": external,
}
(STAGING / "R3_STAGING_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
