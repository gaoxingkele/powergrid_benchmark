"""Download primary + high-quality citing papers for grid-tracking datasets.

Targets datasets added in the 2026-08 grid-tracking bundle (EnEnv, MAPDN, PROTECT-90,
InspecSafe, SIIB-Time, SMIB PINN, Swiss DER, IEEE33 fault, etc.).

OA PDFs only; paywalled entries are logged in metadata for manual fetch.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PAPER_PDF = ROOT / "papers/literature/grid_tracking_targets/pdfs"
PAPER_META = ROOT / "papers/literature/grid_tracking_targets/metadata"
PROXY = "http://127.0.0.1:17890"

# (target_id, year, filename_stem, url, dataset_id, role, venue_note)
PAPERS = [
    # --- primary / dataset descriptor (not yet in bundle) ---
    ("PG-T03", 2025, "SwissDER_SciData_2025", "https://www.nature.com/articles/s41597-025-05830-y.pdf", "grid_tracking_swiss_der", "primary", "Scientific Data"),
    ("PG-T03", 2025, "SwissDER_SEGAN_planning_2025", "https://www.sciencedirect.com/science/article/pii/S2352346725000678/pdfft?md5=placeholder", "grid_tracking_swiss_der", "related", "Sustainable Energy Grids and Networks"),
    ("PG-T04", 2023, "BenchMARL_benchmarking_MARL", "https://arxiv.org/pdf/2312.01472", "grid_tracking_enenv", "framework", "arXiv / JMLR track"),
    ("PG-T04", 2021, "MAPDN_NeurIPS2021_proceedings", "https://proceedings.neurips.cc/paper/2021/file/1a6727711b84fd1efbb87fc565199d13-Paper.pdf", "grid_tracking_mapdn", "primary", "NeurIPS 2021"),
    ("PG-T01", 2026, "PINN_surrogate_VV_framework_SMIB", "https://arxiv.org/pdf/2603.17836", "grid_tracking_smib_pinn", "related", "arXiv"),
    ("PG-T13", 2025, "Neural_Operators_power_system_components", "https://arxiv.org/pdf/2511.05216", "grid_tracking_siib_time", "related", "arXiv"),
    ("PG-T13", 2026, "Microgrid_digital_twin_dataset_IBR", "https://arxiv.org/pdf/2603.10262", "grid_tracking_siib_time", "related", "arXiv"),
    ("PG-T10", 2016, "DSGC_Taming_instabilities_power_grid_EPJ", "https://arxiv.org/pdf/1603.03584", "grid_tracking_uci_grid_stability", "primary", "EPJ Special Topics"),
    ("PG-T10", 2020, "Smart_grid_stability_prediction_Energies", "https://www.mdpi.com/1996-1073/13/10/2559/pdf", "grid_tracking_uci_grid_stability", "citing", "Energies"),
    # --- MAPDN citing (high-quality venues) ---
    ("PG-T04", 2024, "MAPDN_SafetyConstrained_AVC", "https://arxiv.org/pdf/2405.08443", "grid_tracking_mapdn", "citing", "arXiv / MAPDN env"),
    ("PG-T04", 2023, "MAPDN_SafetyLayer_AAMAS2023", "https://www.southampton.ac.uk/~eg/AAMAS2023/pdfs/p1533.pdf", "grid_tracking_mapdn", "citing", "AAMAS 2023"),
    ("PG-T04", 2023, "OffTheGrid_MARL_datasets_baselines", "https://arxiv.org/pdf/2302.00521", "grid_tracking_mapdn", "citing", "AAMAS 2023"),
    ("PG-T04", 2025, "MAPDN_AppliedEnergy_data_driven_control_2025", "https://intra.ece.ucr.edu/~nyu/papers/2025-Data_Driven_Control_ADN-WG.pdf", "grid_tracking_mapdn", "citing", "Applied Energy"),
    ("PG-T04", 2024, "MAPDN_AAAI_Imagine_Initialize_Explore_2024", "https://ojs.aaai.org/index.php/AAAI/article/download/29698/31195", "grid_tracking_mapdn", "citing", "AAAI 2024"),
    ("PG-T10", 2020, "Smart_grid_stability_prediction_Energies", "https://mdpi-res.com/d_attachment/energies/energies-13-02559/article_deploy/energies-13-02559.pdf", "grid_tracking_uci_grid_stability", "citing", "Energies"),
    # --- InspecSafe / industrial inspection citing ---
    ("PG-T09", 2026, "SafeSceneReason_industrial_hazard_benchmark", "https://arxiv.org/pdf/2608.09230", "grid_tracking_inspecsafe", "citing", "arXiv"),
    ("PG-T09", 2026, "SteelBench_VLM_industrial_environments", "https://arxiv.org/pdf/2607.05264", "grid_tracking_inspecsafe", "citing", "arXiv"),
    # --- fault / protection adjacent ---
    ("PG-T12", 2020, "Data_driven_fault_localization_DER_Energies", "https://mdpi-res.com/d_attachment/energies/energies-13-00275/article_deploy/energies-13-00275.pdf", "grid_tracking_fault_location_ieee33", "related", "Energies"),
]

# Curated OA overrides (OpenAlex / publisher direct links verified manually)
OA_OVERRIDES = {
    "SwissDER_SEGAN_planning_2025": "https://doi.org/10.1016/j.segan.2025.101678",
}

# Replace placeholder URLs
FIXED = []
for row in PAPERS:
    tid, year, stem, url, ds, role, venue = row
    url = OA_OVERRIDES.get(stem, url)
    if "placeholder" in url:
        continue
    FIXED.append((tid, year, stem, url, ds, role, venue))
PAPERS = FIXED


def is_pdf(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 15000 and path.read_bytes()[:4] == b"%PDF"


def fetch(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and is_pdf(dest):
        return "exists"
    code = download(url, dest, proxy=PROXY, use_aria2=True, fallback=True)
    if is_pdf(dest):
        return "downloaded"
    if dest.exists() and dest.stat().st_size > 15000:
        return "non_pdf"
    return f"fail_{code}"


def main() -> None:
    PAPER_PDF.mkdir(parents=True, exist_ok=True)
    PAPER_META.mkdir(parents=True, exist_ok=True)

    rows = []
    ok = 0
    for tid, year, stem, url, ds, role, venue in PAPERS:
        dest = PAPER_PDF / tid / f"{stem}.pdf"
        print(f"[{role}] {ds} {stem}", flush=True)
        status = fetch(url, dest)
        nbytes = dest.stat().st_size if dest.exists() else 0
        if status in {"downloaded", "exists"} and nbytes > 15000:
            ok += 1
        print(f"  -> {status} ({nbytes})", flush=True)
        rows.append(
            {
                "target_id": tid,
                "year": year,
                "title": stem,
                "url": url,
                "dataset_id": ds,
                "role": role,
                "venue": venue,
                "path": str(dest.relative_to(ROOT)).replace("\\", "/") if dest.exists() else "",
                "status": status,
                "bytes": nbytes,
                "batch": "dataset_literature_v1",
            }
        )
        time.sleep(0.25)

    out_csv = PAPER_META / "papers_dataset_literature_status.csv"
    with out_csv.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    summary = {
        "papers_ok": ok,
        "papers_total": len(rows),
        "papers_failed": [r["title"] for r in rows if r["status"] not in {"downloaded", "exists"} or r["bytes"] <= 15000],
    }
    (PAPER_META / "dataset_literature_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
