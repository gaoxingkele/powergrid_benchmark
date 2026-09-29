"""Retry failed OA PDFs and Zenodo dataset files for grid tracking bundle."""
from __future__ import annotations

import json
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "papers/literature/grid_tracking_targets/pdfs"
DATA = ROOT / "data/public_datasets/grid_tracking/datasets"
PROXY = "http://127.0.0.1:17890"
UA = "powergrid-benchmark/1.0"


def is_pdf(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 20000 and path.read_bytes()[:4] == b"%PDF"


def try_urls(dest: Path, urls: list[str]) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if is_pdf(dest):
        print(f"ok_exists {dest} {dest.stat().st_size}")
        return True
    for url in urls:
        print(f"try {dest.name} <- {url}")
        code = download(url, dest, proxy=PROXY)
        if is_pdf(dest):
            print(f"  ok {code} {dest.stat().st_size}")
            return True
        print(f"  fail {code} size={dest.stat().st_size if dest.exists() else 0}")
    return False


def zenodo_files(record_id: int) -> list[dict]:
    api = f"https://zenodo.org/api/records/{record_id}"
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as resp:
        rec = json.loads(resp.read().decode())
    return rec.get("files") or []


def main() -> None:
    try_urls(
        PAPER / "PG-T03" / "SimBench_benchmark_dataset_Energies.pdf",
        [
            "https://mdpi-res.com/d_attachment/energies/energies-13-03290/article_deploy/energies-13-03290.pdf",
            "https://www.mdpi.com/1996-1073/13/12/3290/pdf?version=1592579800",
        ],
    )
    try_urls(
        PAPER / "PG-T08" / "Transformer_DETR_X_digital_twin_SciRep.pdf",
        ["https://www.nature.com/articles/s41598-024-83561-7.pdf"],
    )
    try_urls(
        PAPER / "PG-T09" / "InspecSafe_V1_multimodal_inspection_SciData.pdf",
        ["https://www.nature.com/articles/s41597-026-07796-x.pdf"],
    )
    try_urls(
        PAPER / "PG-T10" / "Lightweight_AI_edge_LVDN_Frontiers.pdf",
        [
            "https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2024.1424663/pdf",
            "https://www.frontiersin.org/articles/10.3389/fenrg.2024.1424663/pdf",
        ],
    )

    for record_id, subdir in [(15210584, "fault_location"), (19562416, "smib_pinn")]:
        print(f"zenodo {record_id}")
        try:
            files = zenodo_files(record_id)
        except Exception as exc:
            print(f"  api_error {exc}")
            continue
        for f in files:
            key = f.get("key")
            links = f.get("links") or {}
            url = links.get("download") or links.get("self")
            if not key or not url:
                continue
            dest = DATA / subdir / key
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists() and dest.stat().st_size > 0:
                print(f"  exists {key} {dest.stat().st_size}")
                continue
            print(f"  dl {key}")
            code = download(url, dest, proxy=PROXY)
            print(f"    {code} {dest.stat().st_size if dest.exists() else 0}")


if __name__ == "__main__":
    main()
