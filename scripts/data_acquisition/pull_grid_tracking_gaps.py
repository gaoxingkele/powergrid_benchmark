# -*- coding: utf-8 -*-
"""Download gap-fill datasets (grid tracking batch 2026-08-28)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download  # noqa: E402

PROXY = "http://127.0.0.1:17890"
DATA = ROOT / "data/public_datasets/grid_tracking/datasets"
OPF = ROOT / "data/public_datasets/opf_benchmarks"
CARBON = DATA / "carbonx"
OGE = DATA / "open_grid_emissions"
UTK = DATA / "oscillation_testcases_utk"
STATUS_PATH = DATA / "gap_pull_status.json"


def save(status: dict) -> None:
    STATUS_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATUS_PATH.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(status, ensure_ascii=False), flush=True)


def bytes_of(path: Path) -> int:
    if not path.exists():
        return 0
    if path.is_file():
        return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def zenodo_file(record_id: int, key: str, dest: Path) -> dict:
    import urllib.request

    api = f"https://zenodo.org/api/records/{record_id}"
    req = urllib.request.Request(api, headers={"User-Agent": "powergrid-benchmark-gap/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        rec = json.loads(resp.read().decode())
    url = None
    size = 0
    for f in rec.get("files") or []:
        if f.get("key") == key:
            url = (f.get("links") or {}).get("self")
            size = int(f.get("size") or 0)
            break
    if not url:
        return {"key": key, "status": "missing_in_record", "bytes": 0}
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size == size and size > 0:
        return {"key": key, "status": "exists", "bytes": dest.stat().st_size, "path": str(dest)}
    code = download(url, dest, proxy=PROXY, use_aria2=True, fallback=True)
    ok = dest.exists() and dest.stat().st_size > 0
    return {
        "key": key,
        "status": "ok" if code == 0 and ok else f"fail_{code}",
        "bytes": dest.stat().st_size if ok else 0,
        "path": str(dest),
    }


def hf_pglearn_full() -> dict:
    from huggingface_hub import snapshot_download

    dest = OPF / "pglearn_small" / "PGLearn-Small-14_ieee_full"
    dest.mkdir(parents=True, exist_ok=True)
    before = bytes_of(dest)
    snapshot_download(
        repo_id="PGLearn/PGLearn-Small-14_ieee",
        repo_type="dataset",
        local_dir=str(dest),
        max_workers=8,
    )
    after = bytes_of(dest)
    return {
        "name": "pglearn_14_ieee_full",
        "status": "ok",
        "bytes_before": before,
        "bytes": after,
        "path": str(dest),
    }


def copy_carbonx() -> dict:
    src = ROOT / "data/public_datasets/grid_tracking/code/PG-T11/CarbonX/data"
    CARBON.mkdir(parents=True, exist_ok=True)
    for sub in ["forecasting-data", "imputation-data"]:
        s = src / sub
        d = CARBON / sub
        if not s.is_dir():
            continue
        if d.exists():
            shutil.rmtree(d)
        shutil.copytree(s, d)
    meta = {
        "source": "grid_tracking/code/PG-T11/CarbonX/data",
        "note": "Curated CI CSVs bundled with CarbonX repo (not China provincial).",
    }
    (CARBON / "README.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return {"name": "carbonx_csv", "status": "ok", "bytes": bytes_of(CARBON), "path": str(CARBON)}


def utk_downloads() -> list[dict]:
    items = [
        (
            "wecc240_contest_all_cases",
            "http://web.eecs.utk.edu/~kaisun/Oscillation/download/All_cases.zip",
        ),
        (
            "wecc179_simulated_pmu",
            "http://web.eecs.utk.edu/~kaisun/Oscillation/download/TestCasesLibrary_Measurement.zip",
        ),
        (
            "wecc179_models",
            "http://web.eecs.utk.edu/~kaisun/Oscillation/download/TestCasesLibrary_Model.zip",
        ),
    ]
    out = []
    UTK.mkdir(parents=True, exist_ok=True)
    for name, url in items:
        dest = UTK / name
        if not str(dest).endswith(".zip"):
            dest = dest.with_suffix(".zip")
        print(f"UTK {name}", flush=True)
        if dest.exists() and dest.stat().st_size > 1_000_000:
            out.append({"name": name, "status": "exists", "bytes": dest.stat().st_size, "path": str(dest)})
            continue
        # UTK host often blocks or slows via local proxy; try direct first.
        code = download(url, dest, proxy=None, use_aria2=True, fallback=True)
        if code != 0 or not dest.exists() or dest.stat().st_size < 100_000:
            code = download(url, dest, proxy=PROXY, use_aria2=True, fallback=True)
        ok = dest.exists() and dest.stat().st_size > 100_000
        out.append(
            {
                "name": name,
                "status": "ok" if code == 0 and ok else f"fail_{code}",
                "bytes": dest.stat().st_size if dest.exists() else 0,
                "path": str(dest),
            }
        )
    return out


def opfdata_case14_sample() -> dict:
    """Try public GCS sample for OPFData case14 (small); skip if unavailable."""
    dest = OPF / "opfdata_case14_sample"
    dest.mkdir(parents=True, exist_ok=True)
    marker = dest / "FETCH_NOTE.txt"
    urls = [
        "https://storage.googleapis.com/gridopt-dataset/case14.tar.gz",
        "https://storage.googleapis.com/gridopt-dataset/v0/case14.tar.gz",
        "https://storage.googleapis.com/gridopt-dataset/OPFData/case14.tar.gz",
    ]
    tar = dest / "case14.tar.gz"
    for url in urls:
        print(f"OPFData try {url}", flush=True)
        code = download(url, tar, proxy=PROXY, use_aria2=True, fallback=True)
        if tar.exists() and tar.stat().st_size > 10_000_000:
            return {
                "name": "opfdata_case14",
                "status": "ok",
                "bytes": tar.stat().st_size,
                "path": str(tar),
                "url": url,
            }
    marker.write_text(
        "Public GCS paths probed failed. Full bucket: gs://gridopt-dataset/ (install gcloud).\n",
        encoding="utf-8",
    )
    return {"name": "opfdata_case14", "status": "gcs_probe_failed", "path": str(marker)}


def dataport_gap_batch() -> list[dict]:
    """Run extended DataPort S3 download if URIs are configured."""
    script = ROOT / "scripts/data_acquisition/download_dataport_gap_s3.py"
    if not script.is_file():
        return [{"name": "dataport_gap", "status": "script_missing"}]
    env = os.environ.copy()
    env["DATAPORT_AWS_ACCESS_KEY_ID"] = env.get("AWS_ACCESS_KEY_ID", "")
    env["DATAPORT_AWS_SECRET_ACCESS_KEY"] = env.get("AWS_SECRET_ACCESS_KEY", "")
    proc = subprocess.run([sys.executable, str(script)], env=env, capture_output=True, text=True)
    print(proc.stdout, flush=True)
    if proc.returncode != 0:
        print(proc.stderr, flush=True)
    return [
        {
            "name": "dataport_gap_s3",
            "status": "ok" if proc.returncode == 0 else f"fail_{proc.returncode}",
            "log_tail": (proc.stdout or proc.stderr or "")[-2000:],
        }
    ]


def main() -> int:
    status: dict = {"started": time.strftime("%Y-%m-%dT%H:%M:%S"), "steps": []}

    # OGE: recent 3 years outputs (~3.8 GB)
    OGE.mkdir(parents=True, exist_ok=True)
    for year, key in [(2023, "outputs_2023.zip"), (2024, "outputs_2024.zip"), (2025, "outputs_2025.zip")]:
        print(f"OGE {key}", flush=True)
        row = zenodo_file(22052851, key, OGE / key)
        row["name"] = f"oge_{year}"
        status["steps"].append(row)
        save(status)

    print("PGLearn full", flush=True)
    status["steps"].append(hf_pglearn_full())
    save(status)

    print("CarbonX copy", flush=True)
    status["steps"].append(copy_carbonx())
    save(status)

    print("UTK oscillation", flush=True)
    status["steps"].extend(utk_downloads())
    save(status)

    print("OPFData probe", flush=True)
    status["steps"].append(opfdata_case14_sample())
    save(status)

    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        print("DataPort gap S3", flush=True)
        status["steps"].extend(dataport_gap_batch())
        save(status)

    status["done"] = True
    status["finished"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    save(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
