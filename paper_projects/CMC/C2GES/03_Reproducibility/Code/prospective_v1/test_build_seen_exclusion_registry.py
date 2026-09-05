from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from build_seen_exclusion_registry import build


class SeenExclusionRegistryTests(unittest.TestCase):
    def test_historical_and_unique_prefreeze_items_are_all_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            historical = root / "historical.csv"
            with historical.open("w", encoding="utf-8", newline="") as stream:
                writer = csv.DictWriter(
                    stream,
                    fieldnames=["doc_id", "report_series_id", "source_url", "pdf_sha256"],
                )
                writer.writeheader()
                writer.writerow({
                    "doc_id": "old-1", "report_series_id": "series-1",
                    "source_url": "https://example.org/old.pdf", "pdf_sha256": "A" * 64,
                })
            access_log = root / "access.md"
            access_log.write_text(
                "`https://example.org/old.pdf`\n`https://example.org/exposed.pdf`\n"
                "`https://example.org/exposed.pdf`\n",
                encoding="utf-8",
            )
            rows = build(historical, access_log)
            self.assertEqual(len(rows), 2)
            self.assertEqual(
                {row["exposure_class"] for row in rows},
                {"historical_corpus", "prefreeze_content_exposure"},
            )
            self.assertTrue(all(
                row["disposition"] == "EXCLUDE_FROM_CONFIRMATORY_EXTERNAL" for row in rows
            ))


if __name__ == "__main__":
    unittest.main()
