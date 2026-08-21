"""Fail-closed structural verifier for an original-title manuscript round."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


PAPERS = {
    "c2ges": {
        "title": "Causal and Counterfactual Graph-Enhanced Extractive Summarization",
        "authors": ["Liu Bijing", "Yang Yong"],
        "repository": "https://github.com/gaoxingkele/c2ges",
        "prohibited": [
            # The former dataset name may appear in an explicit disclosure that
            # its unsupported results were removed.  Reject the old numerical
            # claims, not an integrity-preserving historical mention.
            "500 GridMaint-CausalSum",
            "Graph F1 score of 68.2",
            "QA Accuracy of 71.5",
            "ROUGE-1}{41.1",
        ],
    },
    "ma_sqlgrid": {
        "title": "MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases",
        "authors": ["Liu Bijing", "Sun Chenglong", "Yang Yong"],
        "repository": "https://github.com/gaoxingkele/ma-sqlgrid",
        "prohibited": [
            "88.2\\%",
            "93.5\\%",
            "91.7\\%",
            "1000 question--SQL",
            "1000 question-SQL",
        ],
    },
}


def check(path: Path, paper: str) -> dict:
    text = path.read_text(encoding="utf-8")
    contract = PAPERS[paper]
    checks: list[dict] = []

    def require(name: str, passed: bool, detail: str) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    require("original_title", contract["title"] in text, contract["title"])
    for author in contract["authors"]:
        require(f"author_{author.replace(' ', '_')}", author in text, author)
    require("corresponding_author", "Correspondence: Yang Yong" in text, "Yang Yong")
    require(
        "manual_email_boundary",
        "email address to be provided before submission" in text,
        "correspondence email remains a manual author field",
    )
    require("funding_number", "521300250006" in text, "grant number")
    require(
        "all_authors_confirmation",
        "All authors have read and agreed to the published version of the manuscript." in text,
        "MDPI confirmation sentence",
    )
    require("repository", contract["repository"] in text, contract["repository"])
    require("data_availability", "\\dataavailability{" in text, "MDPI data availability macro")
    require("author_contributions", "\\authorcontributions{" in text, "CRediT statement")
    require("conflicts", "\\conflictsofinterest{" in text, "conflict statement")
    require("irb", "\\institutionalreview{" in text, "IRB statement")
    require("informed_consent", "\\informedconsent{" in text, "consent statement")
    for token in contract["prohibited"]:
        require(f"prohibited_absent_{token}", token not in text, token)

    failures = [item for item in checks if not item["passed"]]
    return {
        "schema_version": "original-title-round-verifier-v1",
        "paper": paper,
        "manuscript": str(path.resolve()),
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failure_count": len(failures),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("paper", choices=sorted(PAPERS))
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = check(args.manuscript, args.paper)
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.out:
        args.out.write_text(rendered, encoding="utf-8")
    print(rendered)
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
