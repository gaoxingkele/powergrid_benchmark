"""Regression tests for the W7 C2GES citation/compliance audit."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import audit_w7


HERE = Path(__file__).resolve().parent


class W7AuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads((HERE / "W7_CITATION_COMPLIANCE_AUDIT.json").read_text(encoding="utf-8"))

    def test_source_hashes_and_scope(self) -> None:
        self.assertEqual(self.audit["scope"], "read-only audit; no TeX/Bib modification")
        for item in self.audit["sources"]:
            path = audit_w7.REPO / item["path"]
            self.assertEqual(item["sha256"], hashlib.sha256(path.read_bytes()).hexdigest())

    def test_bib_and_citation_integrity(self) -> None:
        self.assertEqual(self.audit["summary"]["old_bib_entries"], 48)
        self.assertEqual(self.audit["summary"]["old_unique_cited_keys"], 14)
        self.assertEqual(self.audit["old_tex"]["undefined_citation_keys"], [])
        self.assertEqual(self.audit["old_bib"]["duplicate_doi_groups"], [])
        self.assertEqual(self.audit["old_bib"]["duplicate_title_groups"], [])
        self.assertEqual(self.audit["old_bib"]["explicit_doi_field_count"], 0)
        self.assertEqual(self.audit["missing_reusable_keys_internal_error"], [])

    def test_abstract_corpus_and_draft_gaps(self) -> None:
        self.assertLessEqual(self.audit["summary"]["old_abstract_words"], 200)
        self.assertEqual(self.audit["summary"]["downloaded_applsci_corpus_n"], 10)
        self.assertEqual(self.audit["summary"]["w5_citation_count"], 0)
        self.assertEqual(self.audit["summary"]["w6_citation_count"], 0)
        self.assertGreaterEqual(len(self.audit["claim_citation_gaps"]), 10)

    def test_mandatory_boundaries_and_blockers(self) -> None:
        table = {item["item"]: item["status"] for item in self.audit["mdpi_compliance"]}
        self.assertEqual(table["Oracle disclosure"], "pass_in_new_drafts")
        self.assertEqual(table["NERC provenance disclosure"], "pass_in_new_drafts")
        self.assertIn(table["AI-use disclosure"], {"open", "pass"})
        self.assertEqual(table["Current title truthful to frozen role result"], "blocker")
        self.assertEqual(table["Citation coverage in rebuilt drafts"], "blocker")
        self.assertFalse(self.audit["summary"]["submission_ready"])

    def test_verification_urls_are_restricted(self) -> None:
        allowed = ("https://doi.org/", "https://www.techscience.com/")
        self.assertTrue(all(item["url"].startswith(allowed) for item in self.audit["verification_urls"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
