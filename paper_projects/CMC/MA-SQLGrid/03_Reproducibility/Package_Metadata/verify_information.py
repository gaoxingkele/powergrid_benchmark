"""Non-mutating Information technical check; never a submission verdict.

Default output is stdout. An explicit report must be new and outside Workspace.
Historical checks are reused only for data and software, not author readiness.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
import verify_package as historical

ROOT = Path(__file__).resolve().parents[2]
LATEX = ROOT / "01_Manuscript/LaTeX"
TEX = LATEX / "paper_information.tex"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def execute(command, cwd):
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    result = subprocess.run(command, cwd=cwd, env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-10000:])
    return result.stdout + result.stderr


def check_source():
    source = TEX.read_text(encoding="utf-8")
    for token in ("\\Title", "tab:failure-partition", "sec:historical-question-statistics",
                  "post-result", "99", "100", "129", "\\appendixstart"):
        if token not in source:
            raise ValueError("Missing current manuscript marker: " + token)
    if not re.search(r"\\documentclass\[[^]]*information", source):
        raise ValueError("Not an Information manuscript")
    refs = set(re.findall(r"\\(?:ref|eqref|pageref)\{([^}]+)\}", source))
    labels = re.findall(r"\\label\{([^}]+)\}", source)
    if len(labels) != len(set(labels)) or refs - set(labels):
        raise ValueError("Duplicate or unresolved source labels")
    bib_names = [name.strip() for group in re.findall(r"\\bibliography\{([^}]+)\}", source)
                 for name in group.split(",")]
    bib = "\n".join((LATEX / (name + ".bib")).read_text(encoding="utf-8") for name in bib_names)
    keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)", bib))
    cited = {k.strip() for group in re.findall(r"\\cite\w*\{([^}]+)\}", source)
             for k in group.split(",")}
    if cited - keys:
        raise ValueError("Missing bibliography keys")
    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", source)
    for name in figures:
        if not (LATEX / name).is_file():
            raise ValueError("Missing figure: " + name)
    return {"sha256": digest(TEX), "cited_keys": len(cited), "figures": len(figures),
            "tables": len(re.findall(r"\\begin\{table\*?\}", source))}


def check_partition():
    path = ROOT / "03_Reproducibility/Data/selection_failure_decomposition/information_r1/selection_failure_decomposition.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["analysis_status"] != "post_result_exploratory" or len(data["items"]) != 360:
        raise ValueError("Partition identity mismatch")
    for name, correct, tied in (("validation_only", 99, 33), ("complete_witness", 100, 32)):
        categories = data["summaries"][name]["categories"]
        expected = {"no_correct_candidate": 42, "all_correct_candidates_gated_out": 0,
                    "correct_candidates_below_top_score": 6,
                    "correct_top_candidate_lost_by_tie_order": tied, "selected_correct": correct}
        if any(categories.get(k, 0) != v for k, v in expected.items()) or sum(categories.values()) != 180:
            raise ValueError("Partition counts mismatch")
    audit = ROOT / "03_Reproducibility/Code/evaluator_audit"
    log = execute([sys.executable, "-B", "-m", "unittest", "test_selection_failure_decomposition.py", "-v"], audit)
    return {"sha256": digest(path), "items": 360, "test_log": log}


def build():
    engines = {name: shutil.which(name) for name in ("pdflatex", "bibtex")}
    if not all(engines.values()):
        raise RuntimeError("pdflatex and bibtex must be available on PATH")
    with tempfile.TemporaryDirectory(prefix="information_build_") as temp:
        dest = Path(temp) / "LaTeX"
        shutil.copytree(LATEX, dest, ignore=shutil.ignore_patterns(
            "*.aux", "*.bbl", "*.blg", "*.log", "*.out", "paper_*.pdf", "__pycache__"))
        for tool in ("pdflatex", "bibtex", "pdflatex", "pdflatex"):
            args = [engines[tool]]
            if tool == "pdflatex":
                args += ["-interaction=batchmode", "-halt-on-error", "paper_information.tex"]
            else:
                args += ["paper_information"]
            execute(args, dest)
        log = (dest / "paper_information.log").read_text(encoding="utf-8", errors="replace")
        if any(term in log.lower() for term in ("undefined references", "undefined citations", "overfull ")):
            raise ValueError("Build contains unresolved references or overfull boxes")
        pages = re.search(r"Output written on .*?\((\d+) pages?", log)
        return {"status": "PASS", "pages": int(pages[1]) if pages else None,
                "pdf_sha256": digest(dest / "paper_information.pdf"),
                "note": "Temporary clean build; PDF timestamps can change its hash"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-latex", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.report:
        report = args.report.resolve()
        if report.exists() or report.is_relative_to(ROOT):
            parser.error("Report must be new and outside the paper Workspace")
        if not report.parent.is_dir():
            parser.error("Report parent must already exist")
    before = digest(TEX)
    # Prevent imported legacy subprocesses from producing bytecode in the package.
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    result = {"schema": "information-technical-v1", "python": sys.version,
              "manuscript": check_source(), "retained_data": historical.verify_data(),
              "software": historical.run_unit_tests(), "partition": check_partition(),
              "latex": {"status": "SKIPPED"} if args.skip_latex else build(),
              "submission_ready": None, "publication_status": "NOT_ESTABLISHED",
              "scope": "Technical checks only; no new expert, external-validity, citation-truth or author approval verdict"}
    if digest(TEX) != before:
        raise RuntimeError("Source changed during verification")
    result["technical_status"] = "PARTIAL" if args.skip_latex else "PASS"
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        with report.open("x", encoding="utf-8") as handle:
            handle.write(encoded + "\n")
    print(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
