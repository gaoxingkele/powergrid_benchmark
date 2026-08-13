"""Build reproducible journal-class LaTeX previews for the six Mintou papers.

The Markdown files remain the content masters.  This script performs only a
deterministic format conversion: numbered headings are normalized for the
journal classes, figures/tables are emitted as full-width floats, and the
numbered reference list is preserved as a LaTeX bibliography.  It never edits
the manuscript, figures, or evidence files.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "paper_projects"
MDPI_TEMPLATE = PAPERS / "target_journal_templates" / "mdpi-acs" / "official" / "extracted"
IEEE_TEMPLATE = PAPERS / "target_journal_templates" / "ieee-access" / "official" / "extracted" / "ACCESS_latex_template_20260513"
PANDOC = ROOT / ".tools" / "pandoc-3.6.4" / "pandoc.exe"


def resolve_pandoc() -> Path:
    """Resolve a verified local Pandoc without copying the large binary into every worktree."""
    candidates = [
        Path(os.environ["PAPER_HARNESS_PANDOC"]) if os.environ.get("PAPER_HARNESS_PANDOC") else None,
        PANDOC,
        Path(r"D:/aicoding/powergrid_benchmark/.tools/pandoc-3.6.4/pandoc.exe"),
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    discovered = shutil.which("pandoc")
    if discovered:
        return Path(discovered)
    raise FileNotFoundError("pandoc not found; set PAPER_HARNESS_PANDOC to a verified executable")


@dataclass(frozen=True)
class Spec:
    slug: str
    venue: str
    journal_option: str | None


SPECS = [
    Spec("mintou_p1_dstar_gru_dispatch", "IEEE Access", None),
    Spec("mintou_p2_hygraph_load_forecasting", "Electronics", "electronics"),
    Spec("mintou_p3_samode_distribution_planning", "Energies", "energies"),
    Spec("mintou_p4_shield_resilience_planning", "Energies", "energies"),
    Spec("mintou_p5_trace_moea_feasibility_review", "Energies", "energies"),
    Spec("mintou_p6_bilonsga_project_review", "Applied Sciences", "applsci"),
]


BACK_MATTER = {
    "Author Contributions",
    "Funding",
    "Institutional Review Board Statement",
    "Informed Consent Statement",
    "Data Availability Statement",
    "Acknowledgments",
    "Conflicts of Interest",
    "Generative AI Statement",
    "Declaration of Generative AI and AI-Assisted Technologies in the Writing Process",
    "Author Biographies",
}


def latex_escape_plain(value: str) -> str:
    value = html.unescape(value)
    value = value.replace("\\", r"\textbackslash{}")
    for old, new in [("&", r"\&"), ("%", r"\%"), ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}")]:
        value = value.replace(old, new)
    value = value.replace("~", r"\textasciitilde{}").replace("^", r"\textasciicircum{}")
    return value


def inline_tex(value: str) -> str:
    """Convert the small Markdown subset used inside tables/references."""
    protected: list[str] = []

    def hold(text: str) -> str:
        protected.append(text)
        return f"@@PROTECTED{len(protected)-1}@@"

    value = re.sub(r"\$[^$]+\$", lambda m: hold(m.group(0)), value)
    value = re.sub(r"https?://[^\s)]+", lambda m: hold(r"\url{" + m.group(0).rstrip(".,;") + "}" + m.group(0)[len(m.group(0).rstrip(".,;")):]), value)
    value = re.sub(r"`([^`]+)`", lambda m: hold(r"\texttt{" + latex_escape_plain(m.group(1)) + "}"), value)
    value = latex_escape_plain(value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\\textbf{\1}", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"\\emph{\1}", value)
    value = value.replace("---", "---").replace("–", "--").replace("—", "---")
    value = value.replace("−", "-").replace("×", r"$\times$").replace("≤", r"$\leq$").replace("≥", r"$\geq$")
    for i, item in enumerate(protected):
        value = value.replace(latex_escape_plain(f"@@PROTECTED{i}@@"), item)
    return value


def extract_field(text: str, label: str, default: str) -> str:
    match = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*(.+)$", text, flags=re.M)
    return match.group(1).strip() if match else default


def clean_authors(raw: str) -> str:
    if "AUTHOR INPUT REQUIRED" in raw:
        return "Author Details Required before Submission"
    raw = re.sub(r"\s*\([^)]*[\u3400-\u9fff][^)]*\)", "", raw)
    return raw


def parse_master(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    title_match = re.search(r"^#\s+(.+)$", text, flags=re.M)
    if not title_match:
        raise ValueError(f"No title in {path}")
    title = title_match.group(1).strip()
    abstract_match = re.search(r"^##\s+Abstract\s*$\n(.*?)(?=^\*\*(?:Keywords|Index Terms):?\*\*)", text, flags=re.M | re.S)
    if not abstract_match:
        raise ValueError(f"No abstract in {path}")
    abstract = abstract_match.group(1).strip()
    kw_match = re.search(r"^\*\*(?:Keywords|Index Terms):?\*\*\s*(?:—|:)?\s*(.+)$", text, flags=re.M)
    if not kw_match:
        raise ValueError(f"No keywords in {path}")
    keywords = kw_match.group(1).strip()
    body = text[kw_match.end():]
    body = re.sub(r"^\s*---\s*", "", body)
    return {
        "title": title,
        "authors": clean_authors(extract_field(text, "Authors", "Author Details Required before Submission")),
        "affiliations": extract_field(text, "Affiliations", "Affiliation details required before submission"),
        "correspondence": extract_field(text, "Corresponding author", extract_field(text, "Correspondence", "Corresponding-author details required before submission")),
        "abstract": abstract,
        "keywords": keywords,
        "body": body.strip(),
    }


def strip_heading_number(value: str) -> str:
    value = re.sub(r"^(?:[IVX]+|\d+)(?:\.\d+){0,2}\.\s+", "", value)
    value = re.sub(r"^[A-Z]\.\s+", "", value)
    return value


def table_block(caption: str, header: list[str], rows: list[list[str]], label: str) -> str:
    n = len(header)
    size = r"\scriptsize" if n >= 6 or len(rows) > 10 else r"\footnotesize"
    spec = " ".join([r">{\raggedright\arraybackslash}X"] * n)
    lines = [
        r"\begin{table*}[t]",
        r"\centering",
        size,
        r"\setlength{\tabcolsep}{3pt}",
        rf"\caption{{{inline_tex(caption)}}}\label{{{label}}}",
        rf"\begin{{tabularx}}{{\textwidth}}{{@{{}}{spec}@{{}}}}",
        r"\toprule",
        " & ".join(inline_tex(cell) for cell in header) + r" \\",
        r"\midrule",
    ]
    for row in rows:
        row = row + [""] * (n - len(row))
        lines.append(" & ".join(inline_tex(cell) for cell in row[:n]) + r" \\")
    lines.extend([r"\bottomrule", r"\end{tabularx}", r"\end{table*}"])
    return "\n".join(lines)


def figure_block(path: str, caption: str, label: str) -> str:
    path = path.removeprefix("./")
    return "\n".join(
        [
            r"\begin{figure*}[t]",
            r"\centering",
            rf"\includegraphics[width=0.94\textwidth]{{{path}}}",
            rf"\caption{{{inline_tex(caption)}}}\label{{{label}}}",
            r"\end{figure*}",
        ]
    )


def read_markdown_table(lines: list[str], start: int) -> tuple[list[str], list[list[str]], int] | None:
    if start + 1 >= len(lines) or not lines[start].strip().startswith("|"):
        return None
    if not re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[start + 1]):
        return None
    header = [c.strip() for c in lines[start].strip().strip("|").split("|")]
    rows: list[list[str]] = []
    cursor = start + 2
    while cursor < len(lines) and lines[cursor].strip().startswith("|"):
        rows.append([c.strip() for c in lines[cursor].strip().strip("|").split("|")])
        cursor += 1
    return header, rows, cursor


def preprocess_body(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0
    fig_count = 0
    table_count = 0
    while i < len(lines):
        line = lines[i]
        heading = re.match(r"^(#{2,4})\s+(.+)$", line)
        if heading:
            name = strip_heading_number(heading.group(2).strip())
            if name == "References":
                j = i + 1
                while j < len(lines) and not re.match(r"^##\s+", lines[j]):
                    j += 1
                refs = "\n".join(lines[i + 1 : j]).strip()
                refs = re.sub(r"\n---\s*$", "", refs).strip()
                starts = list(re.finditer(r"(?m)^\s*(?:\[(\d+)\]|(\d+)\.)\s+", refs))
                out.append(r"\begin{thebibliography}{99}")
                for pos, match in enumerate(starts):
                    number = match.group(1) or match.group(2)
                    end = starts[pos + 1].start() if pos + 1 < len(starts) else len(refs)
                    entry = refs[match.end() : end]
                    out.append(rf"\bibitem{{ref{number}}} {inline_tex(' '.join(entry.split()))}")
                out.append(r"\end{thebibliography}")
                i = j
                continue
            # MANUSCRIPT.md reserves level one for the paper title, so its
            # numbered research sections start at level two.  The title is
            # removed before this fragment is passed to Pandoc; shift the
            # remaining headings up one level so journals receive \section,
            # \subsection, ... instead of starting at \subsection (which
            # renders as "0.1" in MDPI classes and "A." in IEEE Access).
            hashes = "#" * max(1, len(heading.group(1)) - 1)
            if name in BACK_MATTER:
                out.append(rf"\section*{{{inline_tex(name)}}}")
            else:
                out.append(f"{hashes} {name}")
            i += 1
            continue

        image_match = re.match(r"^!\[(.*)\]\(([^)]+)\)\s*$", line)
        if image_match:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            caption = image_match.group(1)
            if j < len(lines):
                cap_match = re.match(r"^\*\*Fig(?:ure)?\.?\s+\d+\.\*\*\s*(.+)$", lines[j])
                if cap_match:
                    caption = cap_match.group(1).strip()
                    i = j
            fig_count += 1
            out.append(figure_block(image_match.group(2), caption, f"fig:{fig_count}"))
            i += 1
            continue

        table_caption = re.match(r"^\*\*Table\s+\d+\.\*\*\s*(.+)$", line)
        if table_caption:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            converted: list[str] = []
            cursor = j
            while cursor < len(lines):
                subtitle = ""
                subtitle_match = re.match(r"^\*([^*]+)\*\s*$", lines[cursor].strip())
                if subtitle_match:
                    subtitle = subtitle_match.group(1).strip()
                    cursor += 1
                    while cursor < len(lines) and not lines[cursor].strip():
                        cursor += 1
                parsed = read_markdown_table(lines, cursor)
                if not parsed:
                    break
                header, rows, cursor = parsed
                table_count += 1
                caption = table_caption.group(1).strip() + (f" {subtitle}" if subtitle else "")
                converted.append(table_block(caption, header, rows, f"tab:{table_count}"))
                while cursor < len(lines) and not lines[cursor].strip():
                    cursor += 1
                if not (cursor < len(lines) and re.match(r"^\*([^*]+)\*\s*$", lines[cursor].strip())):
                    break
            if converted:
                out.extend(converted)
                i = cursor
                continue

        out.append(line)
        i += 1
    return "\n".join(out)


def pandoc_fragment(markdown: str, cwd: Path) -> str:
    temp = cwd / "body.generated.md"
    out = cwd / "body.generated.tex"
    temp.write_text(markdown, encoding="utf-8")
    subprocess.run(
        [str(resolve_pandoc()), str(temp), "--from", "markdown+tex_math_dollars+tex_math_single_backslash+raw_tex", "--to", "latex", "--wrap=none", "-o", str(out)],
        cwd=cwd,
        check=True,
    )
    return out.read_text(encoding="utf-8")


def abstract_tex(markdown: str, cwd: Path) -> str:
    return pandoc_fragment(markdown, cwd).strip()


def sanitize_tex(value: str) -> str:
    """Replace Unicode glyphs unsupported by the journal pdfLaTeX classes."""
    value = value.replace("10⁻³", r"$10^{-3}$")
    replacements = {
        "≥": r"$\geq$", "≤": r"$\leq$", "×": r"$\times$",
        "α": r"$\alpha$", "λ": r"$\lambda$", "→": r"$\rightarrow$",
        "≈": r"$\approx$", "³": r"$^{3}$", "⁻": r"$^{-}$",
        "±": r"$\pm$", "−": "-",
        "á": r"\'{a}", "ä": r'\"{a}', "Ç": r"\c{C}",
        "é": r"\'{e}", "í": r"\'{\i}", "ı": r"\i{}",
        "ñ": r"\~{n}", "Ö": r'\"{O}', "š": r"\v{s}",
        "ú": r"\'{u}", "ü": r'\"{u}', "ć": r"\'{c}",
        "Ž": r"\v{Z}",
    }
    for old, new in replacements.items():
        value = value.replace(old, new)
    return value


def mdpi_tex(spec: Spec, meta: dict[str, str], body: str, abstract: str) -> str:
    authors = inline_tex(meta["authors"])
    title = inline_tex(meta["title"])
    affiliation = inline_tex(meta["affiliations"])
    correspondence = inline_tex(meta["correspondence"])
    keywords = inline_tex(meta["keywords"])
    return rf"""\documentclass[{spec.journal_option},article,submit,moreauthors]{{Definitions/mdpi}}
\usepackage{{tabularx}}
\usepackage{{array}}
\firstpage{{1}}
\pubvolume{{1}}
\issuenum{{1}}
\articlenumber{{0}}
\pubyear{{2026}}
\copyrightyear{{2026}}
\datereceived{{}}
\daterevised{{}}
\dateaccepted{{}}
\datepublished{{}}
\Title{{{title}}}
\Author{{{authors}}}
\AuthorNames{{{authors}}}
\address{{{affiliation}}}
\corres{{Correspondence: {correspondence}}}
\abstract{{{abstract}}}
\keyword{{{keywords}}}
\providecommand{{\tightlist}}{{\setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
\begin{{document}}
{body}
\end{{document}}
"""


def ieee_tex(meta: dict[str, str], body: str, abstract: str) -> str:
    title = inline_tex(meta["title"])
    authors = inline_tex(meta["authors"])
    affiliation = inline_tex(meta["affiliations"])
    correspondence = inline_tex(meta["correspondence"])
    keywords = inline_tex(meta["keywords"].replace(";", ","))
    return rf"""\documentclass{{ieeeaccess}}
\usepackage{{cite}}
\usepackage{{amsmath,amssymb,amsfonts}}
\usepackage{{graphicx}}
\usepackage{{booktabs,tabularx,array,longtable}}
\usepackage{{url}}
\providecommand{{\tightlist}}{{\setlength{{\itemsep}}{{0pt}}\setlength{{\parskip}}{{0pt}}}}
\begin{{document}}
\history{{Date of publication xxxx 00, 0000, date of current version xxxx 00, 0000.}}
\doi{{10.1109/ACCESS.XXXX.XXXXXXX}}
\title{{{title}}}
\author{{\uppercase{{{authors}}}}}
\address[1]{{{affiliation}}}
\tfootnote{{Funding and sponsor information must be confirmed by the authors before submission.}}
\markboth{{Author et al.: {title}}}{{Author et al.: {title}}}
\corresp{{Corresponding author: {correspondence}.}}
\begin{{abstract}}
{abstract}
\end{{abstract}}
\begin{{keywords}}
{keywords}
\end{{keywords}}
\maketitle
{body}
\EOD
\end{{document}}
"""


def build_one(spec: Spec) -> tuple[Path, Path]:
    manuscript = PAPERS / spec.slug / "manuscript"
    out = manuscript / "journal_submission"
    out.mkdir(parents=True, exist_ok=True)
    if spec.journal_option:
        shutil.copytree(MDPI_TEMPLATE / "Definitions", out / "Definitions", dirs_exist_ok=True)
    else:
        for source in IEEE_TEMPLATE.iterdir():
            if source.is_file() and source.suffix.lower() in {".cls", ".sty", ".fd", ".tfm", ".pfb", ".map", ".png"}:
                shutil.copy2(source, out / source.name)
    shutil.copytree(manuscript / "figures", out / "figures", dirs_exist_ok=True)
    meta = parse_master(manuscript / "MANUSCRIPT.md")
    prepared = preprocess_body(meta["body"])
    body = pandoc_fragment(prepared, out)
    abstract = abstract_tex(meta["abstract"], out)
    tex = mdpi_tex(spec, meta, body, abstract) if spec.journal_option else ieee_tex(meta, body, abstract)
    paper = out / "paper.tex"
    paper.write_text(sanitize_tex(tex), encoding="utf-8")
    engine = "pdflatex"
    for _ in range(2):
        subprocess.run([engine, "-interaction=nonstopmode", "-halt-on-error", "paper.tex"], cwd=out, check=True, stdout=subprocess.DEVNULL)
    return paper, out / "paper.pdf"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build one or all Mintou journal previews deterministically.")
    parser.add_argument(
        "--project",
        choices=[spec.slug for spec in SPECS],
        help="Build only the named paper; omitted means build all six papers.",
    )
    args = parser.parse_args(argv)
    selected = [spec for spec in SPECS if args.project in (None, spec.slug)]
    for spec in selected:
        tex, pdf = build_one(spec)
        print(f"{spec.slug}: {tex.relative_to(ROOT)} -> {pdf.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
