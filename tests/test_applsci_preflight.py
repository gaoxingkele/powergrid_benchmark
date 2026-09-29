import tempfile
import unittest
from pathlib import Path

from scripts.papers.applsci_preflight import audit_project


TEX = r"""
\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}
\Title{A Sound Applied Study}
\Author{A. Author}
\AuthorNames{A. Author}
\address{An Institute; author@institute.edu}
\corres{Correspondence: author@institute.edu}
\abstract{This study evaluates an applied system. We describe the method, report a reproducible result, and delimit the conclusion.}
\keyword{applied system; engineering; reproducibility}
\begin{document}
\section{Introduction}
Motivation \cite{example2026}.
\section{Materials and Methods}
Method. See Figure~\ref{fig:one}.
\begin{figure}\includegraphics{figures/one.pdf}\caption{One.}\label{fig:one}\end{figure}
\section{Results}
Result.
\section{Discussion}
Boundary.
\section{Conclusions}
Conclusion.
\authorcontributions{The author completed the work.}
\funding{This research received no external funding.}
\institutionalreview{Not applicable.}
\informedconsent{Not applicable.}
\dataavailability{Data are archived at https://doi.org/10.0000/example.}
\acknowledgments{The author used OpenAI Codex for language editing, reviewed the output, and takes full responsibility.}
\conflictsofinterest{The author declares no conflict of interest.}
\bibliography{references}
\end{document}
"""


def make_project(root: Path, tex: str = TEX) -> Path:
    latex = root / "01_Manuscript/LaTeX"
    (latex / "Definitions").mkdir(parents=True)
    (latex / "figures").mkdir()
    (root / "01_Manuscript/PDF").mkdir(parents=True)
    (root / "03_Reproducibility/Code").mkdir(parents=True)
    (root / "03_Reproducibility/Data").mkdir()
    (root / "03_Reproducibility/Figures").mkdir()
    metadata = root / "03_Reproducibility/Package_Metadata"
    metadata.mkdir()
    (root / "02_Revision_and_QA").mkdir()

    (latex / "paper_applsci.tex").write_text(tex, encoding="utf-8")
    (latex / "Definitions/mdpi.cls").write_text(
        r"\ProvidesClass{Definitions/mdpi}[23/06/2026 MDPI paper class]", encoding="utf-8"
    )
    (latex / "figures/one.pdf").write_bytes(b"%PDF-1.4 figure")
    (latex / "references.bib").write_text(
        "@article{example2026, title={Example}, author={Author, A.}, year={2026}}\n",
        encoding="utf-8",
    )
    (root / "01_Manuscript/PDF/paper.pdf").write_bytes(b"%PDF-1.4 paper")
    (metadata / "DATA_RIGHTS_NOTICE.md").write_text("rights\n", encoding="utf-8")
    (metadata / "RELEASE_MANIFEST.json").write_text("{}\n", encoding="utf-8")
    (metadata / "FILE_SHA256SUMS.txt").write_text("hash file\n", encoding="utf-8")
    qa = root / "02_Revision_and_QA"
    for name in (
        "INTEGRITY_AUDIT.md",
        "REFERENCE_EXISTENCE_AUDIT.md",
        "VISUAL_QA_REPORT.md",
        "PLAN_COMPLETION_AUDIT.md",
        "BUILD_VALIDATION.md",
        "APPLIED_SCIENCES_SUBMISSION_CHECKLIST.md",
        "COVER_LETTER.md",
        "AUTHOR_APPROVAL_FORM.md",
    ):
        (qa / name).write_text("- [x] complete\n", encoding="utf-8")
    return root


class AppliedSciencesPreflightTests(unittest.TestCase):
    def test_valid_project_has_no_mechanical_failures(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            report = audit_project(make_project(Path(temporary) / "paper"))
        self.assertEqual(report["summary"]["fail"], 0)
        self.assertEqual(report["status"], "PASS_WITH_MANUAL_GATES")

    def test_placeholder_is_blocking(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = make_project(
                Path(temporary) / "paper",
                TEX.replace("author@institute.edu", "author@example.com"),
            )
            report = audit_project(project)
        failed = {
            item["check_id"]
            for item in report["checks"]
            if item["status"] == "FAIL"
        }
        self.assertIn("metadata.placeholders", failed)
        self.assertEqual(report["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
