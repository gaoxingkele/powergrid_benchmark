from __future__ import annotations

import csv
import json
import re
import time
from pathlib import Path
from urllib.parse import quote

import requests


ROOT = Path(r"D:\aicoding\powergrid_benchmark")
OUT = ROOT / "reviews" / "mintou_2026-08-09_journal_fit_audit"
PROJECTS = ROOT / "paper_projects"


def normalize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def split_references(text: str) -> list[tuple[int, str]]:
    parts = re.split(r"\n## References\s*\n", text, maxsplit=1, flags=re.I)
    if len(parts) != 2:
        return []
    refs = re.split(r"\n## ", parts[1], maxsplit=1)[0]
    starts = list(re.finditer(r"(?m)^(?:\[(\d+)\]|(\d+)\.)\s", refs))
    out = []
    for i, match in enumerate(starts):
        end = starts[i + 1].start() if i + 1 < len(starts) else len(refs)
        out.append((int(match.group(1) or match.group(2)), re.sub(r"\s+", " ", refs[match.start():end]).strip()))
    return out


def clean_doi(raw: str) -> str:
    return raw.rstrip(".,;)]}*_")


def publication_years(message: dict, doi: str) -> set[int]:
    """Return defensible publication/issue years without treating deposit dates as publication dates.

    MDPI can post an article online at the end of one calendar year while assigning it
    to the following year's volume/issue. Crossref records the latter under
    ``journal-issue``. Older IEEE records can have a null ``issued`` date; for those,
    a four-digit proceedings year embedded in the DOI is a useful fallback. A
    Crossref ``created`` timestamp is intentionally excluded because it is a metadata
    registration date, not a bibliographic publication year.
    """

    years: set[int] = set()
    for container in (message, message.get("journal-issue", {})):
        for key in ("published-print", "published-online", "issued"):
            parts = container.get(key, {}).get("date-parts", [])
            if parts and parts[0] and parts[0][0] is not None:
                years.add(int(parts[0][0]))
    if not years:
        doi_year = re.search(r"(?:^|[./])(19\d{2}|20\d{2})(?:[./]|$)", doi)
        if doi_year:
            years.add(int(doi_year.group(1)))
    return years


def main() -> None:
    session = requests.Session()
    session.headers.update({"User-Agent": "powergrid-benchmark-integrity-audit/1.0 (mailto:iamafan@xmu.edu.cn)"})
    rows = []
    cache: dict[str, dict] = {}
    for manuscript in sorted(PROJECTS.glob("mintou_p*/manuscript/MANUSCRIPT.md")):
        paper = manuscript.parts[-3]
        for ref_id, reference in split_references(manuscript.read_text(encoding="utf-8")):
            match = re.search(r"10\.\d{4,9}/[^\s<]+", reference, flags=re.I)
            doi = clean_doi(match.group(0)) if match else ""
            row = {"paper": paper, "ref_id": ref_id, "doi": doi, "status": "", "crossref_title": "", "crossref_year": "", "title_token_coverage": "", "year_in_reference": "", "url": "", "reference": reference}
            if not doi:
                row["status"] = "MANUAL_NO_DOI"
                rows.append(row)
                continue
            key = doi.lower()
            if key not in cache:
                url = "https://api.crossref.org/works/" + quote(doi, safe="")
                try:
                    response = session.get(url, timeout=30)
                    if response.status_code == 200:
                        cache[key] = {"ok": True, "message": response.json()["message"], "url": url}
                    else:
                        cache[key] = {"ok": False, "status": response.status_code, "url": url}
                except Exception as exc:
                    cache[key] = {"ok": False, "error": type(exc).__name__, "url": url}
                time.sleep(0.11)
            result = cache[key]
            row["url"] = result["url"]
            if not result.get("ok"):
                row["status"] = "NOT_FOUND_OR_TRANSPORT"
                rows.append(row)
                continue
            message = result["message"]
            title = (message.get("title") or [""])[0]
            years = publication_years(message, doi)
            title_tokens = [x for x in normalize(title) if len(x) > 2]
            ref_tokens = set(normalize(reference))
            coverage = sum(x in ref_tokens for x in title_tokens) / max(1, len(title_tokens))
            year_ok = not years or any(str(year) in reference for year in years)
            row.update({
                "crossref_title": title,
                "crossref_year": ";".join(str(year) for year in sorted(years)),
                "title_token_coverage": f"{coverage:.3f}",
                "year_in_reference": year_ok,
                "status": "VERIFIED" if coverage >= 0.80 and year_ok else "MISMATCH_REVIEW",
            })
            rows.append(row)
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "reference_verification_crossref.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)
    summary = {}
    for paper in sorted({r["paper"] for r in rows}):
        subset = [r for r in rows if r["paper"] == paper]
        counts = {status: sum(r["status"] == status for r in subset) for status in sorted({r["status"] for r in subset})}
        summary[paper] = {"references": len(subset), **counts}
    (OUT / "reference_verification_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
