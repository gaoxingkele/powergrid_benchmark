"""Background large dataset pulls for grid tracking gaps."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, r"D:\aicoding\mylib")
from download_tools import download

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/public_datasets/grid_tracking/datasets"
PROXY = "http://127.0.0.1:17890"
os.environ["HTTP_PROXY"] = PROXY
os.environ["HTTPS_PROXY"] = PROXY

STATUS = DATA / "large_pull_status.json"


def save(status: dict) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(status, ensure_ascii=False), flush=True)


def main() -> None:
    status: dict = {"steps": []}

    # 1) PROTECT-90 zip ~12GB
    protect_zip = DATA / "protect90" / "hv_double_line_90kv_preprocessed_data.zip"
    protect_zip.parent.mkdir(parents=True, exist_ok=True)
    url = "https://zenodo.org/api/records/18418330/files/hv_double_line_90kv_preprocessed_data.zip/content"
    print("PROTECT-90 zip...", flush=True)
    if protect_zip.exists() and protect_zip.stat().st_size > 10_000_000_000:
        status["steps"].append({"name": "protect90", "status": "exists", "bytes": protect_zip.stat().st_size})
    else:
        code = download(url, protect_zip, proxy=PROXY)
        status["steps"].append(
            {
                "name": "protect90",
                "status": "ok" if code == 0 and protect_zip.exists() else f"fail_{code}",
                "bytes": protect_zip.stat().st_size if protect_zip.exists() else 0,
            }
        )
    save(status)

    # 2) InspecSafe train/test
    from huggingface_hub import hf_hub_download

    insp = DATA / "inspecsafe_v1"
    insp.mkdir(parents=True, exist_ok=True)
    for fname in ["train.tar.gz", "test.tar.gz", "README.md", "dataset_loader.py"]:
        print("InspecSafe", fname, flush=True)
        try:
            path = hf_hub_download(
                repo_id="Tetrabot2026/InspecSafe-V1",
                repo_type="dataset",
                filename=fname,
                local_dir=str(insp),
            )
            p = Path(path)
            status["steps"].append({"name": f"inspecsafe_{fname}", "status": "ok", "bytes": p.stat().st_size})
        except Exception as exc:
            status["steps"].append({"name": f"inspecsafe_{fname}", "status": f"error:{exc}"})
        save(status)

    # 3) WindFM tokenizer
    wind_tok = DATA / "windfm" / "NeoQuasar_WindFM_Tokenizer"
    wind_tok.mkdir(parents=True, exist_ok=True)
    print("WindFM tokenizer...", flush=True)
    try:
        from huggingface_hub import snapshot_download

        snapshot_download(repo_id="NeoQuasar/WindFM-Tokenizer", local_dir=str(wind_tok))
        status["steps"].append({"name": "windfm_tokenizer", "status": "ok"})
    except Exception as exc:
        status["steps"].append({"name": "windfm_tokenizer", "status": f"error:{exc}"})
    save(status)

    # 4) SIIB-Time full snapshot (many files)
    siib = DATA / "siib_time_full"
    siib.mkdir(parents=True, exist_ok=True)
    print("SIIB-Time full snapshot...", flush=True)
    try:
        from huggingface_hub import snapshot_download

        snapshot_download(
            repo_id="neurips26-PSML/SIIB-Time",
            repo_type="dataset",
            local_dir=str(siib),
            max_workers=8,
        )
        nfiles = sum(1 for _ in siib.rglob("*") if _.is_file())
        nbytes = sum(p.stat().st_size for p in siib.rglob("*") if p.is_file())
        status["steps"].append({"name": "siib_time_full", "status": "ok", "files": nfiles, "bytes": nbytes})
    except Exception as exc:
        status["steps"].append({"name": "siib_time_full", "status": f"error:{exc}"})
    save(status)

    status["done"] = True
    save(status)
    print("ALL LARGE PULLS DONE", flush=True)


if __name__ == "__main__":
    main()
