"""Repair incomplete extension dataset downloads."""
from __future__ import annotations

import json
import shutil
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "public_datasets"
UA = "powergrid-benchmark-repair/0.1"


def get(url: str, dest: Path, timeout: int = 300) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)
    print(f"OK {dest} ({dest.stat().st_size} bytes)", flush=True)


def nasa() -> None:
    dest = DATA / "battery_bms" / "nasa_pcoe_battery"
    zip_path = dest / "5._Battery_Data_Set.zip"
    if not zip_path.exists() or zip_path.stat().st_size < 1_000_000:
        print("Downloading NASA battery zip from S3...", flush=True)
        get("https://phm-datasets.s3.amazonaws.com/NASA/5.+Battery+Data+Set.zip", zip_path, timeout=600)
    cells = dest / "cells"
    cells.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path) as zf:
        names = zf.namelist()
        print(f"zip entries: {len(names)}", flush=True)
        for name in names:
            base = Path(name).name
            if base.startswith("B") and base.endswith(".mat"):
                target = cells / base
                if target.exists() and target.stat().st_size > 1000:
                    continue
                with zf.open(name) as src, target.open("wb") as out:
                    shutil.copyfileobj(src, out)
                print(f"extracted {base}", flush=True)
            if base.lower().startswith("readme") and base.lower().endswith(".txt"):
                with zf.open(name) as src, (dest / base).open("wb") as out:
                    shutil.copyfileobj(src, out)


def zenodo_file(record_id: str, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    meta_path = dest_dir / "zenodo_record.json"
    if not meta_path.exists():
        get(f"https://zenodo.org/api/records/{record_id}", meta_path, timeout=60)
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    for f in meta.get("files") or []:
        key = f.get("key") or "file.bin"
        url = (f.get("links") or {}).get("content") or (f.get("links") or {}).get("download")
        out = dest_dir / key
        if out.exists() and out.stat().st_size > 1000:
            print(f"skip existing {key}", flush=True)
            continue
        if not url:
            continue
        print(f"zenodo {record_id} -> {key}", flush=True)
        get(url, out, timeout=900)


def renewables_opsd() -> None:
    dest = DATA / "renewable_weather" / "renewables_ninja_country_sample"
    dest.mkdir(parents=True, exist_ok=True)
    # OPSD packages that wrap renewables.ninja style capacity factors
    urls = [
        (
            "opsd_time_series_60min_sample_head.csv",
            "https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv",
        ),
    ]
    # Only fetch a small head via Range when possible; otherwise skip giant CSV if already in opsd cache.
    opsd_full = DATA / "time_series_market" / "opsd_time_series" / "time_series_60min_singleindex.csv"
    note = dest / "LINKED_OPSD.md"
    note.write_text(
        "Renewables.ninja static Europe CSV URLs are no longer public at the old /static/downloads paths.\n"
        "Use https://www.renewables.ninja/ country/point UI for custom extracts.\n"
        f"Local OPSD time series cache (includes load/wind/solar columns): `{opsd_full}`\n"
        "Exists: " + str(opsd_full.exists()) + "\n",
        encoding="utf-8",
    )
    print("renewables.ninja note written; linked to OPSD cache", flush=True)


def opfdata() -> None:
    dest = DATA / "opf_benchmarks" / "opfdata_landing"
    dest.mkdir(parents=True, exist_ok=True)
    get("https://arxiv.org/pdf/2406.07234", dest / "OPFData_2406.07234.pdf", timeout=120)
    (dest / "GCS_BUCKET.md").write_text(
        "OPFData JSON files: gs://gridopt-dataset/\nUse gsutil when available.\n",
        encoding="utf-8",
    )


def acn_sessions() -> None:
    dest = DATA / "distribution_ev" / "acn_data_static" / "session data"
    dest.mkdir(parents=True, exist_ok=True)
    # Try multiple raw paths
    candidates = [
        "https://raw.githubusercontent.com/tongxin-li/ACN-Data-Static/main/session%20data/caltech_sessions.json",
        "https://raw.githubusercontent.com/tongxin-li/ACN-Data-Static/master/session%20data/caltech_sessions.json",
        "https://cdn.jsdelivr.net/gh/tongxin-li/ACN-Data-Static@main/session%20data/caltech_sessions.json",
    ]
    out = dest / "caltech_sessions.json"
    for url in candidates:
        try:
            get(url, out, timeout=120)
            if out.stat().st_size > 100:
                return
        except Exception as exc:
            print(f"ACN fail {url}: {exc}", flush=True)
    # Fallback: clone session folder via sparse again with checkout
    print("ACN session JSON still missing; keep README only", flush=True)


def m5bat_note() -> None:
    dest = DATA / "bess_grid" / "m5bat_bess"
    # Detect fake tiny downloads
    for name in ["M5BAT_04-2023_RAW.zip", "Report_04-2023.pdf", "record.html"]:
        p = dest / name
        if p.exists() and p.stat().st_size < 1000:
            p.unlink()
    (dest / "ACCESS_NOTE.md").write_text(
        "RWTH publications direct file URLs returned placeholder/error bodies (~248 bytes).\n"
        "Manual download: https://doi.org/10.18154/rwth-2024-04895 or\n"
        "https://publications.rwth-aachen.de/record/985295\n"
        "Landing HTML retained when available.\n",
        encoding="utf-8",
    )
    try:
        get("https://publications.rwth-aachen.de/record/985295", dest / "record.html", timeout=30)
    except Exception as exc:
        print(f"m5bat record html: {exc}", flush=True)


def main() -> None:
    nasa()
    zenodo_file("17494555", DATA / "bess_grid" / "finland_afrr_weather")
    zenodo_file("18199323", DATA / "bess_grid" / "bess_european_balancing_inputs")
    # Light metadata for large climate packs already have zenodo_record.json
    for rid, rel in [
        ("13937523", "renewable_weather/vce_rare_power"),
        ("20518257", "renewable_weather/eia860_wind_solar_cf"),
        ("14615500", "renewable_weather/secures_energy"),
        ("13938926", "renewable_weather/era5_eu_supply_demand"),
    ]:
        d = DATA / rel
        if not (d / "zenodo_record.json").exists():
            get(f"https://zenodo.org/api/records/{rid}", d / "zenodo_record.json", timeout=60)
        (d / "DOWNLOAD_POLICY.md").write_text(
            f"Full Zenodo record {rid} cached as metadata. "
            "Download selected files with: python -c \"...\" or Zenodo UI when disk budget allows.\n",
            encoding="utf-8",
        )
    renewables_opsd()
    opfdata()
    acn_sessions()
    m5bat_note()
    print("repair done", flush=True)


if __name__ == "__main__":
    main()
