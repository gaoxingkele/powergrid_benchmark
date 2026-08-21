from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
QUERIES = {
    "c2_domain": [
        "power grid natural language processing",
        "power grid knowledge graph",
        "power system knowledge graph",
        "power fault knowledge graph",
        "maintenance knowledge graph",
        "grid relation extraction",
        "fault report text mining",
    ],
    "c2_method": [
        "extractive text summarization",
        "graph based text summarization",
        "technical document summarization",
        "causal relation extraction natural language",
        "counterfactual graph text",
    ],
    "ma_domain": [
        "power grid database natural language",
        "power system multi-agent",
        "smart grid multi-agent system",
        "power grid large language model",
    ],
    "ma_method": [
        "text-to-SQL",
        "schema linking SQL generation",
        "natural language database query",
        "large language model multi-agent framework",
        "agentic AI multi-agent",
        "database question answering SQL",
    ],
}


def query_crossref(q: str) -> list[dict]:
    params = urllib.parse.urlencode({
        "query.bibliographic": q,
        "filter": "issn:2076-3417,from-pub-date:2020-01-01",
        "rows": 50,
        "select": "DOI,title,published,URL,abstract,subject,type,author,container-title",
    })
    url = "https://api.crossref.org/works?" + params
    req = urllib.request.Request(url, headers={"User-Agent": "CodexResearch/1.0 (mailto:liubijing@outlook.com)"})
    with urllib.request.urlopen(req, timeout=45) as response:
        return json.load(response)["message"]["items"]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    merged: dict[str, dict] = {}
    hits: defaultdict[str, list[str]] = defaultdict(list)
    for group, queries in QUERIES.items():
        for q in queries:
            for item in query_crossref(q):
                doi = item.get("DOI", "").lower()
                if not doi.startswith("10.3390/app"):
                    continue
                merged[doi] = item
                hits[doi].append(f"{group}:{q}")
            time.sleep(0.15)
    rows = []
    for doi, item in merged.items():
        year = item.get("published", {}).get("date-parts", [[None]])[0][0]
        title = item.get("title", [""])[0]
        rows.append({
            "doi": doi,
            "year": year,
            "title": title,
            "query_hits": hits[doi],
            "hit_count": len(hits[doi]),
            "url": item.get("URL"),
            "abstract": item.get("abstract", ""),
        })
    rows.sort(key=lambda x: (-x["hit_count"], -(x["year"] or 0), x["title"]))
    (OUT / "crossref_candidates.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"candidates={len(rows)}")
    for row in rows[:150]:
        print(f'{row["hit_count"]:2} {row["year"]} {row["doi"]} | {row["title"]}')


if __name__ == "__main__":
    main()
