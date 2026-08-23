#!/usr/bin/env python3
"""Fresh bibliography-existence and citation-key audit for the CMC manuscripts.

The script uses Crossref registration metadata for DOI-bearing entries and the
publisher/archival URL stored in BibTeX for URL-only entries.  It records the
exact lookup URL and never upgrades an inaccessible or metadata-free page to a
verified reference.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


USER_AGENT = (
    "powergrid-benchmark-reference-audit/1.0 "
    "(bibliographic integrity check; https://github.com/gaoxingkele/powergrid_benchmark)"
)


@dataclass
class BibEntry:
    entry_type: str
    key: str
    fields: dict[str, str]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest().upper()


def _balanced_block(text: str, start: int) -> tuple[str, int]:
    opener = text[start]
    closer = "}" if opener == "{" else ")"
    depth = 0
    quoted = False
    escaped = False
    for pos in range(start, len(text)):
        char = text[pos]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            continue
        if quoted:
            continue
        if char == opener:
            depth += 1
        elif char == closer:
            depth -= 1
            if depth == 0:
                return text[start + 1 : pos], pos + 1
    raise ValueError(f"Unbalanced BibTeX entry beginning at byte {start}")


def _parse_value(body: str, pos: int) -> tuple[str, int]:
    while pos < len(body) and body[pos].isspace():
        pos += 1
    if pos >= len(body):
        return "", pos
    if body[pos] == "{":
        value, end = _balanced_block(body, pos)
        return value.strip(), end
    if body[pos] == '"':
        pos += 1
        out: list[str] = []
        escaped = False
        while pos < len(body):
            char = body[pos]
            if escaped:
                out.append(char)
                escaped = False
            elif char == "\\":
                out.append(char)
                escaped = True
            elif char == '"':
                return "".join(out).strip(), pos + 1
            else:
                out.append(char)
            pos += 1
        raise ValueError("Unterminated quoted BibTeX value")
    end = body.find(",", pos)
    if end < 0:
        end = len(body)
    return body[pos:end].strip(), end


def parse_bib(path: Path) -> list[BibEntry]:
    text = path.read_text(encoding="utf-8")
    entries: list[BibEntry] = []
    pos = 0
    while True:
        match = re.search(r"@(\w+)\s*([\{(])", text[pos:], flags=re.I)
        if not match:
            break
        entry_type = match.group(1).lower()
        block_start = pos + match.start(2)
        body, pos = _balanced_block(text, block_start)
        comma = body.find(",")
        if comma < 0:
            raise ValueError(f"BibTeX entry without key separator: {body[:80]}")
        key = body[:comma].strip()
        field_text = body[comma + 1 :]
        fields: dict[str, str] = {}
        cursor = 0
        while cursor < len(field_text):
            while cursor < len(field_text) and (
                field_text[cursor].isspace() or field_text[cursor] == ","
            ):
                cursor += 1
            if cursor >= len(field_text):
                break
            name_match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", field_text[cursor:])
            if not name_match:
                raise ValueError(f"Cannot parse field in {key}: {field_text[cursor:cursor+80]!r}")
            name = name_match.group(1).lower()
            cursor += name_match.end()
            value, cursor = _parse_value(field_text, cursor)
            fields[name] = value
        entries.append(BibEntry(entry_type, key, fields))
    keys = [entry.key for entry in entries]
    if len(keys) != len(set(keys)):
        raise ValueError("Duplicate BibTeX keys detected")
    return entries


def strip_tex(value: str) -> str:
    value = value.replace("---", "-").replace("--", "-")
    value = re.sub(r"\\[`'\"^~=.uvHtcdb]\s*\{?([A-Za-z])\}?", r"\1", value)
    value = re.sub(r"\\(?:textit|emph|textbf|mathrm|operatorname)\s*\{([^{}]*)\}", r"\1", value)
    value = re.sub(r"\\[A-Za-z]+\*?", " ", value)
    return re.sub(r"[{}$]", "", value).strip()


def normalized(value: str) -> str:
    value = strip_tex(value)
    value = unicodedata.normalize("NFKD", value)
    value = "".join(char for char in value if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def authors_from_bib(value: str) -> list[str]:
    authors = re.split(r"\s+and\s+", strip_tex(value), flags=re.I)
    surnames: list[str] = []
    for author in authors:
        author = author.strip()
        if not author:
            continue
        if "," in author:
            surname = author.split(",", 1)[0]
        else:
            parts = author.split()
            surname_parts = parts[-1:]
            while len(parts) > len(surname_parts) and parts[-len(surname_parts) - 1].lower() in {
                "da", "de", "del", "der", "di", "du", "la", "van", "von"
            }:
                surname_parts.insert(0, parts[-len(surname_parts) - 1])
            surname = " ".join(surname_parts)
        surnames.append(normalized(surname))
    return surnames


class _MetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: list[dict[str, str]] = []
        self.in_title = False
        self.title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "meta":
            self.meta.append({key.lower(): value or "" for key, value in attrs})
        elif tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)


def extract_citations(tex_path: Path) -> set[str]:
    lines: list[str] = []
    for raw in tex_path.read_text(encoding="utf-8").splitlines():
        lines.append(re.split(r"(?<!\\)%", raw, maxsplit=1)[0])
    text = "\n".join(lines)
    pattern = re.compile(
        r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear|parencite|textcite)\w*"
        r"\s*(?:\[[^\]]*\]\s*){0,2}\{([^}]*)\}",
        flags=re.I,
    )
    keys: set[str] = set()
    for group in pattern.findall(text):
        keys.update(key.strip() for key in group.split(",") if key.strip())
    return keys


def fetch(url: str, accept: str = "application/json,text/html;q=0.9,*/*;q=0.5") -> tuple[int, str, bytes, str]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return (
                    int(response.status),
                    response.headers.get("Content-Type", ""),
                    response.read(4 * 1024 * 1024),
                    response.geturl(),
                )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last_error = exc
            if attempt < 2:
                time.sleep(0.5 * (attempt + 1))
    raise RuntimeError(str(last_error))


def crossref_lookup(doi: str) -> dict[str, Any]:
    query = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    status, content_type, payload, final_url = fetch(query, "application/json")
    if status != 200 or "json" not in content_type.lower():
        raise RuntimeError(f"Crossref returned HTTP {status} ({content_type})")
    message = json.loads(payload.decode("utf-8"))["message"]
    years: set[str] = set()
    for name in ("published-print", "published-online", "issued", "created"):
        date_parts = message.get(name, {}).get("date-parts", [])
        if date_parts and date_parts[0]:
            years.add(str(date_parts[0][0]))
    return {
        "query_url": query,
        "source_url": final_url,
        "title": " ".join(message.get("title", [])).strip(),
        "years": sorted(years),
        "authors": [normalized(item.get("family", "")) for item in message.get("author", [])],
        "doi": str(message.get("DOI", "")),
    }


def html_metadata(url: str) -> dict[str, Any]:
    status, content_type, payload, final_url = fetch(url)
    if status != 200:
        raise RuntimeError(f"Publisher URL returned HTTP {status}")
    if "html" not in content_type.lower():
        return {
            "query_url": url,
            "source_url": final_url,
            "title": "",
            "years": [],
            "authors": [],
            "content_type": content_type,
        }
    text = payload.decode("utf-8", errors="replace")
    parser = _MetaParser()
    parser.feed(text)

    def meta(names: list[str]) -> list[str]:
        found: list[str] = []
        for attrs in parser.meta:
            marker = (attrs.get("name") or attrs.get("property") or "").lower()
            if marker in names and attrs.get("content"):
                found.append(html.unescape(attrs["content"]).strip())
        return found

    titles = meta(["citation_title", "dc.title", "og:title"])
    if not titles and parser.title_parts:
        titles = [html.unescape(" ".join(parser.title_parts)).strip()]
    dates = meta(["citation_publication_date", "citation_date", "dc.date", "article:published_time"])
    years = sorted({match.group(0) for value in dates for match in [re.search(r"(?:19|20)\d{2}", value)] if match})
    return {
        "query_url": url,
        "source_url": final_url,
        "title": titles[0] if titles else "",
        "years": years,
        "authors": authors_from_bib(" and ".join(meta(["citation_author", "dc.creator"]))),
        "content_type": content_type,
    }


def compare(entry: BibEntry, remote: dict[str, Any], method: str) -> dict[str, Any]:
    local_title = strip_tex(entry.fields.get("title", ""))
    remote_title = remote.get("title", "")
    similarity = SequenceMatcher(None, normalized(local_title), normalized(remote_title)).ratio() if remote_title else 0.0
    local_year = re.search(r"(?:19|20)\d{2}", entry.fields.get("year", ""))
    year_ok = not local_year or local_year.group(0) in remote.get("years", [])
    local_authors = authors_from_bib(entry.fields.get("author", ""))
    remote_authors = [item for item in remote.get("authors", []) if item]
    author_ok = not local_authors or (
        bool(remote_authors)
        and local_authors[0] == remote_authors[0]
        and set(local_authors).issubset(set(remote_authors))
    )
    doi_ok = True
    if method == "crossref":
        doi_ok = normalized(entry.fields.get("doi", "")) == normalized(remote.get("doi", ""))
    metadata_complete = bool(remote_title) and (not local_authors or bool(remote_authors))
    verified = similarity >= 0.90 and year_ok and author_ok and doi_ok and metadata_complete
    return {
        "key": entry.key,
        "local": {
            "title": local_title,
            "year": local_year.group(0) if local_year else "",
            "authors": local_authors,
            "doi": entry.fields.get("doi", ""),
            "url": entry.fields.get("url", ""),
        },
        "lookup_method": method,
        "query_url": remote.get("query_url", ""),
        "source_url": remote.get("source_url", ""),
        "remote": {
            "title": remote_title,
            "years": remote.get("years", []),
            "authors": remote_authors,
            "doi": remote.get("doi", ""),
            "content_type": remote.get("content_type", ""),
        },
        "checks": {
            "title_similarity": round(similarity, 6),
            "title_match": similarity >= 0.90,
            "year_match": year_ok,
            "author_match": author_ok,
            "doi_match": doi_ok,
            "metadata_complete": metadata_complete,
        },
        "verdict": "VERIFIED" if verified else "MISMATCH",
    }


def audit_entry(entry: BibEntry, override: dict[str, Any] | None = None) -> dict[str, Any]:
    doi = entry.fields.get("doi", "").strip()
    url = entry.fields.get("url", "").strip()
    errors: list[str] = []
    if override:
        remote = {
            "query_url": override["source_url"],
            "source_url": override["source_url"],
            "title": override["title"],
            "years": [str(override["year"])] if override.get("year") else [],
            "authors": [normalized(item) for item in override.get("author_surnames", [])],
            "content_type": "documented primary-source verification",
        }
        result = compare(entry, remote, "documented_primary_source")
        result["override_record"] = override
        return result
    if doi:
        try:
            return compare(entry, crossref_lookup(doi), "crossref")
        except Exception as exc:  # noqa: BLE001 - recorded in audit trail
            errors.append(f"crossref: {exc}")
    if url:
        try:
            result = compare(entry, html_metadata(url), "publisher_url")
            result["lookup_errors"] = errors
            return result
        except Exception as exc:  # noqa: BLE001 - recorded in audit trail
            errors.append(f"publisher_url: {exc}")
    return {
        "key": entry.key,
        "local": {
            "title": strip_tex(entry.fields.get("title", "")),
            "year": strip_tex(entry.fields.get("year", "")),
            "authors": authors_from_bib(entry.fields.get("author", "")),
            "doi": doi,
            "url": url,
        },
        "lookup_method": "none",
        "query_url": "",
        "source_url": "",
        "remote": {},
        "checks": {},
        "lookup_errors": errors,
        "verdict": "NOT_FOUND",
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Fresh Reference-Existence and Citation-Key Audit",
        "",
        f"Generated: `{report['created_at']}`",
        f"Verdict: **{report['verdict']}**",
        f"BibTeX entries: **{report['counts']['bibliography']}**; cited keys: **{report['counts']['cited_keys']}**; verified: **{report['counts']['verified']}**; mismatches: **{report['counts']['mismatch']}**; not found: **{report['counts']['not_found']}**.",
        "",
        "This audit checks bibliographic existence/identity and the manuscript--bibliography key join. It does not by itself establish claim-to-source semantic fidelity or professional plagiarism clearance.",
        "",
        "## Citation-key join",
        "",
        f"- Missing bibliography keys: `{report['ghost_citations']['dangling']}`",
        f"- Uncited bibliography entries: `{report['ghost_citations']['orphan']}`",
        "",
        "## Entry-level audit trail",
        "",
        "| Key | Verdict | Lookup | Title similarity | Year | Authors | DOI | Source |",
        "|---|---|---|---:|---|---|---|---|",
    ]
    for item in report["entries"]:
        checks = item.get("checks", {})
        source = item.get("source_url") or item.get("query_url") or ""
        lines.append(
            "| {key} | {verdict} | {lookup} | {title} | {year} | {authors} | {doi} | {source} |".format(
                key=item["key"],
                verdict=item["verdict"],
                lookup=item.get("lookup_method", ""),
                title=checks.get("title_similarity", ""),
                year=checks.get("year_match", ""),
                authors=checks.get("author_match", ""),
                doi=checks.get("doi_match", ""),
                source=source.replace("|", "%7C"),
            )
        )
    failed = [item for item in report["entries"] if item["verdict"] != "VERIFIED"]
    if failed:
        lines.extend(["", "## Items requiring correction or manual primary-source verification", ""])
        for item in failed:
            lines.append(f"- `{item['key']}` — **{item['verdict']}**; errors: `{item.get('lookup_errors', [])}`; checks: `{item.get('checks', {})}`")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tex", type=Path, required=True)
    parser.add_argument("--bib", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--md-out", type=Path, required=True)
    parser.add_argument("--overrides", type=Path)
    args = parser.parse_args()
    tex = args.tex.resolve()
    bib = args.bib.resolve()
    entries = parse_bib(bib)
    overrides: dict[str, Any] = {}
    if args.overrides:
        overrides = json.loads(args.overrides.resolve().read_text(encoding="utf-8"))
    bib_keys = {entry.key for entry in entries}
    cited_keys = extract_citations(tex)
    results = [audit_entry(entry, overrides.get(entry.key)) for entry in entries]
    counts = {
        "bibliography": len(entries),
        "cited_keys": len(cited_keys),
        "verified": sum(item["verdict"] == "VERIFIED" for item in results),
        "mismatch": sum(item["verdict"] == "MISMATCH" for item in results),
        "not_found": sum(item["verdict"] == "NOT_FOUND" for item in results),
    }
    dangling = sorted(cited_keys - bib_keys)
    orphan = sorted(bib_keys - cited_keys)
    passed = counts["verified"] == len(entries) and not dangling and not orphan
    report = {
        "schema_version": "cmc-reference-integrity-audit-v1",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "verdict": "PASS" if passed else "FAIL",
        "inputs": {
            "tex": args.tex.as_posix(),
            "tex_sha256": sha256(tex),
            "bib": args.bib.as_posix(),
            "bib_sha256": sha256(bib),
            "overrides": args.overrides.as_posix() if args.overrides else None,
            "overrides_sha256": sha256(args.overrides.resolve()) if args.overrides else None,
        },
        "counts": counts,
        "ghost_citations": {"dangling": dangling, "orphan": orphan},
        "entries": results,
        "boundary": "Existence/identity and citation-key join only; citation-context and originality checks remain separate.",
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.md_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    write_markdown(report, args.md_out)
    print(json.dumps({"verdict": report["verdict"], "counts": counts, "dangling": dangling, "orphan": orphan}))
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
