"""Continue open-data acquisition for remaining incomplete sources.

Uses aria2+proxy for large/HTTP downloads when available.
"""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import zipfile
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "public_datasets"
MANIFEST = DATA / "manifests" / "public_dataset_manifest.csv"
CACHE = DATA / "CACHE_STATUS.md"
PROXY = "http://127.0.0.1:17890"
ARIA2 = Path(r"C:\Users\10175\AppData\Local\aria2\aria2-1.37.0-win-64bit-build1\aria2c.exe")


def aria2(url: str, dest: Path, expected: int | None = None) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if expected and dest.exists() and dest.stat().st_size >= expected:
        print(f"skip complete {dest.name} ({dest.stat().st_size})", flush=True)
        return True
    if not ARIA2.exists():
        raise FileNotFoundError(ARIA2)
    cmd = [
        str(ARIA2),
        f"--all-proxy={PROXY}",
        "--check-certificate=false",
        "--split=16",
        "--max-connection-per-server=16",
        "--min-split-size=1M",
        "--continue=true",
        "--file-allocation=none",
        "--max-tries=0",
        "--retry-wait=5",
        "--timeout=60",
        "--connect-timeout=30",
        "--auto-file-renaming=false",
        "--allow-overwrite=true",
        f"--dir={dest.parent}",
        f"--out={dest.name}",
        url,
    ]
    print("RUN", " ".join(cmd), flush=True)
    code = subprocess.call(cmd)
    ok = code == 0 and dest.exists() and (expected is None or dest.stat().st_size >= expected * 0.99)
    print(f"{'OK' if ok else 'FAIL'} {dest} size={dest.stat().st_size if dest.exists() else 0}", flush=True)
    return ok


def write_readme(path: Path, title: str, body: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / "README.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")


def fetch_m5bat() -> str:
    dest = DATA / "bess_grid" / "m5bat_bess"
    # Correct RWTH record id is 985923 (not 985295)
    ok1 = aria2(
        "https://publications.rwth-aachen.de/record/985923/files/M5BAT_04-2023_RAW.zip",
        dest / "M5BAT_04-2023_RAW.zip",
        expected=97_000_000,
    )
    ok2 = aria2(
        "https://publications.rwth-aachen.de/record/985923/files/Report_04-2023.pdf",
        dest / "Report_04-2023.pdf",
        expected=1_000_000,
    )
    aria2(
        "https://publications.rwth-aachen.de/record/985923",
        dest / "record.html",
    )
    write_readme(
        dest,
        "m5bat_bess",
        f"- Source record: https://publications.rwth-aachen.de/record/985923\n"
        f"- DOI: https://doi.org/10.18154/rwth-2024-04895\n"
        f"- RAW zip: {'ok' if ok1 else 'failed'}\n"
        f"- Report pdf: {'ok' if ok2 else 'failed'}\n",
    )
    return "downloaded" if ok1 else ("partial" if ok2 else "failed")


def fetch_acn_static() -> str:
    dest = DATA / "distribution_ev" / "acn_data_static"
    dest.mkdir(parents=True, exist_ok=True)
    # Full repo zip (~time-series csv.gz). Prefer GitHub codeload.
    zip_path = dest / "ACN-Data-Static-main.zip"
    ok = aria2(
        "https://codeload.github.com/tongxin-li/ACN-Data-Static/zip/refs/heads/main",
        zip_path,
    )
    if ok and zip_path.exists() and zip_path.stat().st_size > 1_000_000:
        extract_dir = dest / "_extract"
        if extract_dir.exists():
            shutil.rmtree(extract_dir, ignore_errors=True)
        extract_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path) as zf:
            # Extract README + a limited sample of time-series to keep disk sane,
            # plus all session data; if zip is manageable extract all.
            names = zf.namelist()
            total = sum(zi.file_size for zi in zf.infolist())
            print(f"ACN zip entries={len(names)} uncompressed≈{total/1e9:.2f}GB", flush=True)
            if total < 8e9:
                zf.extractall(extract_dir)
                # flatten one level
                inner = next(extract_dir.iterdir())
                for child in inner.iterdir():
                    target = dest / child.name
                    if target.exists():
                        if target.is_dir():
                            shutil.rmtree(target, ignore_errors=True)
                        else:
                            target.unlink()
                    shutil.move(str(child), str(target))
                shutil.rmtree(extract_dir, ignore_errors=True)
                status = "downloaded"
            else:
                # Extract README + first 200 csv.gz as sample + any json
                keep = 0
                for name in names:
                    base = Path(name).name
                    if base in {"README.md"} or name.endswith(".json") or (
                        name.endswith(".csv.gz") and keep < 200
                    ):
                        zf.extract(name, extract_dir)
                        if name.endswith(".csv.gz"):
                            keep += 1
                status = "partial"
        write_readme(
            dest,
            "acn_data_static",
            f"- GitHub zip: {zip_path} ({zip_path.stat().st_size} bytes)\n"
            f"- Note: session data/caltech_sessions.json is empty upstream; use time-series dirs.\n"
            f"- Status: {status}\n",
        )
        return status
    # Fallback: sparse git for caltech folder only
    if (dest / ".git").exists():
        shutil.rmtree(dest / ".git", ignore_errors=True)
    work = dest / "_sparse"
    if work.exists():
        shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    subprocess.run(["git", "init"], cwd=work, check=True)
    subprocess.run(["git", "remote", "add", "origin", "https://github.com/tongxin-li/ACN-Data-Static.git"], cwd=work, check=True)
    subprocess.run(["git", "config", "core.sparseCheckout", "true"], cwd=work, check=True)
    (work / ".git" / "info" / "sparse-checkout").write_text(
        "README.md\ncaltech/\njpl/\noffice_01/\nsession data/\n",
        encoding="utf-8",
    )
    pull = subprocess.run(
        ["git", "pull", "--depth", "1", "origin", "main"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    if pull.returncode == 0:
        for child in work.iterdir():
            if child.name == ".git":
                continue
            target = dest / child.name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target, ignore_errors=True)
                else:
                    target.unlink()
            shutil.move(str(child), str(target))
        write_readme(dest, "acn_data_static", "Sparse git pull of site folders completed.\n")
        return "downloaded"
    write_readme(dest, "acn_data_static", f"codeload+sparse failed: {pull.stderr}\n")
    return "failed"


def fetch_nasa_recommissioned() -> str:
    dest = DATA / "battery_bms" / "nasa_randomized_recommissioned_battery"
    dest.mkdir(parents=True, exist_ok=True)
    # Try known PHM S3 style / data.nasa.gov landing; official note said unavailable.
    candidates = [
        ("landing.html", "https://data.nasa.gov/dataset/randomized-and-recommissioned-battery-dataset"),
        ("dataset.json", "https://data.nasa.gov/api/views/xg3n-ngei.json"),
        # community mirrors if any appear later
    ]
    ok_meta = False
    for name, url in candidates:
        try:
            if aria2(url, dest / name):
                ok_meta = True
        except Exception as exc:
            print(f"nasa recommissioned {name}: {exc}", flush=True)
    # Attempt PHM naming guess (may 404)
    guess = "https://phm-datasets.s3.amazonaws.com/NASA/21.+Accelerated+Battery+Life+Testing.zip"
    got = aria2(guess, dest / "Accelerated_Battery_Life_Testing.zip")
    write_readme(
        dest,
        "nasa_randomized_recommissioned_battery",
        "- Official note: direct download may be unavailable; contact christopher.a.teubert@nasa.gov\n"
        f"- Metadata cached: {ok_meta}\n"
        f"- S3 guess download: {got}\n",
    )
    return "downloaded" if got else ("metadata-only" if ok_meta else "failed")


def fetch_pglearn() -> str:
    dest = DATA / "opf_benchmarks" / "pglearn_small"
    dest.mkdir(parents=True, exist_ok=True)
    try:
        from huggingface_hub import hf_hub_download, list_repo_files, snapshot_download
    except Exception as exc:
        write_readme(dest, "pglearn_small", f"huggingface_hub missing: {exc}\n")
        return "failed"

    # Prefer a small representative system with parquet/json samples
    repos = ["PGLearn/14_ieee", "PGLearn/30_ieee", "PGLearn/118_ieee"]
    downloaded = []
    for repo in repos:
        try:
            files = list_repo_files(repo, repo_type="dataset")
            (dest / f"{repo.split('/')[-1]}_filelist.json").write_text(
                json.dumps(files, indent=2), encoding="utf-8"
            )
            # Download up to ~500MB worth of preferred files
            preferred = [
                f
                for f in files
                if f.endswith((".parquet", ".json", ".csv", ".md", ".txt", ".npz"))
            ]
            local = dest / repo.split("/")[-1]
            local.mkdir(parents=True, exist_ok=True)
            budget = 500 * 1024 * 1024
            used = 0
            for f in preferred:
                if used >= budget:
                    break
                print(f"hf {repo}:{f}", flush=True)
                path = hf_hub_download(
                    repo_id=repo,
                    filename=f,
                    repo_type="dataset",
                    local_dir=str(local),
                )
                used += Path(path).stat().st_size
                downloaded.append(f"{repo}:{f}")
        except Exception as exc:
            print(f"pglearn {repo} failed: {exc}", flush=True)
    write_readme(
        dest,
        "pglearn_small",
        "HuggingFace PGLearn small-system subsets.\n\nDownloaded:\n"
        + "\n".join(f"- {x}" for x in downloaded[:50])
        + f"\n\nTotal entries: {len(downloaded)}\n",
    )
    return "downloaded" if downloaded else "partial"


def fetch_renewables_ninja() -> str:
    dest = DATA / "renewable_weather" / "renewables_ninja_country_sample"
    dest.mkdir(parents=True, exist_ok=True)
    # OPSD national generation capacity / renewables.ninja related packages
    urls = [
        (
            "opsd_renewable_power_plants_DE.csv",
            "https://data.open-power-system-data.org/renewable_power_plants/2020-08-25/renewable_power_plants_DE.csv",
        ),
        (
            "opsd_national_generation_capacity.csv",
            "https://data.open-power-system-data.org/national_generation_capacity/2020-10-01/national_generation_capacity.csv",
        ),
        (
            "opsd_weather_data_README.md",
            "https://data.open-power-system-data.org/weather_data/2020-09-16/README.md",
        ),
    ]
    ok = 0
    for name, url in urls:
        if aria2(url, dest / name):
            # reject tiny error pages
            if (dest / name).stat().st_size > 500:
                ok += 1
    # Link note to already-cached OPSD time series (contains wind/solar columns)
    opsd = DATA / "time_series_market" / "opsd_time_series" / "time_series_60min_singleindex.csv"
    (dest / "LINKED_OPSD.md").write_text(
        f"Country capacity-factor extracts from renewables.ninja UI require interactive download.\n"
        f"Linked local OPSD hourly series with wind/solar fields: `{opsd}` exists={opsd.exists()}.\n",
        encoding="utf-8",
    )
    write_readme(dest, "renewables_ninja_country_sample", f"OPSD-related open packages cached: {ok}\n")
    return "downloaded" if ok >= 2 else ("partial" if ok else "metadata-only")


def fetch_battery_archive() -> str:
    dest = DATA / "battery_bms" / "battery_archive"
    dest.mkdir(parents=True, exist_ok=True)
    pages = [
        ("index.html", "https://batteryarchive.org/"),
        ("study_summaries.html", "https://batteryarchive.org/study_summaries.html"),
        ("about.html", "https://www.batteryarchive.org/about.html"),
    ]
    ok = 0
    for name, url in pages:
        if aria2(url, dest / name) and (dest / name).stat().st_size > 500:
            ok += 1
    write_readme(
        dest,
        "battery_archive",
        "Catalogue portal cached. Individual study CSV downloads require accepting site terms in browser.\n"
        f"Pages: {ok}\n",
    )
    return "metadata-only"


def upsert_status(updates: dict[str, str]) -> None:
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    fields = list(rows[0].keys())
    by = {r["dataset_id"]: r for r in rows}
    for did, status in updates.items():
        if did in by:
            by[did]["status"] = status
            # fix m5bat source url if needed
            if did == "m5bat_bess":
                by[did]["source_url"] = "https://publications.rwth-aachen.de/record/985923"
                by[did]["notes"] = (
                    "M5BAT field BESS Apr 2023 RAW+report; RWTH record 985923 / DOI 10.18154/rwth-2024-04895"
                )
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(by.values())

    # refresh CACHE extension section lightly
    downloaded = sum(1 for r in by.values() if r["status"] == "downloaded")
    partial = sum(1 for r in by.values() if r["status"] == "partial")
    meta = sum(1 for r in by.values() if r["status"] == "metadata-only")
    lines = [
        "# Public Dataset Cache Status",
        "",
        f"更新日期: {date.today().isoformat()}",
        "",
        "## Summary",
        "",
        f"- Manifest rows: {len(by)}",
        f"- Downloaded/cache-ready: {downloaded}",
        f"- Partial: {partial}",
        f"- Metadata-only/API-ready: {meta}",
        "",
        "## Zenodo download policy",
        "",
        "Zenodo 大文件唯一可靠方案：`python scripts/data_acquisition/download_zenodo_aria2.py`",
        "",
        "```text",
        "aria2c --all-proxy=http://127.0.0.1:17890 --split=16 --max-connection-per-server=16 --continue=true --file-allocation=none",
        "```",
        "",
        "## Recent continuation",
        "",
        f"- Updates: {updates}",
        "",
        "## Verification",
        "",
        "```powershell",
        "python scripts/data_acquisition/audit_public_datasets.py",
        "```",
        "",
    ]
    CACHE.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    updates: dict[str, str] = {}
    print("== m5bat", flush=True)
    updates["m5bat_bess"] = fetch_m5bat()
    print("== acn", flush=True)
    updates["acn_data_static"] = fetch_acn_static()
    print("== nasa recommissioned", flush=True)
    updates["nasa_randomized_recommissioned_battery"] = fetch_nasa_recommissioned()
    print("== pglearn", flush=True)
    updates["pglearn_small"] = fetch_pglearn()
    print("== renewables.ninja/opsd", flush=True)
    updates["renewables_ninja_country_sample"] = fetch_renewables_ninja()
    print("== battery archive", flush=True)
    updates["battery_archive"] = fetch_battery_archive()
    upsert_status(updates)
    print("=== DONE ===", updates, flush=True)


if __name__ == "__main__":
    main()
