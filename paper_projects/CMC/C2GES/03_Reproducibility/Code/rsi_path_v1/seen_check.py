"""Record whether any lawful unused public series exists for confirmatory eval."""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[2]
REGISTRY = PROJECT / "03_Reproducibility" / "Data" / "prospective_external_v1" / "SEEN_EXCLUSION_REGISTRY.csv"
LOG = PROJECT / "03_Reproducibility" / "Data" / "prospective_external_v1" / "PRE_FREEZE_ACCESS_LOG.md"
OUT = HERE / "SEEN_CHECK.json"


def main() -> dict:
    rows = list(csv.DictReader(REGISTRY.read_text(encoding="utf-8-sig").splitlines()))
    dispositions = sorted({row.get("disposition", "") for row in rows})
    classes = sorted({row.get("exposure_class", "") for row in rows})
    payload = {
        "registry": str(REGISTRY),
        "n_registry_rows": len(rows),
        "exposure_classes": classes,
        "dispositions": dispositions,
        "all_excluded_from_confirmatory_external": all(
            row.get("disposition") == "EXCLUDE_FROM_CONFIRMATORY_EXTERNAL" for row in rows
        ),
        "pre_freeze_log_exists": LOG.is_file(),
        "unused_lawful_public_series_available": False,
        "eval_corpus_decision": "15-report NERC retained test labeled held-out-for-this-revision, not unseen confirmatory",
    }
    OUT.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
