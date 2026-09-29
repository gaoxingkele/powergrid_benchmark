"""Download OA papers + GitHub repos + open datasets for PG-T tracking targets.

Uses D:\\aicoding\\Lib\\download_tools (aria2 first). Safe to re-run.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
PAPER_ROOT = ROOT / "papers" / "literature" / "grid_tracking_targets"
PAPER_PDF = PAPER_ROOT / "pdfs"
PAPER_META = PAPER_ROOT / "metadata"
CODE_ROOT = ROOT / "data" / "public_datasets" / "grid_tracking" / "code"
DATA_ROOT = ROOT / "data" / "public_datasets" / "grid_tracking" / "datasets"
PROXY = "http://127.0.0.1:17890"

# (target_id, year, title, arxiv_or_oa_pdf_url)
PAPERS = [
    ("PG-T01", 2026, "IEEE9_TSA_graph_dataset_20000", "https://arxiv.org/pdf/2608.18318"),
    ("PG-T01", 2025, "PowerPINN_toolbox_power_system_components", "https://arxiv.org/pdf/2502.06412"),
    ("PG-T01", 2023, "PINNacle_NeurIPS2024_benchmark", "https://arxiv.org/pdf/2306.08827"),
    ("PG-T01", 2024, "Integrating_PINNs_into_power_system_dynamic_simulations", "https://arxiv.org/pdf/2404.13325"),
    ("PG-T01", 2023, "Transient_stability_analysis_with_PINNs", "https://arxiv.org/pdf/2106.13638"),
    ("PG-T02", 2025, "SoCal_28Bus_distribution_digital_twin_dataset", "https://arxiv.org/pdf/2504.06588"),
    ("PG-T02", 2026, "CONDUCTOR_LLM_orchestrated_digital_twin", "https://arxiv.org/pdf/2606.24609"),
    ("PG-T04", 2021, "MAPDN_MARL_active_voltage_control", "https://arxiv.org/pdf/2110.14300"),
    ("PG-T05", 2025, "WindFM_foundation_model_wind_power", "https://arxiv.org/pdf/2509.06311"),
    ("PG-T05", 2025, "SunCastNet_solar_forecasting_economic", "https://arxiv.org/pdf/2509.06925"),
    ("PG-T06", 2024, "GAIA_LLM_advanced_power_dispatch", "https://arxiv.org/pdf/2408.03847"),
    ("PG-T06", 2025, "Grid_Agent_LLM_multi_agent_grid_control", "https://arxiv.org/pdf/2508.05702"),
    ("PG-T08", 2025, "Transformer_DETR_X_digital_twin_SciRep", "https://www.nature.com/articles/s41598-024-83561-7.pdf"),
    ("PG-T09", 2026, "InspecSafe_V1_multimodal_inspection_SciData", "https://www.nature.com/articles/s41597-026-07796-x.pdf"),
    ("PG-T10", 2024, "Lightweight_AI_edge_LVDN_Frontiers", "https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2024.1424663/pdf"),
    ("PG-T10", 2025, "On_device_AI_models_survey", "https://arxiv.org/pdf/2503.06027"),
    ("PG-T11", 2026, "Hyperscale_datacenter_carbon_emissions", "https://arxiv.org/pdf/2606.05420"),
    ("PG-T13", 2025, "IBR_stability_datagen_framework", "https://arxiv.org/pdf/2512.06369"),
    ("PG-T16", 2024, "OPFData_AC_OPF_topological_perturbations", "https://arxiv.org/pdf/2406.07234"),
    ("PG-T16", 2025, "PGLearn_open_source_OPF_learning_toolkit", "https://arxiv.org/pdf/2505.22825"),
    ("PG-T17", 2025, "Power_grid_control_graph_distributed_RL", "https://arxiv.org/pdf/2509.02861"),
    ("PG-T17", 2025, "Optimizing_power_grid_topologies_RL_survey", "https://arxiv.org/pdf/2504.08210"),
    ("PG-T03", 2020, "SimBench_benchmark_dataset_Energies", "https://www.mdpi.com/1996-1073/13/12/3290/pdf"),
    ("PG-T21", 2019, "ACN_Data_open_EV_charging_dataset", "https://arxiv.org/pdf/1901.08085"),
]

# (target_id, name, git_url)
REPOS = [
    ("PG-T01", "PINNacle", "https://github.com/i207M/PINNacle.git"),
    ("PG-T01", "unified_pinn_smib_tsa_cct", "https://github.com/albert8943/unified-physics-informed-neural-surrogate-smib-tsa-cct-benchmark.git"),
    ("PG-T02", "digital_twin_dataset", "https://github.com/caltech-netlab/digital-twin-dataset.git"),
    ("PG-T02", "PowerAgentBench", "https://github.com/kosmylo/PowerAgentBench.git"),
    ("PG-T02", "CONDUCTOR", "https://github.com/antonioalcantaramata/CONDUCTOR.git"),
    ("PG-T03", "probabilistic_pv_hosting_capacity", "https://github.com/skortmann/probabilistic-pv-hosting-capacity.git"),
    ("PG-T04", "MAPDN", "https://github.com/Future-Power-Networks/MAPDN.git"),
    ("PG-T04", "EnEnv", "https://github.com/djbogucki/EnEnv.git"),
    ("PG-T04", "virtual_power_plant", "https://github.com/vinerya/virtual-power-plant.git"),
    ("PG-T05", "WindFM", "https://github.com/shiyu-coder/WindFM.git"),
    ("PG-T08", "pinn_transformer_thermal_model", "https://github.com/mzaib1012/pinn-transformer-thermal-model.git"),
    ("PG-T11", "CarbonX", "https://github.com/codecexp/CarbonX.git"),
    ("PG-T11", "open_grid_emissions", "https://github.com/singularity-energy/open-grid-emissions.git"),
    ("PG-T11", "hyperscale_emissions", "https://github.com/gianguidi/hyperscale-emissions.git"),
    ("PG-T12", "ieee123_ml_fault_location", "https://github.com/fernando-barreira/ieee123-ml-fault-location.git"),
    ("PG-T12", "protect90_dataset", "https://github.com/julianoelhaf/protect90-dataset.git"),
    ("PG-T13", "datagen_ibr", "https://github.com/MauroGarciaLorenzo/datagen.git"),
    ("PG-T13", "Grid_Cyber_Vulnerability_Dataset", "https://github.com/pnnl/Grid-Cyber-Vulnerability-Dataset.git"),
    ("PG-T14", "oHySEM", "https://github.com/IIT-EnergySystemModels/oHySEM.git"),
    ("PG-T09", "InspecSafe", "https://github.com/liuzy0708/InspecSafe.git"),
]

# (target_id, name, url, dest_rel) — modest-size open files
DATASETS = [
    (
        "PG-T01",
        "smib_pinn_splits",
        "https://zenodo.org/records/19562416/files/all_splits_20260211_190612.csv?download=1",
        "smib_pinn/all_splits_20260211_190612.csv",
    ),
    (
        "PG-T01",
        "smib_pinn_train",
        "https://zenodo.org/records/19562416/files/train_data_20260211_190612.csv?download=1",
        "smib_pinn/train_data_20260211_190612.csv",
    ),
    (
        "PG-T01",
        "smib_pinn_val",
        "https://zenodo.org/records/19562416/files/val_data_20260211_190612.csv?download=1",
        "smib_pinn/val_data_20260211_190612.csv",
    ),
    (
        "PG-T01",
        "smib_pinn_test",
        "https://zenodo.org/records/19562416/files/test_data_20260211_190612.csv?download=1",
        "smib_pinn/test_data_20260211_190612.csv",
    ),
    (
        "PG-T12",
        "ieee33_der_fault_location",
        "https://zenodo.org/records/15210584/files/Short-Circuit%20Fault%20Location%20Dataset%20for%20Distribution%20Systems%20with%20DER%20Integration.zip?download=1",
        "fault_location/ieee33_der_fault_location.zip",
    ),
]


def git_shallow_clone(url: str, dest: Path) -> str:
    if dest.exists() and (dest / ".git").exists():
        try:
            subprocess.run(
                ["git", "-C", str(dest), "pull", "--ff-only"],
                check=False,
                capture_output=True,
                text=True,
                timeout=180,
            )
            return "updated"
        except Exception as exc:
            return f"update_error:{exc}"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    cmd = ["git", "clone", "--depth", "1", url, str(dest)]
    # Prefer proxy via env for git if configured
    env = dict(**{k: v for k, v in __import__("os").environ.items()})
    env.setdefault("https_proxy", PROXY)
    env.setdefault("http_proxy", PROXY)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600, env=env)
        if r.returncode == 0:
            return "cloned"
        # retry without proxy
        r2 = subprocess.run(
            ["git", "clone", "--depth", "1", url, str(dest)],
            capture_output=True,
            text=True,
            timeout=600,
        )
        return "cloned" if r2.returncode == 0 else f"fail:{r2.stderr[-300:]}"
    except Exception as exc:
        return f"error:{exc}"


def fetch_file(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        return "exists"
    code = download(url, dest, proxy=PROXY, use_aria2=True, fallback=True)
    if code == 0 and dest.exists() and dest.stat().st_size > 0:
        # basic PDF check when expected
        if dest.suffix.lower() == ".pdf":
            head = dest.read_bytes()[:8]
            if not head.startswith(b"%PDF"):
                return "non_pdf"
        return "downloaded"
    return f"fail_code_{code}"


def main() -> None:
    PAPER_PDF.mkdir(parents=True, exist_ok=True)
    PAPER_META.mkdir(parents=True, exist_ok=True)
    CODE_ROOT.mkdir(parents=True, exist_ok=True)
    DATA_ROOT.mkdir(parents=True, exist_ok=True)

    paper_rows = []
    for tid, year, title, url in PAPERS:
        out = PAPER_PDF / tid / f"{title}.pdf"
        print(f"[paper] {tid} {title}", flush=True)
        status = fetch_file(url, out)
        print(f"  -> {status} ({out.stat().st_size if out.exists() else 0} B)", flush=True)
        paper_rows.append(
            {
                "target_id": tid,
                "year": year,
                "title": title,
                "url": url,
                "path": str(out.relative_to(ROOT)).replace("\\", "/") if out.exists() else "",
                "status": status,
                "bytes": out.stat().st_size if out.exists() else 0,
            }
        )
        time.sleep(0.3)

    repo_rows = []
    for tid, name, url in REPOS:
        dest = CODE_ROOT / tid / name
        print(f"[repo] {tid} {name}", flush=True)
        status = git_shallow_clone(url, dest)
        size = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file()) if dest.exists() else 0
        print(f"  -> {status} (~{size} B)", flush=True)
        repo_rows.append(
            {
                "target_id": tid,
                "name": name,
                "url": url,
                "path": str(dest.relative_to(ROOT)).replace("\\", "/") if dest.exists() else "",
                "status": status,
                "bytes": size,
            }
        )

    data_rows = []
    for tid, name, url, rel in DATASETS:
        dest = DATA_ROOT / rel
        print(f"[data] {tid} {name}", flush=True)
        status = fetch_file(url, dest)
        print(f"  -> {status} ({dest.stat().st_size if dest.exists() else 0} B)", flush=True)
        data_rows.append(
            {
                "target_id": tid,
                "name": name,
                "url": url,
                "path": str(dest.relative_to(ROOT)).replace("\\", "/") if dest.exists() else "",
                "status": status,
                "bytes": dest.stat().st_size if dest.exists() else 0,
            }
        )

    # HuggingFace dataset landing notes (full dump may be huge; record pointer)
    hf_notes = [
        {
            "target_id": "PG-T13",
            "name": "SIIB-Time",
            "url": "https://huggingface.co/datasets/neurips26-PSML/SIIB-Time",
            "note": "Paired EMT/RMS GFM/GFL trajectories; pull via huggingface-cli when needed",
        },
        {
            "target_id": "PG-T04",
            "name": "MAPDN_voltage_control_data",
            "url": "https://huggingface.co/datasets/hsvgbkhgbv/Multi-Agent-Power-Distribution-Networks",
            "note": "voltage_control_data.zip + traditional_control_data.zip",
        },
        {
            "target_id": "PG-T09",
            "name": "InspecSafe-V1",
            "url": "https://huggingface.co/datasets/Tetrabot2026/InspecSafe-V1",
            "note": "Multimodal industrial inspection including power facilities",
        },
        {
            "target_id": "PG-T05",
            "name": "WindFM_weights",
            "url": "https://huggingface.co/NeoQuasar/WindFM",
            "note": "Pretrained WindFM + tokenizer",
        },
    ]
    (DATA_ROOT / "huggingface_pointers.json").write_text(
        json.dumps(hf_notes, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    def write_csv(path: Path, rows: list[dict]) -> None:
        if not rows:
            return
        with path.open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)

    write_csv(PAPER_META / "papers_download_status.csv", paper_rows)
    write_csv(PAPER_META / "repos_download_status.csv", repo_rows)
    write_csv(PAPER_META / "datasets_download_status.csv", data_rows)

    summary = {
        "papers_ok": sum(1 for r in paper_rows if r["status"] in {"downloaded", "exists"} and r["bytes"] > 1000),
        "papers_total": len(paper_rows),
        "repos_ok": sum(1 for r in repo_rows if r["status"] in {"cloned", "updated"} and r["bytes"] > 0),
        "repos_total": len(repo_rows),
        "datasets_ok": sum(1 for r in data_rows if r["status"] in {"downloaded", "exists"} and r["bytes"] > 0),
        "datasets_total": len(data_rows),
        "hf_pointers": len(hf_notes),
    }
    (PAPER_META / "download_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
