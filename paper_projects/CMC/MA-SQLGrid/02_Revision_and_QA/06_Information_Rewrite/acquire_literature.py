"""Acquire a small, explicitly non-systematic Information comparison corpus."""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

import requests

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download

ROOT = Path(__file__).resolve().parent
DOIS = [
    "10.3390/info17010065",  # SQL query descriptions and learning assistance
    "10.3390/info16050368",  # conceptual schema descriptions
    "10.3390/info16110960",  # systems validation of information extraction
    "10.3390/info11050271",  # formal multi-agent coordination
]
VERIFIED_ALTERNATES = {
    "10.3390/info17010065": "https://ousar.lib.okayama-u.ac.jp/files/public/7/70078/20260220102019294010/fulltext.pdf",
    "10.3390/info16050368": "https://mdpi-res.com/d_attachment/information/information-16-00368/article_deploy/information-16-00368-v2.pdf",
    "10.3390/info16110960": "https://mdpi-res.com/d_attachment/information/information-16-00960/article_deploy/information-16-00960.pdf",
    "10.3390/info11050271": "https://mdpi-res.com/d_attachment/information/information-11-00271/article_deploy/information-11-00271.pdf",
}


def get_json(url):
    response = requests.get(url, timeout=40)
    response.raise_for_status()
    return response.json()


def main():
    records = []
    (ROOT / "literature" / "pdf").mkdir(parents=True, exist_ok=True)
    for doi in DOIS:
        m = get_json("https://api.crossref.org/works/" + doi)["message"]
        rec = {
            "title": m["title"][0],
            "authors": [" ".join(filter(None, [a.get("given"), a.get("family")])) for a in m.get("author", [])],
            "year": m["published"]["date-parts"][0][0],
            "venue": m["container-title"][0], "doi": doi,
            "citation_count": None, "code_url": None,
            "source_platforms": ["Crossref"], "fetched_at": date.today().isoformat(),
            "license": m.get("license", []), "oa_checks": {},
        }
        for name, url in {
            "OpenAlex": "https://api.openalex.org/works/https://doi.org/" + doi,
            "Unpaywall": "https://api.unpaywall.org/v2/" + doi + "?email=iamafan@xmu.edu.cn",
        }.items():
            try:
                data = get_json(url)
                rec["oa_checks"][name] = data
                rec["source_platforms"].append(name)
            except Exception as exc:
                rec["oa_checks"][name] = {"error": str(exc)}
        oa = rec["oa_checks"].get("Unpaywall", {})
        ax = rec["oa_checks"].get("OpenAlex", {})
        loc = oa.get("best_oa_location") or {}
        axloc = ax.get("best_oa_location") or {}
        url = loc.get("url_for_pdf") or axloc.get("pdf_url")
        rec["discovered_pdf_url"] = url
        url = VERIFIED_ALTERNATES.get(doi, url)
        rec.update(open_access_status=oa.get("oa_status", ax.get("open_access", {}).get("oa_status", "unknown")),
                   full_text_status="open_pdf" if url else "unknown", pdf_url=url,
                   download_status="not_requested", local_pdf_path=None)
        records.append(rec)
        manifest = ROOT / "literature" / "manifest.json"
        manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        if url:
            dest = ROOT / "literature" / "pdf" / (doi.split("/")[-1] + ".pdf")
            if not dest.exists():
                download(url, dest, max_tries=2, timeout=30, connect_timeout=15, fallback=False)
            if dest.exists() and dest.read_bytes().startswith(b"%PDF-"):
                rec.update(download_status="downloaded", local_pdf_path=str(dest),
                           sha256=hashlib.sha256(dest.read_bytes()).hexdigest())
            else:
                rec["download_status"] = "failed"
        manifest.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        print(rec["title"], rec["download_status"], flush=True)


if __name__ == "__main__":
    main()
