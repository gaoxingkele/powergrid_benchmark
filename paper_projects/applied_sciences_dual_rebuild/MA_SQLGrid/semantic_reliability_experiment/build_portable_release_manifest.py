"""Build a repository-root-relative manifest for the semantic release."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-manifest", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    source = json.loads(args.source_manifest.read_text(encoding="utf-8"))

    paths = [Path(item["path"]).resolve() for item in source["artifacts"]]
    semantic = args.source_manifest.resolve().parents[1]
    ma_root = semantic.parent
    extras = [
        semantic / "exact_sign_enumeration" / "exact_cluster_sign_tests.csv",
        semantic / "exact_sign_enumeration" / "EXACT_SIGN_ENUMERATION_REPORT.json",
        semantic / "POST_SCORE_INDEPENDENT_AUDIT_A.json",
        semantic / "POST_SCORE_INDEPENDENT_AUDIT_B.json",
        semantic / "formal_v5_analysis" / "MANUSCRIPT_FIGURE_LINEAGE.json",
        ma_root / "manuscript_applsci" / "paper_applsci.tex",
        ma_root / "manuscript_applsci" / "tables" / "table_semantic_cell_robustness.tex",
        ma_root / "manuscript_applsci" / "tables" / "table_semantic_effects.tex",
        ma_root / "manuscript_applsci" / "figures" / "results" / "fig04_semantic_reliability.pdf",
    ]
    paths.extend(path.resolve() for path in extras)

    artifacts = []
    seen = set()
    for path in paths:
        if not path.is_file():
            raise FileNotFoundError(path)
        try:
            relative = path.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"Artifact is outside repository root: {path}") from exc
        portable = relative.as_posix()
        if portable in seen:
            continue
        seen.add(portable)
        artifacts.append({"path": portable, "bytes": path.stat().st_size, "sha256": sha256(path)})

    root_marker = root / "README.md"
    manifest = {
        "schema_version": "ma-sqlgrid-semantic-portable-release-v1",
        "path_contract": "all artifact paths are POSIX-style and relative to a caller-supplied repository root",
        "freeze_content_sha256": source["freeze_content_sha256"],
        "invariants": source["invariants"],
        "root_marker": {"path": "README.md", "bytes": root_marker.stat().st_size, "sha256": sha256(root_marker)},
        "artifacts": artifacts,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PORTABLE_MANIFEST_PASS artifacts={len(artifacts)}")


if __name__ == "__main__":
    main()
