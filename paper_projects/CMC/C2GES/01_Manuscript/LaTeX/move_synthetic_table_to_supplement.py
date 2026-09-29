"""Move the small non-confirmatory synthetic table to Supplementary Table S20.

Frees the [H] float that was being pushed to the next page and cascading the
reference block onto an extra page; the table stays in the delivered supplement.
"""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

PARAGRAPH_OLD = (
    "References are extractive reconstructions "
    "of the planted role chain, so this layer tests software and endpoint alignment rather than "
    "unseen real-report validity; in neither set does a Holm-adjusted path contrast differ from zero "
    "(Table~\\ref{tab:synthetic-stress}, Supplementary Table~S20)."
)
PARAGRAPH_NEW = (
    "References are extractive reconstructions "
    "of the planted role chain, so this layer tests software and endpoint alignment rather than "
    "unseen real-report validity; in neither set does a Holm-adjusted path contrast differ from zero "
    "(Supplementary Table~S20)."
)

TABLE_OLD = (
    "\\begin{table}[H]\n"
    "\\caption{Synthetic-stress mean ROUGE-L F1 on the $n=8$ parent fictional reports ($4$ series) at matched word budgets; the held-out set ($n=8$) is reported in the text. References are extractive reconstructions of the planted role chain. This table is not confirmatory and is not real incident data.}\n"
    "\\label{tab:synthetic-stress}\\centering\\small\n"
    "\\begin{tabular}{lrr}\n"
    "\\toprule\n"
    "Method & 110 words & 260 words\\\\\n"
    "\\midrule\n"
    "Full \\cges{} & 0.1303 & 0.1184\\\\\n"
    "No-path \\cges{} & 0.1199 & 0.1086\\\\\n"
    "G-T (typed, no path) & 0.1199 & 0.1086\\\\\n"
    "G-U (untyped, no path) & 0.0887 & 0.0981\\\\\n"
    "\\bottomrule\n"
    "\\end{tabular}\n"
    "\\end{table}\n"
)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for label, old, new in (
        ("synthetic paragraph pointer", PARAGRAPH_OLD, PARAGRAPH_NEW),
        ("synthetic table", TABLE_OLD, ""),
    ):
        count = text.count(old)
        if count != 1:
            raise AssertionError(f"{label}: anchor occurs {count} times")
        text = text.replace(old, new)
    TEX.write_text(text, encoding="utf-8")
    print("synthetic table moved to the supplement")


if __name__ == "__main__":
    main()
