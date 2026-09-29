"""Fill remaining grid-tracking OA papers + open datasets (gap batch)."""
from __future__ import annotations

import csv
import json
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download

ROOT = Path(__file__).resolve().parents[2]
PAPER_PDF = ROOT / "papers/literature/grid_tracking_targets/pdfs"
PAPER_META = ROOT / "papers/literature/grid_tracking_targets/metadata"
DATA = ROOT / "data/public_datasets/grid_tracking/datasets"
PROXY = "http://127.0.0.1:17890"
UA = "powergrid-benchmark-gapfill/0.2"

# Missing-direction / companion OA papers
PAPERS = [
    ("PG-T07", 2025, "Forced_oscillation_locating_IBR_SINDy", "https://arxiv.org/pdf/2508.17505"),
    ("PG-T09", 2026, "InspecSafe_V1_arxiv", "https://arxiv.org/pdf/2601.21173"),
    ("PG-T12", 2026, "PROTECT90_fault_dataset_paper", "https://arxiv.org/pdf/2606.24298"),
    ("PG-T12", 2025, "ML_fault_classification_localization_controlled_comparison", "https://arxiv.org/pdf/2510.00831"),
    ("PG-T04", 2025, "EnEnv_AAMAS2025", "https://www.ifaamas.org/Proceedings/aamas2025/pdfs/p361.pdf"),
    ("PG-T14", 2024, "PyPSA_Eur_sector_coupled_context", "https://arxiv.org/pdf/2110.02827"),
    ("PG-T11", 2022, "Open_grid_emissions_initiative_methods", "https://arxiv.org/pdf/2206.08977"),
    ("PG-T22", 2023, "Graph_neural_networks_PMU_event_detection", "https://arxiv.org/pdf/2301.11189"),
    ("PG-T18", 2024, "SDWPF_Scientific_Data", "https://www.nature.com/articles/s41597-024-03427-5.pdf"),
    ("PG-T01", 2024, "Integrating_PINNs_dynamics_already_ok_backup", "https://arxiv.org/pdf/2404.13325"),
    ("PG-T16", 2025, "Scalable_heterogeneous_GNN_OPF", "https://arxiv.org/pdf/2605.23194"),
    ("PG-T05", 2025, "FuXi_Energy_related_if_oa", "https://arxiv.org/pdf/2412.11974"),
]

# Clean empty / bad placeholders
PAPERS = [(a, b, c, d) for a, b, c, d in PAPERS if d.startswith("http")]


def is_pdf(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 15000 and path.read_bytes()[:4] == b"%PDF"


def fetch(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        if dest.suffix.lower() == ".pdf" and not is_pdf(dest):
            pass
        elif dest.suffix.lower() != ".pdf" or is_pdf(dest):
            return "exists"
    code = download(url, dest, proxy=PROXY, use_aria2=True, fallback=True)
    if dest.suffix.lower() == ".pdf":
        return "downloaded" if is_pdf(dest) else "non_pdf"
    return "downloaded" if code == 0 and dest.exists() and dest.stat().st_size > 0 else f"fail_{code}"


def zenodo_download(record_id: int, subdir: str, keys: list[str] | None = None) -> list[dict]:
    api = f"https://zenodo.org/api/records/{record_id}"
    req = urllib.request.Request(api, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as resp:
        rec = json.loads(resp.read().decode())
    out = []
    for f in rec.get("files") or []:
        key = f.get("key")
        if keys and key not in keys:
            continue
        url = (f.get("links") or {}).get("self") or (f.get("links") or {}).get("download")
        dest = DATA / subdir / key
        print(f"[zenodo:{record_id}] {key} ({f.get('size')})", flush=True)
        status = fetch(url, dest)
        out.append({"record": record_id, "key": key, "status": status, "bytes": dest.stat().st_size if dest.exists() else 0, "path": str(dest)})
        print(f"  -> {status}", flush=True)
    return out


def main() -> None:
    PAPER_PDF.mkdir(parents=True, exist_ok=True)
    PAPER_META.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(parents=True, exist_ok=True)

    paper_rows = []
    for tid, year, title, url in PAPERS:
        dest = PAPER_PDF / tid / f"{title}.pdf"
        print(f"[paper] {tid} {title}", flush=True)
        status = fetch(url, dest)
        print(f"  -> {status} {dest.stat().st_size if dest.exists() else 0}", flush=True)
        paper_rows.append(
            {
                "target_id": tid,
                "year": year,
                "title": title,
                "url": url,
                "path": str(dest.relative_to(ROOT)).replace("\\", "/") if dest.exists() else "",
                "status": status,
                "bytes": dest.stat().st_size if dest.exists() else 0,
                "batch": "gapfill_v1",
            }
        )
        time.sleep(0.2)

    data_rows = []
    # PROTECT-90: labels+readme first (zip started separately if huge)
    data_rows += zenodo_download(18418330, "protect90", ["hv_double_line_90kv_labels.csv", "README.md"])
    # Swiss DER allocation (moderate)
    try:
        data_rows += zenodo_download(16272961, "swiss_der_allocation")
    except Exception as exc:
        print("swiss_der_error", exc, flush=True)

    # UCI Electrical Grid Stability (T10)
    uci = DATA / "uci_electrical_grid_stability" / "Electrical_Grid_Stability_Simulated_Data.csv"
    # common mirror
    for url in [
        "https://archive.ics.uci.edu/ml/machine-learning-databases/00471/Data_for_UCI_named.csv",
        "https://raw.githubusercontent.com/jbrownlee/Datasets/master/electrical-grid-stability.csv",
    ]:
        print("[uci]", url, flush=True)
        st = fetch(url, uci)
        data_rows.append({"record": "uci", "key": uci.name, "status": st, "bytes": uci.stat().st_size if uci.exists() else 0, "path": str(uci)})
        if st in {"downloaded", "exists"} and uci.exists() and uci.stat().st_size > 1000:
            break

    # IEEE DataPort landing pages (auth-walled large dumps)
    landings = [
        ("PG-T07", "dpsyor_landing.html", "https://ieee-dataport.org/documents/dpsyor-dataset-power-system-oscillation-responses"),
        ("PG-T07", "dpsyfor_landing.html", "https://ieee-dataport.org/documents/dataset-power-system-forced-oscillation-responses"),
        ("PG-T01", "ieee9_tsa_dataport_doi_page.html", "https://dx.doi.org/10.21227/ebwk-j667"),
    ]
    for tid, name, url in landings:
        dest = DATA / "dataport_landings" / tid / name
        print(f"[landing] {tid} {name}", flush=True)
        st = fetch(url, dest)
        data_rows.append({"record": "landing", "key": name, "status": st, "bytes": dest.stat().st_size if dest.exists() else 0, "path": str(dest)})

    # EnEnv Google Drive pointer
    (DATA / "enenv" / "GOOGLE_DRIVE.txt").parent.mkdir(parents=True, exist_ok=True)
    (DATA / "enenv" / "GOOGLE_DRIVE.txt").write_text(
        "https://drive.google.com/drive/folders/1Od02_Bp_8tjpLnwvYnZat4HZUUF-Y-Ch?usp=sharing\n"
        "Source: EnEnv repo data.txt — requires browser/gdown auth for full scenario packs.\n",
        encoding="utf-8",
    )

    with (PAPER_META / "papers_gapfill_status.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(paper_rows[0].keys()))
        w.writeheader()
        w.writerows(paper_rows)
    with (PAPER_META / "datasets_gapfill_status.csv").open("w", encoding="utf-8-sig", newline="") as f:
        if data_rows:
            w = csv.DictWriter(f, fieldnames=list(data_rows[0].keys()))
            w.writeheader()
            w.writerows(data_rows)

    summary = {
        "papers_ok": sum(1 for r in paper_rows if r["status"] in {"downloaded", "exists"} and r["bytes"] > 15000),
        "papers_total": len(paper_rows),
        "dataset_entries": len(data_rows),
        "note": "Large: PROTECT-90 zip / InspecSafe tars / SIIB-Time full started by companion jobs",
    }
    (PAPER_META / "gapfill_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
