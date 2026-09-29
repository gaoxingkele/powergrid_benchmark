"""Gating checks for the Information presentation revision (Priority A/B/C).

Reads the shipped tex, bib, cover letter, and supplementary source.
Does not re-implement scoring; it asserts the manuscript artifacts that
the revision plan required.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEX = HERE / "paper_information.tex"
BIB = HERE / "references_cited_verified.bib"
COVER = HERE / "INFORMATION_COVER_LETTER.md"
SUPP = HERE.parent / "Supplementary" / "supplementary_materials.tex"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def abstract_words(tex: str) -> int:
    i = tex.find(r"\abstract{")
    i = tex.find("{", i)
    depth = 0
    for j, ch in enumerate(tex[i:], i):
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                abs_tex = tex[i + 1 : j]
                break
    text = abs_tex.replace(r"\cges{}", "C2GES").replace("--", "-")
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = re.sub(r"[{}]", "", text)
    return len(re.findall(r"[A-Za-z0-9][A-Za-z0-9.'/%-]*", text))


def main() -> int:
    tex = _read(TEX)
    bib = _read(BIB)
    cover = _read(COVER)
    supp = _read(SUPP)
    failures: list[str] = []

    if r"\label{tab:evidence-layers}" not in tex:
        failures.append("missing tab:evidence-layers")
    for needle in (
        "Historical 15-test equal-unit",
        "Seven-series 110/260 post-access",
        "RSI 15-test 110/260 held-out",
        "Synthetic v8",
    ):
        if needle not in tex:
            failures.append(f"missing layer row: {needle}")
    if "Not unseen confirmatory evaluation" not in tex:
        failures.append("evidence table missing unseen confirmatory bound")
    if "not expert gold" not in tex.lower() and "Not expert gold" not in tex and "not expert gold" not in tex:
        if "not expert gold" not in tex:
            failures.append("evidence table missing expert-gold bound")

    for num in ("0.1060", "0.1276", "0.1094", "0.1310", "-0.00799", "-0.00718"):
        if num not in tex:
            failures.append(f"missing conserved number {num}")

    abs_txt = tex[tex.find(r"\abstract{") : tex.find(r"\keyword{")]
    if "primary path-component evidence" not in abs_txt:
        failures.append("abstract does not name primary path-component evidence")
    if "normalized Full versus no-path" not in abs_txt and "normalized Full versus no-path" not in tex:
        failures.append("normalized Full versus no-path not named")
    conc = tex[tex.find(r"\section{Conclusions}") :]
    if "primary path-component evidence" not in conc:
        failures.append("conclusions do not name primary path-component evidence")
    if "scale-coupled historical diagnostic" not in tex:
        failures.append("unrenorm not labeled scale-coupled historical diagnostic")

    nwords = abstract_words(tex)
    if nwords > 200:
        failures.append(f"abstract word count {nwords} > 200")

    for name in ("GraphLSS", "StrucSum", "STAS", "Bi-GAE"):
        if name not in tex:
            failures.append(f"Related Work missing {name}")
    if "does not train edge labels" not in tex:
        failures.append("GraphLSS difference clause missing")
    if "Neither method was scored on the retained 15-report" not in tex:
        failures.append("STAS/Bi-GAE not-baseline wording missing")
    if re.search(r"ECT-BPS", tex) or re.search(r"ECT-BPS", bib):
        failures.append("ECT-BPS must not be cited")
    if "xu2020stas" not in tex or "mao2023bigae" not in tex:
        failures.append("STAS/Bi-GAE cite keys missing from tex")
    if "10.18653/v1/2020.findings-emnlp.161" not in bib:
        failures.append("STAS DOI missing from bib")
    if "10.18653/v1/2023.findings-emnlp.328" not in bib:
        failures.append("Bi-GAE DOI missing from bib")

    for phrase in (
        "20--30-case expert evaluation",
        "not scored on the retained 15-test",
        "12-position edge window",
        "Rhetorical Structure Theory",
        "BERTScore",
    ):
        if phrase not in tex:
            failures.append(f"Priority C disposition missing: {phrase}")
    if "institutional ethics determination" not in tex:
        failures.append("E2 ethics determination missing")
    if "IRB approved" in tex or "expert annotators completed" in tex:
        failures.append("must not claim completed human/IRB work")

    if "normalized path term did not show a stable gain" not in cover:
        failures.append("cover letter missing normalized-path diagnosis")
    if "not an equal-unit ROUGE win" not in cover:
        failures.append("cover letter missing equal-unit-win denial")
    if "evidence-layer table" not in supp and "Evidence layers and claim bounds" not in supp:
        failures.append("supplementary missing evidence-layer pointer")

    print(f"abstract_words={nwords}")
    if failures:
        print("FAIL")
        for item in failures:
            print(" -", item)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
