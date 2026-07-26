"""Download renewable / power-system / BMS extension datasets into the local cache.

Pragmatic policy:
- Prefer fully open, moderate-size sources.
- For multi-GB catalogues (PGLearn Large, climate projections), cache metadata
  plus a representative subset so the benchmark library stays usable.
- Never store API tokens in the repository.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "public_datasets"
MANIFEST = DATA_ROOT / "manifests" / "public_dataset_manifest.csv"
USER_AGENT = "powergrid-benchmark-dataset-fetcher/0.2"


@dataclass
class Job:
    dataset_id: str
    category: str
    rel_path: str
    source_url: str
    access_mode: str
    main_tasks: str
    notes: str
    kind: str
    url: str
    default_download: str = "yes"
    extra: dict | None = None


JOBS: list[Job] = [
    Job(
        "nasa_pcoe_battery",
        "battery_bms",
        "battery_bms/nasa_pcoe_battery",
        "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets",
        "direct_download",
        "SOC;SOH;RUL;battery aging;EIS",
        "NASA PCoE Li-ion aging cells; core .mat files via public mirrors",
        "nasa_battery_core",
        "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets",
    ),
    Job(
        "nasa_randomized_recommissioned_battery",
        "battery_bms",
        "battery_bms/nasa_randomized_recommissioned_battery",
        "https://data.nasa.gov/dataset/randomized-and-recommissioned-battery-dataset",
        "metadata_and_landing",
        "second-life battery;pack aging;variable load",
        "Landing page + data.json metadata cached; full pack files may require portal download",
        "landing_json",
        "https://data.nasa.gov/api/views/xg3n-ngei.json",
        extra={"landing": "https://data.nasa.gov/dataset/randomized-and-recommissioned-battery-dataset"},
    ),
    Job(
        "oxford_battery_degradation",
        "battery_bms",
        "battery_bms/oxford_battery_degradation",
        "https://ora.ox.ac.uk/objects/uuid:03ba4b01-cfed-46d3-9b1a-7d4a7bdf6fac",
        "direct_download",
        "SOH;RUL;drive-cycle aging",
        "Oxford Battery Degradation Dataset 1 (8 Kokam pouch cells)",
        "oxford_mat",
        "https://ora.ox.ac.uk/objects/uuid:03ba4b01-cfed-46d3-9b1a-7d4a7bdf6fac/download_file?file_format=*&safe_filename=Oxford_Battery_Degradation_Dataset_1.mat&type_of_work=Dataset",
    ),
    Job(
        "calce_battery",
        "battery_bms",
        "battery_bms/calce_battery",
        "https://calce.umd.edu/battery-data",
        "landing_and_samples",
        "SOC;SOH;DST;FUDS;temperature-aware estimation",
        "CALCE open battery portal page + A123 sample zip links when reachable",
        "calce_portal",
        "https://calce.umd.edu/battery-data",
    ),
    Job(
        "battery_archive",
        "battery_bms",
        "battery_bms/battery_archive",
        "https://batteryarchive.org/",
        "landing",
        "battery aging catalogue;cross-lab comparison",
        "Battery Archive landing + study summaries cached as catalogue entry",
        "html",
        "https://batteryarchive.org/study_summaries.html",
    ),
    Job(
        "stanford_tri_high_power_battery",
        "battery_bms",
        "battery_bms/stanford_tri_high_power_battery",
        "https://doi.org/10.17605/OSF.IO/9CEAV",
        "osf_api",
        "high C-rate characterization;stochastic battery modeling",
        "Stanford-TRI high-power Li-ion characterization (OSF)",
        "osf",
        "9ceav",
    ),
    Job(
        "m5bat_bess",
        "bess_grid",
        "bess_grid/m5bat_bess",
        "https://doi.org/10.18154/rwth-2024-04895",
        "rwth_publications",
        "BESS FCR;intraday trading;grid frequency;SOC",
        "M5BAT large-scale BESS field operation (Apr 2023 report package)",
        "m5bat",
        "https://publications.rwth-aachen.de/record/985295",
    ),
    Job(
        "finland_afrr_weather",
        "bess_grid",
        "bess_grid/finland_afrr_weather",
        "https://doi.org/10.5281/zenodo.17494555",
        "zenodo",
        "aFRR market;frequency regulation;weather-energy correlation",
        "Finland aFRR energy market + weather hourly Jun 2024-Mar 2025",
        "zenodo",
        "17494555",
    ),
    Job(
        "bess_european_balancing_inputs",
        "bess_grid",
        "bess_grid/bess_european_balancing_inputs",
        "https://doi.org/10.5281/zenodo.18199323",
        "zenodo",
        "FCR;aFRR;BESS market simulation",
        "Paper data for European balancing-market BESS strategies (DE/FI)",
        "zenodo",
        "18199323",
    ),
    Job(
        "renewables_ninja_country_sample",
        "renewable_weather",
        "renewable_weather/renewables_ninja_country_sample",
        "https://www.renewables.ninja/downloads",
        "direct_download",
        "wind capacity factor;solar capacity factor;planning scenarios",
        "Country-level renewables.ninja sample files (EU wind/PV archives when reachable)",
        "renewables_ninja",
        "https://www.renewables.ninja/downloads",
    ),
    Job(
        "vce_rare_power",
        "renewable_weather",
        "renewable_weather/vce_rare_power",
        "https://zenodo.org/records/13937523",
        "zenodo_subset",
        "resource adequacy;county wind/solar CF",
        "VCE RARE county-level renewable CF; metadata + readme first, files on demand",
        "zenodo_record",
        "13937523",
        default_download="yes",
    ),
    Job(
        "eia860_wind_solar_cf",
        "renewable_weather",
        "renewable_weather/eia860_wind_solar_cf",
        "https://zenodo.org/records/20518257",
        "zenodo_record_meta",
        "plant-level wind/solar CF;resource adequacy;extreme weather years",
        "EIA-860 plant CF catalogue (full multi-GB archive kept metadata-first)",
        "zenodo_record",
        "20518257",
    ),
    Job(
        "secures_energy",
        "renewable_weather",
        "renewable_weather/secures_energy",
        "https://zenodo.org/records/14615500",
        "zenodo_record_meta",
        "climate-energy;European demand/supply to 2100",
        "SECURES-Energy metadata cached; full climate projections download on demand",
        "zenodo_record",
        "14615500",
    ),
    Job(
        "era5_eu_supply_demand",
        "renewable_weather",
        "renewable_weather/era5_eu_supply_demand",
        "https://zenodo.org/records/13938926",
        "zenodo_record_meta",
        "wind/solar CF;hydro inflow;heating/cooling demand",
        "Weather/climate-driven EU power supply-demand time series metadata",
        "zenodo_record",
        "13938926",
    ),
    Job(
        "pglearn_small",
        "opf_benchmarks",
        "opf_benchmarks/pglearn_small",
        "https://huggingface.co/collections/PGLearn/pglearn-small",
        "huggingface_subset",
        "ML-OPF;AC/DC/SOC OPF learning;feasibility",
        "PGLearn Small collection: record card + one representative system subset if available",
        "hf_pglearn",
        "PGLearn/14_ieee",
    ),
    Job(
        "opfdata_landing",
        "opf_benchmarks",
        "opf_benchmarks/opfdata_landing",
        "https://arxiv.org/abs/2406.07234",
        "landing",
        "AC-OPF;topological perturbation;GNN OPF",
        "OPFData paper + GCS bucket landing notes (gs://gridopt-dataset/)",
        "html_and_notes",
        "https://arxiv.org/html/2406.07234",
    ),
    Job(
        "acn_data_static",
        "distribution_ev",
        "distribution_ev/acn_data_static",
        "https://github.com/tongxin-li/ACN-Data-Static",
        "git_sparse_clone",
        "EV charging scheduling;charging curve clustering;V2G studies",
        "Sparse offline snapshot of ACN-Data (session JSON + README; full 85k curves optional)",
        "git_sparse_acn",
        "https://github.com/tongxin-li/ACN-Data-Static.git",
    ),
]


def http_get(url: str, dest: Path, timeout: int = 45) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)


def http_text(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def http_json(url: str, timeout: int = 30) -> dict:
    return json.loads(http_text(url, timeout=timeout))


def try_http_get(url: str, dest: Path, timeout: int = 45) -> str | None:
    try:
        http_get(url, dest, timeout=timeout)
        return None
    except Exception as exc:
        return f"{type(exc).__name__}: {exc}"


def write_readme(path: Path, job: Job, status: str, details: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    text = (
        f"# {job.dataset_id}\n\n"
        f"- Category: `{job.category}`\n"
        f"- Source: {job.source_url}\n"
        f"- Access: `{job.access_mode}`\n"
        f"- Status: `{status}`\n"
        f"- Tasks: {job.main_tasks}\n"
        f"- Notes: {job.notes}\n\n"
        f"## Fetch details\n\n{details}\n"
    )
    (path / "README.md").write_text(text, encoding="utf-8")


def clone_git(url: str, dest: Path) -> None:
    if (dest / ".git").exists():
        subprocess.run(["git", "-C", str(dest), "pull", "--ff-only"], check=False)
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and not any(dest.iterdir()):
        dest.rmdir()
    subprocess.run(["git", "clone", "--depth", "1", url, str(dest)], check=True)


def clone_git_sparse_acn(url: str, dest: Path) -> str:
    """Clone only session metadata/README to avoid 85k time-series blobs."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=dest, check=True)
    subprocess.run(["git", "remote", "add", "origin", url], cwd=dest, check=True)
    subprocess.run(["git", "config", "core.sparseCheckout", "true"], cwd=dest, check=True)
    sparse = dest / ".git" / "info" / "sparse-checkout"
    sparse.write_text("README.md\nsession data/\n", encoding="utf-8")
    # Prefer partial clone; fall back to depth-1 sparse fetch.
    result = subprocess.run(
        ["git", "pull", "--depth", "1", "origin", "main"],
        cwd=dest,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        result2 = subprocess.run(
            ["git", "pull", "--depth", "1", "origin", "master"],
            cwd=dest,
            capture_output=True,
            text=True,
        )
        if result2.returncode != 0:
            # Fallback: download README + session JSON via raw.githubusercontent
            details = [f"sparse pull failed: {result.stderr or result2.stderr}"]
            raw_base = "https://raw.githubusercontent.com/tongxin-li/ACN-Data-Static/main"
            for rel in [
                "README.md",
                "session%20data/caltech_sessions.json",
            ]:
                name = urllib.parse.unquote(rel.split("/")[-1])
                out = dest / ("session data" if "session" in rel else ".")
                if "session" in rel:
                    out.mkdir(parents=True, exist_ok=True)
                    target = out / name
                else:
                    target = dest / name
                try:
                    http_get(f"{raw_base}/{rel}", target, timeout=180)
                    details.append(f"raw fetched {name}")
                except Exception as exc:
                    details.append(f"raw {name} failed: {exc}")
            return "\n".join(details) + "\n"
    files = [str(p.relative_to(dest)) for p in dest.rglob("*") if p.is_file() and ".git" not in p.parts]
    return f"sparse ACN clone files={len(files)}: {', '.join(files[:20])}\n"


def fetch_zenodo_record(record_id: str, dest: Path, download_files: bool = True, max_files: int = 8, max_mb: float = 800) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    meta = http_json(f"https://zenodo.org/api/records/{record_id}")
    (dest / "zenodo_record.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    files = meta.get("files") or []
    downloaded = []
    skipped = []
    total = 0.0
    if download_files:
        for f in files:
            size_mb = float(f.get("size") or 0) / (1024 * 1024)
            key = f.get("key") or f.get("filename") or "file.bin"
            if len(downloaded) >= max_files or total + size_mb > max_mb:
                skipped.append(f"{key} ({size_mb:.1f} MB)")
                continue
            url = (f.get("links") or {}).get("content") or (f.get("links") or {}).get("download")
            if not url:
                skipped.append(key)
                continue
            out = dest / key
            if out.exists() and out.stat().st_size > 0:
                downloaded.append(key)
                total += size_mb
                continue
            try:
                print(f"  zenodo {record_id}: {key} ({size_mb:.1f} MB)")
                http_get(url, out, timeout=600)
                downloaded.append(key)
                total += size_mb
            except Exception as exc:
                skipped.append(f"{key} ERR={exc}")
    return (
        f"Zenodo record {record_id}: title={(meta.get('metadata') or {}).get('title')}\n"
        f"Downloaded files ({len(downloaded)}): {', '.join(downloaded) or 'none'}\n"
        f"Skipped/held ({len(skipped)}): {', '.join(skipped[:20]) or 'none'}\n"
    )


def fetch_osf(node_id: str, dest: Path, max_files: int = 20) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    meta = http_json(f"https://api.osf.io/v2/nodes/{node_id}/")
    (dest / "osf_node.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    files_meta = http_json(f"https://api.osf.io/v2/nodes/{node_id}/files/osfstorage/")
    (dest / "osf_files.json").write_text(json.dumps(files_meta, ensure_ascii=False, indent=2), encoding="utf-8")
    downloaded = []
    for item in (files_meta.get("data") or [])[:max_files]:
        attrs = item.get("attributes") or {}
        name = attrs.get("name") or "file"
        if attrs.get("kind") != "file":
            continue
        link = ((item.get("links") or {}).get("download"))
        if not link:
            continue
        out = dest / name
        if out.exists() and out.stat().st_size > 0:
            downloaded.append(name)
            continue
        try:
            print(f"  osf {node_id}: {name}")
            http_get(link, out, timeout=300)
            downloaded.append(name)
        except Exception as exc:
            downloaded.append(f"{name} ERR={exc}")
    return f"OSF node {node_id}: downloaded {len(downloaded)} entries: {', '.join(downloaded) or 'none'}\n"


def fetch_nasa_battery(dest: Path) -> str:
    """Fetch NASA PCoE core cells from commonly mirrored public URLs."""
    dest.mkdir(parents=True, exist_ok=True)
    notes = []
    err = try_http_get(
        "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets",
        dest / "nasa_landing.html",
        timeout=20,
    )
    notes.append("Landing OK" if err is None else f"Landing skipped: {err}")

    candidates = [
        (
            "B0005.mat",
            "https://raw.githubusercontent.com/chintanegc/battery-remaining-useful-life-prediction/master/Battery%20Dataset/B0005.mat",
        ),
        (
            "B0006.mat",
            "https://raw.githubusercontent.com/chintanegc/battery-remaining-useful-life-prediction/master/Battery%20Dataset/B0006.mat",
        ),
        (
            "B0007.mat",
            "https://raw.githubusercontent.com/chintanegc/battery-remaining-useful-life-prediction/master/Battery%20Dataset/B0007.mat",
        ),
        (
            "B0018.mat",
            "https://raw.githubusercontent.com/chintanegc/battery-remaining-useful-life-prediction/master/Battery%20Dataset/B0018.mat",
        ),
    ]
    ok = []
    for name, url in candidates:
        out = dest / "cells" / name
        if out.exists() and out.stat().st_size > 1000:
            ok.append(name)
            continue
        print(f"  nasa cell {name}", flush=True)
        err = try_http_get(url, out, timeout=60)
        if err is None:
            ok.append(name)
        else:
            notes.append(f"{name} failed: {err}")
    (dest / "SOURCE_NOTE.md").write_text(
        "Core .mat cells were fetched from public research mirrors commonly used with the NASA PCoE dataset. "
        "For the complete official pack, use the NASA Open Data / DASHlink portal linked in README.\n",
        encoding="utf-8",
    )
    return "NASA PCoE: " + "; ".join(notes) + f"\nCells cached: {', '.join(ok) or 'none'}\n"


def fetch_oxford(dest: Path, url: str) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    out = dest / "Oxford_Battery_Degradation_Dataset_1.mat"
    if not (out.exists() and out.stat().st_size > 1000):
        print("  oxford mat")
        http_get(url, out, timeout=300)
    # readme
    try:
        readme_url = "https://ora.ox.ac.uk/objects/uuid:03ba4b01-cfed-46d3-9b1a-7d4a7bdf6fac/download_file?file_format=txt&safe_filename=readme.txt&type_of_work=Dataset"
        http_get(readme_url, dest / "readme.txt", timeout=60)
    except Exception as exc:
        return f"Oxford mat downloaded ({out.stat().st_size} bytes); readme failed: {exc}\n"
    return f"Oxford dataset mat size={out.stat().st_size} bytes; readme cached.\n"


def fetch_calce(dest: Path) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    try:
        http_get("https://calce.umd.edu/battery-data", dest / "battery-data.html", timeout=60)
        http_get("https://calce.umd.edu/data", dest / "data.html", timeout=60)
    except Exception as exc:
        return f"CALCE portal fetch failed: {exc}\n"
    # Known public sample packages occasionally linked from CALCE pages / mirrors.
    sample_urls = [
        ("CS2_35.zip", "https://web.calce.umd.edu/batteries/data/CS2_35.zip"),
        ("CS2_36.zip", "https://web.calce.umd.edu/batteries/data/CS2_36.zip"),
        ("CX2_16.zip", "https://web.calce.umd.edu/batteries/data/CX2_16.zip"),
    ]
    ok = []
    for name, url in sample_urls:
        out = dest / "samples" / name
        if out.exists() and out.stat().st_size > 1000:
            ok.append(name)
            continue
        try:
            print(f"  calce {name}")
            http_get(url, out, timeout=300)
            ok.append(name)
        except Exception as exc:
            (dest / "samples" / f"{name}.failed.txt").parent.mkdir(parents=True, exist_ok=True)
            (dest / "samples" / f"{name}.failed.txt").write_text(str(exc), encoding="utf-8")
    return f"CALCE portal HTML cached; sample zips: {', '.join(ok) or 'none (manual portal download may be required)'}\n"


def fetch_m5bat(dest: Path) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    details = []
    try:
        http_get("https://publications.rwth-aachen.de/record/985295", dest / "record.html", timeout=60)
        details.append("RWTH record HTML cached.")
    except Exception as exc:
        details.append(f"record HTML failed: {exc}")
    # Try common download endpoints exposed on RWTH publications pages.
    candidates = [
        "https://publications.rwth-aachen.de/record/985295/files/M5BAT_04-2023_RAW.zip",
        "https://publications.rwth-aachen.de/record/985295/files/Report_04-2023.pdf",
    ]
    for url in candidates:
        name = url.rsplit("/", 1)[-1]
        out = dest / name
        if out.exists() and out.stat().st_size > 1000:
            details.append(f"already have {name}")
            continue
        try:
            print(f"  m5bat {name}")
            http_get(url, out, timeout=600)
            details.append(f"downloaded {name} ({out.stat().st_size} bytes)")
        except Exception as exc:
            details.append(f"{name} failed: {exc}")
    return "\n".join(details) + "\n"


def fetch_renewables_ninja(dest: Path) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    http_get("https://www.renewables.ninja/downloads", dest / "downloads.html", timeout=60)
    # OPSD also hosts renewables.ninja packages; fetch country capacity factors via known open package if present.
    opsd_candidates = [
        (
            "ninja_pv_europe_v1.1_merra2.csv",
            "https://www.renewables.ninja/static/downloads/ninja_pv_europe_v1.1_merra2.csv",
        ),
        (
            "ninja_wind_europe_v1.1_current_on-offshore.csv",
            "https://www.renewables.ninja/static/downloads/ninja_wind_europe_v1.1_current_on-offshore.csv",
        ),
    ]
    ok = []
    for name, url in opsd_candidates:
        out = dest / name
        if out.exists() and out.stat().st_size > 1000:
            ok.append(name)
            continue
        try:
            print(f"  renewables.ninja {name}")
            http_get(url, out, timeout=300)
            ok.append(name)
        except Exception as exc:
            (dest / f"{name}.failed.txt").write_text(str(exc), encoding="utf-8")
    return f"downloads.html cached; country files: {', '.join(ok) or 'none'}\n"


def fetch_pglearn(dest: Path) -> str:
    dest.mkdir(parents=True, exist_ok=True)
    details = []
    try:
        http_get("https://huggingface.co/collections/PGLearn/pglearn-small", dest / "collection.html", timeout=60)
        details.append("HF collection HTML cached.")
    except Exception as exc:
        details.append(f"collection HTML failed: {exc}")
    # Try huggingface_hub for a small representative dataset.
    try:
        from huggingface_hub import hf_hub_download, list_repo_files

        repo = "PGLearn/14_ieee"
        files = list_repo_files(repo, repo_type="dataset")
        (dest / "14_ieee_filelist.json").write_text(json.dumps(files, indent=2), encoding="utf-8")
        # Prefer small parquet/json samples
        preferred = [f for f in files if f.endswith((".json", ".md", ".parquet", ".csv", ".txt"))]
        chosen = preferred[:5] if preferred else files[:3]
        local_dir = dest / "14_ieee"
        local_dir.mkdir(parents=True, exist_ok=True)
        for f in chosen:
            print(f"  hf {repo}:{f}")
            path = hf_hub_download(repo_id=repo, filename=f, repo_type="dataset", local_dir=str(local_dir))
            details.append(f"downloaded {path}")
    except Exception as exc:
        details.append(f"HF subset download failed: {exc}")
        (dest / "PGLEARN_NOTE.md").write_text(
            "Full PGLearn collections are multi-million samples. "
            "Cache collection landing locally and download specific systems via HuggingFace when needed.\n"
            f"Error: {exc}\n",
            encoding="utf-8",
        )
    return "\n".join(details) + "\n"


def run_job(job: Job) -> tuple[str, str]:
    dest = DATA_ROOT / job.rel_path
    print(f"==> {job.dataset_id} ({job.kind})", flush=True)
    try:
        if job.kind == "git":
            clone_git(job.url, dest)
            details = f"git clone/pull {job.url}"
            status = "downloaded"
        elif job.kind == "git_sparse_acn":
            details = clone_git_sparse_acn(job.url, dest)
            status = "downloaded" if any(dest.rglob("*.json")) or (dest / "README.md").exists() else "partial"
        elif job.kind == "nasa_battery_core":
            details = fetch_nasa_battery(dest)
            status = "downloaded" if any((dest / "cells").glob("*.mat")) else "partial"
        elif job.kind == "oxford_mat":
            details = fetch_oxford(dest, job.url)
            status = "downloaded"
        elif job.kind == "calce_portal":
            details = fetch_calce(dest)
            status = "downloaded" if (dest / "battery-data.html").exists() else "partial"
        elif job.kind == "html":
            dest.mkdir(parents=True, exist_ok=True)
            http_get(job.url, dest / "index.html", timeout=60)
            details = f"HTML cached from {job.url}"
            status = "metadata-only"
        elif job.kind == "landing_json":
            dest.mkdir(parents=True, exist_ok=True)
            http_get(job.url, dest / "dataset.json", timeout=60)
            landing = (job.extra or {}).get("landing")
            if landing:
                http_get(landing, dest / "landing.html", timeout=60)
            details = "Socrata/NASA metadata JSON + landing cached"
            status = "metadata-only"
        elif job.kind == "osf":
            details = fetch_osf(job.url, dest)
            status = "downloaded" if any(dest.iterdir()) else "partial"
        elif job.kind == "m5bat":
            details = fetch_m5bat(dest)
            status = "downloaded" if any(dest.glob("*.zip")) or any(dest.glob("*.pdf")) else "partial"
        elif job.kind == "zenodo":
            details = fetch_zenodo_record(job.url, dest, download_files=True, max_files=12, max_mb=1500)
            status = "downloaded"
        elif job.kind == "zenodo_record":
            # Metadata always; optionally light files.
            details = fetch_zenodo_record(job.url, dest, download_files=True, max_files=3, max_mb=200)
            status = "downloaded" if any(p.suffix != ".json" and p.name != "README.md" for p in dest.rglob("*") if p.is_file()) else "metadata-only"
        elif job.kind == "renewables_ninja":
            details = fetch_renewables_ninja(dest)
            status = "downloaded" if any(dest.glob("*.csv")) else "partial"
        elif job.kind == "hf_pglearn":
            details = fetch_pglearn(dest)
            status = "downloaded" if (dest / "14_ieee").exists() else "partial"
        elif job.kind == "html_and_notes":
            dest.mkdir(parents=True, exist_ok=True)
            http_get(job.url, dest / "arxiv_html.html", timeout=90)
            (dest / "GCS_BUCKET.md").write_text(
                "OPFData JSON files are hosted at gs://gridopt-dataset/.\n"
                "Use `gsutil -m cp -r gs://gridopt-dataset/<case> .` when cloud credentials/network allow.\n",
                encoding="utf-8",
            )
            details = "arXiv HTML + GCS notes cached"
            status = "metadata-only"
        else:
            details = f"unknown kind {job.kind}"
            status = "planned"
        write_readme(dest, job, status, details)
        return status, details
    except Exception as exc:
        write_readme(dest, job, "failed", str(exc))
        return "failed", str(exc)


def upsert_manifest(results: list[tuple[Job, str]]) -> None:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    fields = list(rows[0].keys()) if rows else [
        "dataset_id",
        "category",
        "local_path",
        "status",
        "source_url",
        "access_mode",
        "default_download",
        "main_tasks",
        "notes",
    ]
    by_id = {r["dataset_id"]: r for r in rows}
    for job, status in results:
        by_id[job.dataset_id] = {
            "dataset_id": job.dataset_id,
            "category": job.category,
            "local_path": f"data/public_datasets/{job.rel_path}",
            "status": status,
            "source_url": job.source_url,
            "access_mode": job.access_mode,
            "default_download": job.default_download,
            "main_tasks": job.main_tasks,
            "notes": job.notes,
        }
    # Also upgrade acn_data note if static snapshot exists.
    if "acn_data" in by_id and (DATA_ROOT / "distribution_ev" / "acn_data_static").exists():
        by_id["acn_data"]["notes"] = (
            by_id["acn_data"].get("notes", "")
            + "; offline snapshot available at distribution_ev/acn_data_static"
        )
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(by_id.values())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", default=None, help="Optional dataset_id filter")
    args = parser.parse_args()
    jobs = JOBS
    if args.only:
        wanted = set(args.only)
        jobs = [j for j in JOBS if j.dataset_id in wanted]
    results: list[tuple[Job, str]] = []
    for job in jobs:
        status, _ = run_job(job)
        results.append((job, status))
        time.sleep(0.2)
    upsert_manifest(results)
    print("=== summary ===")
    for job, status in results:
        print(f"{job.dataset_id}: {status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
