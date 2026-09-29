"""Upgrade the L5 synthetic-stress layer to the frozen parent/held-out fixtures.

Only the synthetic (non-confirmatory) layer changes; every real-corpus number,
the L5 claim boundary, and all other layers stay exactly as they were.
"""

from __future__ import annotations

from pathlib import Path

TEX = Path(__file__).resolve().parent / "paper_information.tex"

L5_ROW_OLD = (
    "L5 Synthetic stress set & 8 fictional reports, 4 series & 110/260 words & Full vs no-path on "
    "planted role-chain references & Software and endpoint alignment on fictional fixtures; no "
    "Holm-adjusted path contrast is nonzero. Not real incident data.\\\\"
)
L5_ROW_NEW = (
    "L5 Synthetic stress set & 16 fictional reports, 8 series (parent and held-out) & 110/260 words "
    "& Full vs no-path on planted role-chain references & Software and endpoint alignment on "
    "fictional fixtures; no Holm-adjusted path contrast is nonzero in either the parent or the "
    "held-out set. Not real incident data.\\\\"
)

PARAGRAPH_OLD = (
    "The single four-series stress set of earlier iterations was replaced by a stricter "
    "parent--held-out pair generated under a frozen protocol: sixteen reports in eight series (four "
    "unused themes per set), written by two generator families whose roles are swapped between the "
    "sets, and accepted only after nineteen deterministic gates (structure, distribution, leakage "
    "and semantic self-consistency). The references are extractive reconstructions of the planted "
    "role chain, so this layer tests software and endpoint alignment rather than unseen real-report "
    "validity. Table~\\ref{tab:synthetic-stress} reports the means. In the parent set Full \\cges{} "
    "exceeded no-path at both budgets (0.1303 versus 0.1199 at 110 words; 0.1184 versus 0.1086 at "
    "260 words), with series-equal Full-minus-no-path means of $+0.0103$ and $+0.0098$ and "
    "Holm-adjusted values of 1.0; in the held-out set the contrast was $-0.0007$ and $+0.0032$ "
    "(Holm 1.0). Typed-minus-untyped graph means remained positive in both sets, with "
    "Holm-adjusted exact values of 0.25."
)
PARAGRAPH_NEW = (
    "The single four-series stress set of earlier iterations was replaced by a stricter "
    "parent--held-out pair under a frozen protocol: sixteen reports in eight series (four unused "
    "themes per set), written by two generator families with their roles swapped between the sets, "
    "and accepted only after nineteen deterministic gates. References are extractive reconstructions "
    "of the planted role chain, so this layer tests software and endpoint alignment rather than "
    "unseen real-report validity; in neither set does a Holm-adjusted path contrast differ from zero "
    "(Table~\\ref{tab:synthetic-stress}, Supplementary Table~S20)."
)

TABLE_VARIANTS = [
    (
        "\\caption{Synthetic-stress mean ROUGE-L F1 on $n=8$ fictional reports ($4$ series) at matched word budgets. References are extractive reconstructions of the planted role chain. This table is not confirmatory and is not real incident data.}\n"
        "\\label{tab:synthetic-stress}\\centering\\small\n"
        "\\begin{tabular}{lrr}\n"
        "\\toprule\n"
        "Method & 110 words & 260 words\\\\\n"
        "\\midrule\n"
        "Full \\cges{} & 0.3886 & 0.3481\\\\\n"
        "No-path \\cges{} & 0.3750 & 0.3269\\\\\n"
        "G-T (typed, no path) & 0.3750 & 0.3269\\\\\n"
        "G-U (untyped, no path) & 0.3002 & 0.2346\\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}"
    ),
    (
        "\\caption{Synthetic-stress mean ROUGE-L F1 on $n=16$ fictional reports ($8$ series: parent and held-out) at matched word budgets. References are extractive reconstructions of the planted role chain. This table is not confirmatory and is not real incident data.}\n"
        "\\label{tab:synthetic-stress}\\centering\\small\n"
        "\\begin{tabular}{lrrrr}\n"
        "\\toprule\n"
        "& \\multicolumn{2}{c}{Parent set} & \\multicolumn{2}{c}{Held-out set}\\\\\n"
        "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\n"
        "Method & 110 words & 260 words & 110 words & 260 words\\\\\n"
        "\\midrule\n"
        "Full \\cges{} & 0.1303 & 0.1184 & 0.1168 & 0.1082\\\\\n"
        "No-path \\cges{} & 0.1199 & 0.1086 & 0.1171 & 0.1039\\\\\n"
        "G-T (typed, no path) & 0.1199 & 0.1086 & 0.1171 & 0.1039\\\\\n"
        "G-U (untyped, no path) & 0.0887 & 0.0981 & 0.0826 & 0.0910\\\\\n"
        "\\bottomrule\n"
        "\\end{tabular}\n"
        "\\end{table}"
    ),
]
TABLE_FINAL = (
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
    "\\end{table}"
)

SUPP_DECL_OLD = "\\supplementary{The supplementary PDF contains Tables~S1--S19 and Figures~S4--S5."
SUPP_DECL_NEW = "\\supplementary{The supplementary PDF contains Tables~S1--S20 and Figures~S4--S5."


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise AssertionError(f"{label}: anchor occurs {count} times")
    return text.replace(old, new)


def main() -> None:
    text = TEX.read_text(encoding="utf-8")
    for label, old, new in (
        ("L5 evidence row", L5_ROW_OLD, L5_ROW_NEW),
        ("synthetic paragraph", PARAGRAPH_OLD, PARAGRAPH_NEW),
        ("supplementary declaration", SUPP_DECL_OLD, SUPP_DECL_NEW),
    ):
        if new in text and old not in text:
            continue
        text = replace_once(text, old, new, label)
    if TABLE_FINAL not in text:
        for variant in TABLE_VARIANTS:
            if variant in text:
                text = replace_once(text, variant, TABLE_FINAL, "synthetic table")
                break
        else:
            raise AssertionError("synthetic table anchor not found")
    TEX.write_text(text, encoding="utf-8")
    print("L5 upgraded to the parent/held-out fixtures")


if __name__ == "__main__":
    main()
