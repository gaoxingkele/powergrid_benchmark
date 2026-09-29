"""Fetch archived PDFs that the bulk downloader missed.

For each target URL: list Wayback snapshots with HTTP 200, then try the newest
few in turn, validating the PDF magic bytes before keeping a file.  Live URLs are
tried first when the host still serves the document.
"""

from __future__ import annotations

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

PROXY = "http://127.0.0.1:17890"
OUT = Path(__file__).resolve().parent / "source_pdfs_v2"
POOL = Path(r"F:\aicoding\powergrid_benchmark\_scratch_render\candidate_pool_v2.json")
TARGETS = re.compile(
    r"(Main Report_updated|Main_Report_updated|Nordic_Grid_Disturbance_and_Fault_Statistics_2011"
    r"|nordic_and_baltic_grid_disturbance_statistics_2019|NORDIC_GRID_DISTURBANCE_AND_FAULT_STATISTICS_2010"
    r"|Odessa_Disturbance|investigation-9-august-2019|Winter_Storm_Generator_Outages"
    r"|Quebec-Disturbance|FrequencyInvestigationReport|Disturbance_Sweden_Denmark)",
    re.I,
)


def opener():
    build = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    build.addheaders = [("User-Agent", "Mozilla/5.0 (research)")]
    return build


def snapshots(op, url: str) -> list[str]:
    query = (
        "http://web.archive.org/cdx/search/cdx?url="
        + urllib.parse.quote(url, safe="")
        + "&fl=timestamp,statuscode&filter=statuscode:200&limit=20&output=json"
    )
    try:
        data = json.loads(op.open(query, timeout=120).read().decode("utf-8", errors="replace"))
    except Exception:
        return []
    rows = [r for r in (data[1:] if data else []) if len(r) >= 2]
    rows.sort(key=lambda r: r[0], reverse=True)
    return [r[0] for r in rows[:5]]


def fetch(op, url: str) -> bytes | None:
    try:
        payload = op.open(url, timeout=240).read()
    except Exception:
        return None
    return payload if payload[:4] == b"%PDF" else None


def main() -> None:
    op = opener()
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    have = {p.name.lower() for p in OUT.glob("*.pdf")}
    done = 0
    for item in pool:
        name = item["file"]
        if not TARGETS.search(name):
            continue
        safe = re.sub(r"[^A-Za-z0-9._-]", "_", urllib.parse.unquote(name))
        if not safe.lower().endswith(".pdf"):
            safe += ".pdf"
        if safe.lower() in have:
            continue
        original = item["url"]
        payload = fetch(op, original)  # live first
        source = "live"
        if payload is None:
            for ts in snapshots(op, original):
                payload = fetch(op, f"https://web.archive.org/web/{ts}id_/{original}")
                if payload is not None:
                    source = f"wayback:{ts}"
                    break
        if payload is None:
            print(f"  FAIL  {safe[:70]}")
            continue
        (OUT / safe).write_bytes(payload)
        done += 1
        print(f"  OK    {source:22s} {len(payload)/1e6:6.2f} MB  {safe[:60]}")
    print(f"\n新增 {done} 份 → {OUT}")


if __name__ == "__main__":
    sys.exit(main())
