"""Non-submission audit: evidence parity and finite examples of stated properties."""
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TEX = ROOT.parents[1] / "01_Manuscript" / "LaTeX"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tables(text):
    result = {}
    for block in re.findall(r"\\begin\{table\}.*?\\end\{table\}", text, re.S):
        label = re.search(r"\\label\{([^}]+)\}", block).group(1)
        result[label] = block
    return result


def select(scores, eligible, order):
    allowed = [i for i in order if eligible[i]]
    return max(allowed, key=lambda i: scores[i]) if allowed else None


def finite_property_checks():
    # Exhaustive 3-candidate examples; these supplement, not replace, the proofs.
    count = 0
    for scores in itertools.product(range(2), repeat=3):
        for eligible in itertools.product((False, True), repeat=3):
            outputs = {select(scores, eligible, p) for p in itertools.permutations(range(3))}
            allowed = [i for i in range(3) if eligible[i]]
            top = {i for i in allowed if scores[i] == max(scores[j] for j in allowed)}
            assert outputs == (top or {None})
            for correct in itertools.product((0, 1), repeat=3):
                values = {0 if y is None else correct[y] for y in outputs}
                oracle_a = max((correct[y] for y in allowed), default=0)
                assert max(values) <= oracle_a <= max(correct)
                assert (len(values) > 1) == (len({correct[y] for y in top}) > 1)
                count += 1
    # Same observed evidence; opposite intended meanings: no answer satisfies both.
    for output in (None, 0, 1):
        assert not (output in {0} and output in {1})
    return count


def main():
    old_path, new_path = TEX / "paper_applsci.tex", TEX / "paper_information.tex"
    old, new = old_path.read_text(encoding="utf-8"), new_path.read_text(encoding="utf-8")
    old_tables, new_tables = tables(old), tables(new)
    old_figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", old)
    new_figures = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", new)
    abstract = new.split(r"\abstract{", 1)[1].split(r"\keyword", 1)[0]
    abstract_words = len(abstract.split())
    log = (TEX / "paper_information.log").read_text(encoding="utf-8", errors="replace")
    bibliography = (TEX / "references_verified.bib").read_text(encoding="utf-8") + (TEX / "references_information.bib").read_text(encoding="utf-8")
    keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bibliography))
    used = {key.strip() for group in re.findall(r"\\cite\w*\{([^}]+)\}", new) for key in group.split(",")}
    references = re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", new)
    labels = re.findall(r"\\label\{([^}]+)\}", new)
    manifest = json.loads((ROOT / "literature" / "manifest.json").read_text(encoding="utf-8"))
    pdfs = []
    import fitz
    for rec in manifest:
        path = ROOT / "literature" / "pdf" / (rec["doi"].split("/")[-1] + ".pdf")
        with fitz.open(path) as doc:
            first = doc[0].get_text().lower()
            pdfs.append({"doi": rec["doi"], "pages": len(doc), "sha256_matches": sha(path) == rec["sha256"], "doi_on_first_page": rec["doi"].lower() in first})
    report = {
        "scope": "Rewrite preservation and build checks only; not scientific acceptance or submission readiness",
        "original_sha256": sha(old_path), "rewrite_sha256": sha(new_path),
        "original_baseline_unchanged": sha(old_path).upper() == "75A3CBB673EE687522E41DC296440BB1433C098A52BBCCDFBEEB1A44D7410A5D",
        "empirical_tables_identical": old_tables == new_tables,
        "table_count": len(new_tables), "figure_references_identical": sorted(old_figures) == sorted(new_figures),
        "figure_order_changed_for_narrative": old_figures != new_figures,
        "figure_count": len(new_figures), "abstract_words": abstract_words,
        "missing_bibkeys": sorted(used - keys), "missing_labels": sorted(set(references) - set(labels)),
        "duplicate_labels": sorted({x for x in labels if labels.count(x) > 1}),
        "log_problems": [line for line in log.splitlines() if any(t in line for t in ("Overfull", "undefined", "multiply defined", "! LaTeX Error", "Rerun to"))],
        "finite_property_cases": finite_property_checks(), "literature_pdfs": pdfs,
        "pdf_sha256": sha(TEX / "paper_information.pdf"),
        "visual_qa": "Separate human/agent page inspection required; not certified by this script",
    }
    (ROOT / "REWRITE_AUDIT.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    assert report["original_baseline_unchanged"] and report["empirical_tables_identical"]
    assert report["figure_references_identical"] and not report["missing_bibkeys"]
    assert not report["missing_labels"] and not report["duplicate_labels"]
    assert not report["log_problems"] and abstract_words <= 200
    assert all(p["sha256_matches"] and p["doi_on_first_page"] for p in pdfs)


if __name__ == "__main__":
    main()
