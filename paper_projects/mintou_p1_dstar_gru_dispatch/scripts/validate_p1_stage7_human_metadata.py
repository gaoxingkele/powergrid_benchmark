#!/usr/bin/env python3
"""Fail-closed human-fact and submission gate for P1 Stage 7.

The ledger is deliberately incomplete until the authors supply and confirm
every fact.  Repository history, sample IEEE assets, and the manuscript's
``ORCID(s): NONE`` rendering are never accepted as human confirmation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "manuscript" / "STAGE7_HUMAN_METADATA.json"
MARKDOWN_PATH = ROOT / "manuscript" / "MANUSCRIPT.md"
JOURNAL_TEX_PATH = ROOT / "manuscript" / "journal_submission" / "paper.tex"
PACKAGE_TEX_PATH = ROOT / "release_package" / "manuscript" / "paper.tex"
PACKAGE_MANIFEST_PATH = ROOT / "release_package" / "PACKAGE_MANIFEST.json"
EVIDENCE_PATH = ROOT / "manuscript" / "DEEP_REVISION_EVIDENCE.md"

REQUIRED_EVIDENCE_HEADINGS = (
    "Title-to-Evidence Map",
    "Primary Estimand and Analysis Unit",
    "Comparison Budget and Data Visibility",
    "Negative and Null Results",
    "Shared Assets and Independent Contribution",
    "New or Rerun Experiments",
    "Unresolved Human Blockers",
)

SAMPLE_PHOTO_SHA256 = {
    "198616cf28c75497af183f8e9dc374f28d26537a4a8dc3ace9a5eee44a0d193c",
    "b673e3d89c4021b5984f91983d3b1cd989348bbc50b3581e7eca2ee7d7352a53",
    "df03222e551646eb458e8b8808cc613efa049b387bc2c6b4adba5dc59963bd05",
}

PLACEHOLDER_PATTERNS = (
    re.compile(r"AUTHOR\s+INPUT\s+REQUIRED", re.IGNORECASE),
    re.compile(r"\bT[B]D\b", re.IGNORECASE),
    re.compile(r"\bTO[D]O\b", re.IGNORECASE),
    re.compile(r"\bX{4,}\b", re.IGNORECASE),
    re.compile(r"Author\s+Details\s+Required\s+before\s+Submission", re.IGNORECASE),
    re.compile(r"must\s+be\s+confirmed\s+by\s+the\s+authors\s+before\s+submission", re.IGNORECASE),
)

ORCID_PATTERN = re.compile(r"^\d{4}-\d{4}-\d{4}-\d{3}[\dX]$")
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
DOI_PATTERN = re.compile(r"^10\.\d{4,9}/\S+$", re.IGNORECASE)


class Gate:
    def __init__(self) -> None:
        self.failures: list[str] = []

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.failures.append(message)


def load_json(gate: Gate, path: Path) -> dict[str, Any]:
    if not path.is_file():
        gate.failures.append(f"required JSON is missing: {path.relative_to(ROOT)}")
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        gate.failures.append(f"cannot parse {path.relative_to(ROOT)}: {exc}")
        return {}
    if not isinstance(value, dict):
        gate.failures.append(f"JSON root is not an object: {path.relative_to(ROOT)}")
        return {}
    return value


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def valid_confirmation_time(value: Any) -> bool:
    if not nonempty(value):
        return False
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def valid_orcid(value: Any) -> bool:
    if not nonempty(value) or not ORCID_PATTERN.fullmatch(value.strip()):
        return False
    digits = value.replace("-", "")
    total = 0
    for character in digits[:15]:
        total = (total + int(character)) * 2
    check = (12 - total % 11) % 11
    expected = "X" if check == 10 else str(check)
    return digits[-1].upper() == expected


def confirmed_statement(gate: Gate, metadata: dict[str, Any], key: str, label: str) -> None:
    section = metadata.get(key)
    gate.require(isinstance(section, dict), f"{label}: metadata section is missing")
    if not isinstance(section, dict):
        return
    gate.require(section.get("confirmed") is True, f"{label}: human confirmation is missing")
    gate.require(nonempty(section.get("statement")), f"{label}: final statement is missing")
    gate.require(nonempty(section.get("tex_statement")), f"{label}: final TeX rendering is missing")


def validate_evidence_contract(gate: Gate) -> None:
    gate.require(EVIDENCE_PATH.is_file(), "manuscript/DEEP_REVISION_EVIDENCE.md is missing")
    if not EVIDENCE_PATH.is_file():
        return
    text = EVIDENCE_PATH.read_text(encoding="utf-8", errors="strict")
    headings = {match.group(1).strip() for match in re.finditer(r"^#\s+(.+?)\s*$", text, re.MULTILINE)}
    for heading in REQUIRED_EVIDENCE_HEADINGS:
        gate.require(heading in headings, f"DEEP_REVISION_EVIDENCE heading is missing: {heading}")


def validate_authors(gate: Gate, metadata: dict[str, Any]) -> tuple[set[str], list[dict[str, Any]]]:
    authors = metadata.get("authors")
    gate.require(isinstance(authors, list) and bool(authors), "authors: final names and order are unconfirmed")
    if not isinstance(authors, list) or not authors:
        return set(), []

    author_ids: set[str] = set()
    expected_orders = list(range(1, len(authors) + 1))
    observed_orders: list[Any] = []
    for index, author in enumerate(authors, start=1):
        label = f"authors[{index}]"
        gate.require(isinstance(author, dict), f"{label}: entry is not an object")
        if not isinstance(author, dict):
            continue
        author_id = author.get("id")
        gate.require(nonempty(author_id), f"{label}: stable author id is missing")
        if nonempty(author_id):
            gate.require(author_id not in author_ids, f"{label}: duplicate author id {author_id!r}")
            author_ids.add(author_id)
        observed_orders.append(author.get("order"))
        gate.require(nonempty(author.get("name")), f"{label}: author name is missing")
        gate.require(nonempty(author.get("tex_name")), f"{label}: TeX-rendered author name is missing")
        affiliations = author.get("affiliation_ids")
        gate.require(
            isinstance(affiliations, list) and bool(affiliations) and all(nonempty(item) for item in affiliations),
            f"{label}: affiliation mapping is missing",
        )
        roles = author.get("credit_roles")
        gate.require(
            isinstance(roles, list) and bool(roles) and all(nonempty(item) for item in roles),
            f"{label}: CRediT roles are missing",
        )
        gate.require(nonempty(author.get("biography")), f"{label}: biography is missing")
        gate.require(nonempty(author.get("tex_biography")), f"{label}: TeX-rendered biography is missing")
        gate.require(nonempty(author.get("photograph_path")), f"{label}: photograph path is missing")
        gate.require(author.get("confirmed") is True, f"{label}: name/order/roles/biography/photo are not human-confirmed")
    gate.require(observed_orders == expected_orders, "authors: order values must be consecutive and match array order")
    return author_ids, authors


def validate_affiliations(gate: Gate, metadata: dict[str, Any], authors: list[dict[str, Any]]) -> set[str]:
    affiliations = metadata.get("affiliations")
    gate.require(isinstance(affiliations, list) and bool(affiliations), "affiliations: confirmed records are missing")
    if not isinstance(affiliations, list) or not affiliations:
        return set()
    affiliation_ids: set[str] = set()
    for index, affiliation in enumerate(affiliations, start=1):
        label = f"affiliations[{index}]"
        gate.require(isinstance(affiliation, dict), f"{label}: entry is not an object")
        if not isinstance(affiliation, dict):
            continue
        affiliation_id = affiliation.get("id")
        gate.require(nonempty(affiliation_id), f"{label}: id is missing")
        if nonempty(affiliation_id):
            gate.require(affiliation_id not in affiliation_ids, f"{label}: duplicate id {affiliation_id!r}")
            affiliation_ids.add(affiliation_id)
        gate.require(nonempty(affiliation.get("address")), f"{label}: complete institutional address is missing")
        gate.require(nonempty(affiliation.get("tex_address")), f"{label}: TeX-rendered institutional address is missing")
        gate.require(affiliation.get("confirmed") is True, f"{label}: human confirmation is missing")
    for index, author in enumerate(authors, start=1):
        if not isinstance(author, dict):
            continue
        author_affiliations = author.get("affiliation_ids")
        if not isinstance(author_affiliations, list):
            continue
        for affiliation_id in author_affiliations:
            gate.require(affiliation_id in affiliation_ids, f"authors[{index}]: unknown affiliation id {affiliation_id!r}")
    return affiliation_ids


def validate_photographs(
    gate: Gate,
    authors: list[dict[str, Any]],
    *,
    require_package: bool,
) -> None:
    for index, author in enumerate(authors, start=1):
        if not isinstance(author, dict) or not nonempty(author.get("photograph_path")):
            continue
        relative = Path(author["photograph_path"])
        gate.require(not relative.is_absolute() and ".." not in relative.parts, f"authors[{index}]: photograph path must stay inside the worktree")
        if relative.is_absolute() or ".." in relative.parts:
            continue
        photo = ROOT / relative
        gate.require(photo.is_file(), f"authors[{index}]: photograph file is missing: {relative.as_posix()}")
        if not photo.is_file():
            continue
        gate.require(photo.suffix.lower() in {".png", ".jpg", ".jpeg"}, f"authors[{index}]: photograph must be PNG or JPEG")
        digest = sha256(photo)
        gate.require(digest not in SAMPLE_PHOTO_SHA256, f"authors[{index}]: bundled IEEE sample portrait cannot be used")
        try:
            journal_relative = photo.relative_to(ROOT / "manuscript" / "journal_submission")
        except ValueError:
            gate.failures.append(f"authors[{index}]: photograph must be under manuscript/journal_submission")
            continue
        if require_package:
            package_photo = ROOT / "release_package" / "manuscript" / journal_relative
            gate.require(package_photo.is_file(), f"authors[{index}]: release-package photograph is missing")
            if package_photo.is_file():
                gate.require(sha256(package_photo) == digest, f"authors[{index}]: source/package photograph hashes differ")


def validate_correspondence(gate: Gate, metadata: dict[str, Any], author_ids: set[str]) -> None:
    section = metadata.get("correspondence")
    gate.require(isinstance(section, dict), "correspondence: metadata section is missing")
    if not isinstance(section, dict):
        return
    gate.require(section.get("confirmed") is True, "correspondence: human confirmation is missing")
    gate.require(section.get("author_id") in author_ids, "correspondence: corresponding author is not in the confirmed author list")
    email = section.get("email")
    gate.require(nonempty(email) and EMAIL_PATTERN.fullmatch(email.strip()) is not None, "correspondence: valid e-mail is missing")
    gate.require(nonempty(section.get("postal_address")), "correspondence: full postal detail is missing")
    gate.require(nonempty(section.get("tex_text")), "correspondence: final TeX rendering is missing")


def validate_orcid(gate: Gate, metadata: dict[str, Any]) -> None:
    section = metadata.get("orcid")
    gate.require(isinstance(section, dict), "ORCID: metadata section is missing")
    if not isinstance(section, dict):
        return
    gate.require(section.get("manuscript_rendering") == "NONE", "ORCID: manuscript rendering must remain exactly NONE")
    gate.require(
        section.get("none_satisfies_submission_account_requirement") is False,
        "ORCID: NONE must not be treated as satisfying the IEEE submission-account requirement",
    )
    account = section.get("submitting_account")
    gate.require(isinstance(account, dict), "ORCID: submitting-account record is missing")
    if not isinstance(account, dict):
        return
    gate.require(account.get("confirmed") is True, "ORCID: submitting-account ORCID is not human-confirmed")
    gate.require(valid_orcid(account.get("value")), "ORCID: submitting-account ORCID is missing or checksum-invalid")


def validate_remaining_declarations(gate: Gate, metadata: dict[str, Any]) -> None:
    for key, label in (
        ("funding", "funding statement"),
        ("credit_statement", "CRediT contribution statement"),
        ("conflict_of_interest", "conflict declaration"),
        ("acknowledgment", "acknowledgment"),
        ("ai_use", "AI-use confirmation"),
        ("ethics", "ethics declaration"),
    ):
        confirmed_statement(gate, metadata, key, label)

    apc = metadata.get("apc")
    gate.require(isinstance(apc, dict), "APC choice: metadata section is missing")
    if isinstance(apc, dict):
        gate.require(apc.get("confirmed") is True, "APC choice: human confirmation is missing")
        gate.require(nonempty(apc.get("choice")), "APC choice: final choice is missing")

    artifact = metadata.get("public_artifact")
    gate.require(isinstance(artifact, dict), "public repository/DOI: metadata section is missing")
    if isinstance(artifact, dict):
        gate.require(artifact.get("confirmed") is True, "public repository/DOI: human confirmation is missing")
        url = artifact.get("repository_url")
        doi = artifact.get("archival_doi")
        valid_url = nonempty(url) and str(url).strip().lower().startswith("https://")
        valid_doi = nonempty(doi) and DOI_PATTERN.fullmatch(str(doi).strip()) is not None
        gate.require(valid_url or valid_doi, "public repository/DOI: a public HTTPS URL or archival DOI is missing")

    submission = metadata.get("concurrent_and_prior_submission")
    gate.require(isinstance(submission, dict), "concurrent/prior-submission declaration: metadata section is missing")
    if isinstance(submission, dict):
        gate.require(submission.get("confirmed") is True, "concurrent/prior-submission declaration: human confirmation is missing")
        gate.require(isinstance(submission.get("concurrent_submission"), bool), "concurrent submission: explicit yes/no is missing")
        gate.require(isinstance(submission.get("prior_submission"), bool), "prior submission: explicit yes/no is missing")
        gate.require(nonempty(submission.get("statement")), "concurrent/prior-submission declaration: final statement is missing")


def validate_global_confirmation(gate: Gate, metadata: dict[str, Any]) -> None:
    confirmation = metadata.get("human_confirmation")
    gate.require(isinstance(confirmation, dict), "global human confirmation record is missing")
    if not isinstance(confirmation, dict):
        return
    gate.require(confirmation.get("confirmed") is True, "global human confirmation is missing")
    gate.require(nonempty(confirmation.get("confirmed_by")), "global confirmation: confirmer identity is missing")
    gate.require(valid_confirmation_time(confirmation.get("confirmed_at_utc")), "global confirmation: timezone-aware timestamp is missing or invalid")
    gate.require(metadata.get("gate_status") == "ready_for_submission_checks", "gate status is not ready_for_submission_checks")


def validate_rendered_files(
    gate: Gate,
    metadata: dict[str, Any],
    authors: list[dict[str, Any]],
    *,
    require_package: bool,
) -> None:
    required_files = [MARKDOWN_PATH, JOURNAL_TEX_PATH]
    if require_package:
        required_files.append(PACKAGE_TEX_PATH)
    texts: dict[Path, str] = {}
    for path in required_files:
        gate.require(path.is_file(), f"required manuscript file is missing: {path.relative_to(ROOT)}")
        if path.is_file():
            texts[path] = path.read_text(encoding="utf-8", errors="strict")
    for path, text in texts.items():
        for pattern in PLACEHOLDER_PATTERNS:
            gate.require(pattern.search(text) is None, f"placeholder remains in {path.relative_to(ROOT)}: {pattern.pattern}")

    markdown = texts.get(MARKDOWN_PATH, "")
    journal_tex = texts.get(JOURNAL_TEX_PATH, "")
    package_tex = texts.get(PACKAGE_TEX_PATH, "")
    gate.require(re.search(r"^\*\*ORCID\(s\):\*\* NONE\s*$", markdown, re.MULTILINE) is not None, "Markdown must render ORCID(s): NONE")
    tex_outputs = [("journal TeX", journal_tex)]
    if require_package:
        tex_outputs.append(("release-package TeX", package_tex))
    for label, text in tex_outputs:
        gate.require("ORCID(s): NONE" in text, f"{label} must render ORCID(s): NONE")
    if require_package and JOURNAL_TEX_PATH.is_file() and PACKAGE_TEX_PATH.is_file():
        gate.require(JOURNAL_TEX_PATH.read_bytes() == PACKAGE_TEX_PATH.read_bytes(), "journal and release-package TeX bytes differ")

    for index, author in enumerate(authors, start=1):
        if not isinstance(author, dict) or not nonempty(author.get("name")):
            continue
        name = author["name"].strip()
        gate.require(name in markdown, f"authors[{index}]: name is absent from Markdown manuscript")
        if nonempty(author.get("tex_name")):
            gate.require(author["tex_name"].strip() in journal_tex, f"authors[{index}]: name is absent from journal TeX")
            if require_package:
                gate.require(author["tex_name"].strip() in package_tex, f"authors[{index}]: name is absent from release-package TeX")
        biography = author.get("biography")
        tex_biography = author.get("tex_biography")
        if nonempty(biography):
            gate.require(biography.strip() in markdown, f"authors[{index}]: biography is absent from Markdown manuscript")
        if nonempty(tex_biography):
            gate.require(tex_biography.strip() in journal_tex, f"authors[{index}]: biography is absent from journal TeX")
            if require_package:
                gate.require(tex_biography.strip() in package_tex, f"authors[{index}]: biography is absent from release-package TeX")

    affiliations = metadata.get("affiliations")
    if isinstance(affiliations, list):
        for index, affiliation in enumerate(affiliations, start=1):
            if not isinstance(affiliation, dict):
                continue
            address = affiliation.get("address")
            tex_address = affiliation.get("tex_address")
            if nonempty(address):
                gate.require(address.strip() in markdown, f"affiliations[{index}]: address is absent from Markdown manuscript")
            if nonempty(tex_address):
                gate.require(tex_address.strip() in journal_tex, f"affiliations[{index}]: address is absent from journal TeX")
                if require_package:
                    gate.require(tex_address.strip() in package_tex, f"affiliations[{index}]: address is absent from release-package TeX")

    correspondence = metadata.get("correspondence")
    if isinstance(correspondence, dict):
        email = correspondence.get("email")
        postal_address = correspondence.get("postal_address")
        tex_text = correspondence.get("tex_text")
        if nonempty(email):
            gate.require(email.strip() in markdown, "correspondence e-mail is absent from Markdown manuscript")
        if nonempty(postal_address):
            gate.require(postal_address.strip() in markdown, "correspondence address is absent from Markdown manuscript")
        if nonempty(tex_text):
            gate.require(tex_text.strip() in journal_tex, "correspondence text is absent from journal TeX")
            if require_package:
                gate.require(tex_text.strip() in package_tex, "correspondence text is absent from release-package TeX")

    for key, label in (
        ("funding", "funding statement"),
        ("credit_statement", "CRediT contribution statement"),
        ("conflict_of_interest", "conflict declaration"),
        ("acknowledgment", "acknowledgment"),
        ("ai_use", "AI-use statement"),
        ("ethics", "ethics statement"),
    ):
        section = metadata.get(key)
        if isinstance(section, dict) and nonempty(section.get("statement")):
            gate.require(section["statement"].strip() in markdown, f"{label} is absent from Markdown manuscript")
        if isinstance(section, dict) and nonempty(section.get("tex_statement")):
            gate.require(section["tex_statement"].strip() in journal_tex, f"{label} is absent from journal TeX")
            if require_package:
                gate.require(section["tex_statement"].strip() in package_tex, f"{label} is absent from release-package TeX")

    artifact = metadata.get("public_artifact")
    if isinstance(artifact, dict):
        for field in ("repository_url", "archival_doi"):
            value = artifact.get(field)
            if nonempty(value):
                gate.require(value.strip() in markdown, f"public artifact {field} is absent from Markdown manuscript")
                gate.require(value.strip() in journal_tex, f"public artifact {field} is absent from journal TeX")
                if require_package:
                    gate.require(value.strip() in package_tex, f"public artifact {field} is absent from release-package TeX")


def validate_release_manifest(gate: Gate) -> None:
    manifest = load_json(gate, PACKAGE_MANIFEST_PATH)
    if not manifest:
        return
    gate.require(manifest.get("explicit_human_placeholders_retained") is False, "release manifest still records retained human placeholders")
    gate.require(manifest.get("stage7_human_metadata_complete") is True, "release manifest does not record completed Stage 7 metadata")
    gate.require(manifest.get("built_in_pdf_integrity") == "pass", "release manifest does not record passed PDF integrity")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("prebuild", "release"), default="release")
    args = parser.parse_args()
    require_package = args.phase == "release"
    gate = Gate()
    metadata = load_json(gate, METADATA_PATH)
    validate_evidence_contract(gate)
    if metadata:
        gate.require(metadata.get("schema") == "p1_stage7_human_metadata", "metadata schema is invalid")
        gate.require(metadata.get("schema_version") == 1, "metadata schema version is invalid")
        author_ids, authors = validate_authors(gate, metadata)
        validate_affiliations(gate, metadata, authors)
        validate_photographs(gate, authors, require_package=require_package)
        validate_correspondence(gate, metadata, author_ids)
        validate_orcid(gate, metadata)
        validate_remaining_declarations(gate, metadata)
        validate_global_confirmation(gate, metadata)
        validate_rendered_files(gate, metadata, authors, require_package=require_package)
    if require_package:
        validate_release_manifest(gate)

    if gate.failures:
        print("STAGE7 HUMAN METADATA BLOCKED")
        for index, failure in enumerate(gate.failures, start=1):
            print(f"{index:02d}. {failure}")
        return 1
    print(f"STAGE7 HUMAN METADATA PASS phase={args.phase}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
