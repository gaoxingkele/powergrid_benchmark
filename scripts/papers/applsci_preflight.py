#!/usr/bin/env python3
"""Read-only pre-submission audit for MDPI Applied Sciences projects.

The tool deliberately does not rewrite manuscript text.  It checks mechanical
contracts, surfaces manual scientific/portal gates, and can compare the current
manuscript with a Git baseline to make revision drift visible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


SCHEMA_VERSION = "1.0"
DEFAULT_TEX = Path("01_Manuscript/LaTeX/paper_applsci.tex")
REQUIRED_FRONT_MACROS = (
    "Title",
    "Author",
    "AuthorNames",
    "address",
    "corres",
    "abstract",
    "keyword",
)
REQUIRED_BACK_MACROS = (
    "authorcontributions",
    "funding",
    "institutionalreview",
    "informedconsent",
    "dataavailability",
    "acknowledgments",
    "conflictsofinterest",
)
PLACEHOLDER_PATTERNS = {
    "TODO": re.compile(r"\bTODO\b", re.IGNORECASE),
    "TBD": re.compile(r"\bTBD\b", re.IGNORECASE),
    "author-input marker": re.compile(r"AUTHOR\s+(?:INPUT|ACTION)\s+REQUIRED", re.IGNORECASE),
    "example address": re.compile(r"(?:example\.com|example\.org)", re.IGNORECASE),
    "placeholder": re.compile(r"\bPLACEHOLDER\b", re.IGNORECASE),
    "insert marker": re.compile(r"\[(?:INSERT|TO BE CONFIRMED)[^\]]*\]", re.IGNORECASE),
}
CLAIM_TERMS = {
    "outperformance": re.compile(r"\b(?:outperform\w*|superior(?:ity)?)\b", re.IGNORECASE),
    "effectiveness": re.compile(r"\b(?:effective(?:ness)?|improv\w*)\b", re.IGNORECASE),
    "generalization": re.compile(r"\b(?:generali[sz]\w*|transferab\w*)\b", re.IGNORECASE),
    "deployment": re.compile(r"\b(?:deploy\w*|operational)\b", re.IGNORECASE),
    "causality": re.compile(r"\bcaus\w*\b", re.IGNORECASE),
    "significance": re.compile(r"\bstatistically\s+significant\b|\bsignificant(?:ly)?\b", re.IGNORECASE),
    "registration": re.compile(r"\b(?:pre-?register\w*|register\w*)\b", re.IGNORECASE),
}
GRAPHIC_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg")


@dataclass(frozen=True)
class Check:
    check_id: str
    status: str
    severity: str
    message: str
    evidence: list[str]


def _check(
    check_id: str,
    status: str,
    severity: str,
    message: str,
    evidence: Iterable[str] = (),
) -> Check:
    return Check(check_id, status, severity, message, list(evidence))


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        match = re.search(r"(?<!\\)%", line)
        lines.append(line[: match.start()] if match else line)
    return "\n".join(lines)


def extract_macro_argument(text: str, macro: str) -> str | None:
    match = re.search(rf"\\{re.escape(macro)}\s*\{{", text)
    if not match:
        return None
    start = match.end()
    depth = 1
    index = start
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start:index]
        index += 1
    return None


def tex_to_plain_text(text: str) -> str:
    value = strip_comments(text)
    value = re.sub(r"\\(?:cite|ref|eqref|autoref|pageref)[A-Za-z*]*\{[^{}]*\}", " ", value)
    value = re.sub(r"\\(?:url|href)\{[^{}]*\}(?:\{([^{}]*)\})?", r" \1 ", value)
    previous = None
    while previous != value:
        previous = value
        value = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?\{([^{}]*)\}", r" \1 ", value)
    value = re.sub(r"\\[A-Za-z@]+\*?(?:\[[^\]]*\])?", " ", value)
    value = re.sub(r"\$[^$]*\$", " ", value)
    value = value.replace("~", " ").replace("---", " ").replace("--", " ")
    value = re.sub(r"[{}&_^]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def prose_metrics(text: str) -> dict[str, float | int]:
    plain = tex_to_plain_text(text)
    words = re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", plain)
    sentences = [item.strip() for item in re.split(r"(?<=[.!?])\s+", plain) if item.strip()]
    sentence_lengths = [
        len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", sentence))
        for sentence in sentences
    ]
    long_sentences = sum(length >= 40 for length in sentence_lengths)
    return {
        "words": len(words),
        "sentences": len(sentences),
        "average_words_per_sentence": round(
            sum(sentence_lengths) / max(1, len(sentence_lengths)), 2
        ),
        "long_sentences_ge_40": long_sentences,
        "long_sentence_rate": round(long_sentences / max(1, len(sentence_lengths)), 4),
        "paragraphs": len([part for part in re.split(r"\n\s*\n", strip_comments(text)) if part.strip()]),
    }


def citation_keys(text: str) -> set[str]:
    keys: set[str] = set()
    for group in re.findall(r"\\cite[A-Za-z*]*\{([^{}]+)\}", text):
        keys.update(item.strip() for item in group.split(",") if item.strip())
    return keys


def numeric_tokens(text: str) -> set[str]:
    return set(re.findall(r"(?<![A-Za-z])[-+]?\d+(?:[.,]\d+)*(?:\\?%|/\d+)?", strip_comments(text)))


def _resolve_graphic(tex_dir: Path, value: str) -> Path | None:
    candidate = tex_dir / value
    if candidate.suffix:
        return candidate if candidate.is_file() else None
    for extension in GRAPHIC_EXTENSIONS:
        resolved = candidate.with_suffix(extension)
        if resolved.is_file():
            return resolved
    return None


def _bib_files(tex_dir: Path, text: str) -> list[Path]:
    names: list[str] = []
    for group in re.findall(r"\\bibliography\{([^{}]+)\}", text):
        names.extend(item.strip() for item in group.split(",") if item.strip())
    names.extend(re.findall(r"\\addbibresource(?:\[[^\]]*\])?\{([^{}]+)\}", text))
    paths: list[Path] = []
    for name in names:
        path = tex_dir / name
        if path.suffix.lower() != ".bib":
            path = path.with_suffix(".bib")
        paths.append(path)
    if not paths:
        paths = sorted(tex_dir.glob("*.bib"))
    return paths


def _load_git_baseline(tex_path: Path, baseline_ref: str) -> tuple[str | None, str | None]:
    repo = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=tex_path.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if repo.returncode != 0:
        return None, "not inside a Git worktree"
    repo_root = Path(repo.stdout.strip()).resolve()
    try:
        relative = tex_path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return None, "manuscript is outside the Git worktree"
    shown = subprocess.run(
        ["git", "show", f"{baseline_ref}:{relative}"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if shown.returncode != 0:
        return None, shown.stderr.strip() or "git show failed"
    return shown.stdout, None


def _revision_comparison(current: str, baseline: str) -> dict[str, object]:
    current_metrics = prose_metrics(current)
    baseline_metrics = prose_metrics(baseline)
    current_cites = citation_keys(current)
    baseline_cites = citation_keys(baseline)
    current_numbers = numeric_tokens(current)
    baseline_numbers = numeric_tokens(baseline)
    current_long = float(current_metrics["long_sentence_rate"])
    baseline_long = float(baseline_metrics["long_sentence_rate"])
    current_average = float(current_metrics["average_words_per_sentence"])
    baseline_average = float(baseline_metrics["average_words_per_sentence"])
    regression_flags: list[str] = []
    if current_average > 35 and current_average > baseline_average * 1.2:
        regression_flags.append("average sentence length increased by more than 20% and exceeds 35 words")
    if current_long > baseline_long + 0.10:
        regression_flags.append("rate of sentences with at least 40 words increased by more than 10 percentage points")
    if int(current_metrics["words"]) < int(baseline_metrics["words"]) * 0.65:
        regression_flags.append("manuscript word count fell by more than 35%; verify that evidence was not dropped")
    return {
        "baseline": baseline_metrics,
        "current": current_metrics,
        "removed_citation_keys": sorted(baseline_cites - current_cites),
        "added_citation_keys": sorted(current_cites - baseline_cites),
        "removed_numeric_tokens": sorted(baseline_numbers - current_numbers),
        "added_numeric_tokens": sorted(current_numbers - baseline_numbers),
        "writing_regression_flags": regression_flags,
    }


def _find_qa_file(project: Path, pattern: str) -> list[Path]:
    qa_root = project / "02_Revision_and_QA"
    return sorted(qa_root.rglob(pattern)) if qa_root.is_dir() else []


def _relative(project: Path, path: Path) -> str:
    try:
        return path.relative_to(project).as_posix()
    except ValueError:
        return str(path)


def audit_project(
    project_root: Path,
    *,
    tex_relative: Path = DEFAULT_TEX,
    baseline_ref: str | None = None,
    run_project_verifier: bool = False,
) -> dict[str, object]:
    project = project_root.resolve()
    tex_path = project / tex_relative
    checks: list[Check] = []
    metrics: dict[str, object] = {}

    if not tex_path.is_file():
        checks.append(_check("manuscript.source", "FAIL", "error", "Active LaTeX source is missing", [str(tex_path)]))
        return _finish(project, tex_path, checks, metrics)

    raw = tex_path.read_text(encoding="utf-8", errors="replace")
    text = strip_comments(raw)
    tex_dir = tex_path.parent
    metrics["manuscript_sha256"] = hashlib.sha256(tex_path.read_bytes()).hexdigest().upper()
    metrics["prose"] = prose_metrics(text)

    class_match = re.search(r"\\documentclass\[([^\]]*)\]\{([^{}]+)\}", text)
    class_ok = bool(
        class_match
        and "applsci" in {item.strip() for item in class_match.group(1).split(",")}
        and class_match.group(2).replace("\\", "/").endswith("Definitions/mdpi")
    )
    checks.append(
        _check(
            "template.documentclass",
            "PASS" if class_ok else "FAIL",
            "error",
            "Applied Sciences MDPI document class is selected" if class_ok else "Expected an applsci MDPI document class",
            [class_match.group(0) if class_match else "documentclass not found"],
        )
    )
    class_file = tex_dir / "Definitions/mdpi.cls"
    if class_file.is_file():
        class_head = "\n".join(class_file.read_text(encoding="utf-8", errors="replace").splitlines()[:35])
        version = re.search(r"\\ProvidesClass\{[^{}]+\}\[([^\]]+)\]", class_head)
        checks.append(_check("template.class_files", "PASS", "error", "MDPI class file is present", [version.group(1) if version else _relative(project, class_file)]))
    else:
        checks.append(_check("template.class_files", "FAIL", "error", "Definitions/mdpi.cls is missing"))

    missing_front = [macro for macro in REQUIRED_FRONT_MACROS if extract_macro_argument(text, macro) is None]
    missing_back = [macro for macro in REQUIRED_BACK_MACROS if extract_macro_argument(text, macro) is None]
    checks.append(_check("structure.front_matter", "PASS" if not missing_front else "FAIL", "error", "Required front matter is present" if not missing_front else "Required front-matter macros are missing", missing_front))
    checks.append(_check("structure.back_matter", "PASS" if not missing_back else "FAIL", "error", "Required back matter is present" if not missing_back else "Required back-matter macros are missing", missing_back))

    section_names = re.findall(r"\\section\*?\{([^{}]+)\}", text)
    normalized_sections = {re.sub(r"[^a-z]", "", name.lower()) for name in section_names}
    required_section_groups = {
        "Introduction": ("introduction",),
        "Materials and Methods / Methods": ("materialsandmethods", "methods", "method"),
        "Results": ("results", "resultsanddiscussion"),
        "Discussion": ("discussion", "resultsanddiscussion"),
        "Conclusions": ("conclusions", "conclusion"),
    }
    missing_sections = [
        label
        for label, alternatives in required_section_groups.items()
        if not any(item in normalized_sections for item in alternatives)
    ]
    checks.append(_check("structure.imrad", "PASS" if not missing_sections else "FAIL", "error", "Applied Sciences research-article sections are present" if not missing_sections else "Expected research-article sections are missing", missing_sections))

    abstract = extract_macro_argument(text, "abstract") or ""
    abstract_words = int(prose_metrics(abstract)["words"])
    metrics["abstract_words"] = abstract_words
    checks.append(_check("abstract.length", "PASS" if 1 <= abstract_words <= 200 else "FAIL", "error", f"Abstract has {abstract_words} words; target is at most about 200"))
    keywords = [item.strip() for item in (extract_macro_argument(text, "keyword") or "").split(";") if item.strip()]
    metrics["keyword_count"] = len(keywords)
    checks.append(_check("keywords.count", "PASS" if 3 <= len(keywords) <= 10 else "FAIL", "error", f"Keyword count is {len(keywords)}; expected 3--10", keywords))

    placeholders: list[str] = []
    for label, pattern in PLACEHOLDER_PATTERNS.items():
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            placeholders.append(f"{label} at line {line}: {match.group(0)}")
    checks.append(_check("metadata.placeholders", "PASS" if not placeholders else "FAIL", "error", "No active placeholders were found" if not placeholders else "Active placeholders remain in the manuscript", placeholders[:30]))

    data_statement = extract_macro_argument(text, "dataavailability") or ""
    immutable_anchor = bool(re.search(r"(?:/tree/[^\s{}]+|doi\.org/|zenodo|figshare|osf\.io)", data_statement, re.IGNORECASE))
    restriction_explained = bool(re.search(r"restrict|licen[cs]|privacy|propriet|not (?:public|redistribut)", data_statement, re.IGNORECASE))
    checks.append(_check("data.availability_anchor", "PASS" if immutable_anchor or restriction_explained else "REVIEW", "manual", "Data Availability names an immutable repository anchor or explains restrictions" if immutable_anchor or restriction_explained else "Manually verify that Data Availability identifies a frozen release or explains why sharing is restricted"))

    ai_text = " ".join(filter(None, [extract_macro_argument(text, "acknowledgments"), text]))
    ai_named = bool(re.search(r"OpenAI|Codex|ChatGPT|Generative AI|GenAI|large.language.model|\bLLM\b", ai_text, re.IGNORECASE))
    ai_purpose = bool(re.search(r"draft|edit|review|analysis|code|figure|writing|prepar", ai_text, re.IGNORECASE))
    ai_responsibility = bool(re.search(r"responsib|reviewed and edited|reviewed.*output", ai_text, re.IGNORECASE))
    ai_ok = ai_named and ai_purpose and ai_responsibility
    checks.append(_check("disclosure.genai", "PASS" if ai_ok else "REVIEW", "manual", "GenAI disclosure names the tool/interface, purpose, and author responsibility" if ai_ok else "Manually confirm whether GenAI was used and, if so, disclose tool, purpose, review, and author responsibility"))

    bib_files = _bib_files(tex_dir, text)
    missing_bib_files = [str(path) for path in bib_files if not path.is_file()]
    cited = citation_keys(text)
    bib_keys: set[str] = set()
    for path in bib_files:
        if path.is_file():
            bib_keys.update(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", path.read_text(encoding="utf-8", errors="replace"), re.IGNORECASE))
    missing_keys = sorted(cited - bib_keys)
    orphan_keys = sorted(bib_keys - cited)
    checks.append(_check("references.files", "PASS" if not missing_bib_files else "FAIL", "error", "Bibliography files are present" if not missing_bib_files else "Bibliography files are missing", missing_bib_files))
    checks.append(_check("references.citation_join", "PASS" if not missing_keys and not orphan_keys else "FAIL", "error", f"Citation--bibliography join: {len(cited)} cited, {len(bib_keys)} entries", [*(f"missing: {key}" for key in missing_keys), *(f"orphan: {key}" for key in orphan_keys)]))
    metrics["citations"] = {"cited_keys": len(cited), "bib_entries": len(bib_keys)}

    labels = set(re.findall(r"\\label\{([^{}]+)\}", text))
    refs = set(re.findall(r"\\(?:ref|eqref|autoref|pageref)\{([^{}]+)\}", text))
    missing_labels = sorted(refs - labels)
    checks.append(_check("crossrefs.labels", "PASS" if not missing_labels else "FAIL", "error", f"Cross-reference join: {len(refs)} referenced labels", missing_labels))

    graphic_values = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^{}]+)\}", text)
    missing_graphics = [value for value in graphic_values if _resolve_graphic(tex_dir, value) is None]
    checks.append(_check("figures.files", "PASS" if not missing_graphics else "FAIL", "error", f"Figure-path check: {len(graphic_values)} included graphics", missing_graphics))

    pdf_dir = project / "01_Manuscript/PDF"
    pdfs = sorted(pdf_dir.glob("*.pdf")) if pdf_dir.is_dir() else []
    invalid_pdfs = [str(path) for path in pdfs if path.read_bytes()[:5] != b"%PDF-"]
    checks.append(_check("outputs.pdf", "PASS" if pdfs and not invalid_pdfs else "FAIL", "error", f"Found {len(pdfs)} manuscript/supplement PDF file(s)" if pdfs else "No final PDF exists under 01_Manuscript/PDF", invalid_pdfs))
    metrics["pdfs"] = [{"path": _relative(project, path), "bytes": path.stat().st_size} for path in pdfs]

    required_release_paths = (
        Path("03_Reproducibility/Code"),
        Path("03_Reproducibility/Data"),
        Path("03_Reproducibility/Figures"),
        Path("03_Reproducibility/Package_Metadata/DATA_RIGHTS_NOTICE.md"),
        Path("03_Reproducibility/Package_Metadata/RELEASE_MANIFEST.json"),
        Path("03_Reproducibility/Package_Metadata/FILE_SHA256SUMS.txt"),
    )
    missing_release = [path.as_posix() for path in required_release_paths if not (project / path).exists()]
    checks.append(_check("reproducibility.release_layout", "PASS" if not missing_release else "FAIL", "error", "Code, data, figures, rights notice, release manifest, and checksums are present" if not missing_release else "Required release artifacts are missing", missing_release))

    qa_requirements = {
        "integrity audit": "*INTEGRITY_AUDIT*.md",
        "reference audit": "*REFERENCE_EXISTENCE_AUDIT*.md",
        "visual QA": "*VISUAL_QA_REPORT*.md",
        "plan completion audit": "*PLAN_COMPLETION_AUDIT*.md",
        "build validation": "*BUILD_VALIDATION*.md",
        "submission checklist": "*APPLIED_SCIENCES_SUBMISSION_CHECKLIST*.md",
        "cover letter": "*COVER_LETTER*.md",
        "author approval": "*AUTHOR_APPROVAL_FORM*.md",
    }
    missing_qa: list[str] = []
    qa_evidence: list[str] = []
    for label, pattern in qa_requirements.items():
        matches = _find_qa_file(project, pattern)
        if matches:
            qa_evidence.append(f"{label}: {_relative(project, matches[-1])}")
        else:
            missing_qa.append(label)
    checks.append(_check("qa.submission_bundle", "PASS" if not missing_qa else "FAIL", "error", "Submission QA and author-facing documents are present" if not missing_qa else "Submission QA documents are missing", missing_qa or qa_evidence))

    unchecked: list[str] = []
    for checklist in _find_qa_file(project, "*APPLIED_SCIENCES_SUBMISSION_CHECKLIST*.md"):
        for number, line in enumerate(checklist.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if re.match(r"\s*- \[ \]", line):
                unchecked.append(f"{_relative(project, checklist)}:{number}: {line.strip()}")
    checks.append(_check("portal.corresponding_author", "PASS" if not unchecked else "REVIEW", "manual", "No unchecked portal items were found" if not unchecked else f"{len(unchecked)} corresponding-author/SuSy actions remain", unchecked))

    claim_counts = {label: len(pattern.findall(tex_to_plain_text(text))) for label, pattern in CLAIM_TERMS.items()}
    metrics["claim_term_counts"] = claim_counts
    checks.append(_check("claims.evidence_alignment", "REVIEW", "manual", "Claim-bearing terms require a human claim--evidence audit; counts are diagnostic, not a style score", [f"{key}: {value}" for key, value in claim_counts.items() if value]))

    if baseline_ref:
        baseline, baseline_error = _load_git_baseline(tex_path, baseline_ref)
        if baseline is None:
            checks.append(_check("revision.baseline", "FAIL", "error", f"Could not load Git baseline {baseline_ref}", [baseline_error or "unknown error"]))
        else:
            comparison = _revision_comparison(text, baseline)
            metrics["revision_comparison"] = comparison
            flags = list(comparison["writing_regression_flags"])
            checks.append(_check("revision.writing_regression", "PASS" if not flags else "REVIEW", "manual", f"Compared current prose with Git baseline {baseline_ref}", flags))
            changed_numbers = len(comparison["removed_numeric_tokens"]) + len(comparison["added_numeric_tokens"])
            changed_citations = len(comparison["removed_citation_keys"]) + len(comparison["added_citation_keys"])
            checks.append(_check("revision.token_conservation", "PASS" if not changed_numbers and not changed_citations else "REVIEW", "manual", "Numeric and citation tokens are unchanged" if not changed_numbers and not changed_citations else "Numeric or citation tokens changed; reconcile them with evidence and the revision ledger", [f"numeric token changes: {changed_numbers}", f"citation-key changes: {changed_citations}"]))

    if run_project_verifier:
        verifier = project / "03_Reproducibility/Code/run_public_verification.py"
        if not verifier.is_file():
            checks.append(_check("reproducibility.project_verifier", "REVIEW", "warning", "No project verifier was found at the standard path"))
        else:
            with tempfile.TemporaryDirectory(prefix="applsci-preflight-") as temporary:
                report = Path(temporary) / "project_verifier.json"
                completed = subprocess.run(
                    [sys.executable, str(verifier), "--report", str(report)],
                    cwd=project,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    check=False,
                )
                evidence = [completed.stdout.strip(), completed.stderr.strip()]
                evidence = [item for item in evidence if item]
                checks.append(_check("reproducibility.project_verifier", "PASS" if completed.returncode == 0 else "FAIL", "error", f"Project verifier exited with code {completed.returncode}", evidence[-4:]))

    return _finish(project, tex_path, checks, metrics)


def _finish(project: Path, tex_path: Path, checks: list[Check], metrics: dict[str, object]) -> dict[str, object]:
    failures = [item for item in checks if item.status == "FAIL"]
    reviews = [item for item in checks if item.status == "REVIEW"]
    status = "FAIL" if failures else ("PASS_WITH_MANUAL_GATES" if reviews else "PASS")
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "project_root": str(project),
        "manuscript": str(tex_path),
        "status": status,
        "summary": {
            "pass": sum(item.status == "PASS" for item in checks),
            "fail": len(failures),
            "review": len(reviews),
        },
        "checks": [asdict(item) for item in checks],
        "metrics": metrics,
    }


def _print_text(report: dict[str, object]) -> None:
    print(f"Applied Sciences preflight: {report['status']}")
    print(f"Project: {report['project_root']}")
    print(f"Summary: {report['summary']}")
    for item in report["checks"]:
        if item["status"] != "PASS":
            print(f"[{item['status']}] {item['check_id']}: {item['message']}")
            for evidence in item["evidence"]:
                print(f"  - {evidence}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path, help="paper project root with 01_Manuscript/02_Revision_and_QA/03_Reproducibility")
    parser.add_argument("--tex", type=Path, default=DEFAULT_TEX, help="LaTeX source path relative to project root")
    parser.add_argument("--baseline-ref", help="optional Git ref for revision-regression comparison")
    parser.add_argument("--run-project-verifier", action="store_true", help="run 03_Reproducibility/Code/run_public_verification.py")
    parser.add_argument("--output", type=Path, help="write the complete JSON report to this path")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a concise text summary")
    parser.add_argument("--strict", action="store_true", help="return exit code 2 when manual REVIEW gates remain")
    args = parser.parse_args()

    report = audit_project(
        args.project,
        tex_relative=args.tex,
        baseline_ref=args.baseline_ref,
        run_project_verifier=args.run_project_verifier,
    )
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        _print_text(report)
    if report["status"] == "FAIL":
        return 1
    if args.strict and report["status"] == "PASS_WITH_MANUAL_GATES":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
