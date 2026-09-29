# -*- coding: utf-8 -*-
"""Download IEEE DataPort via presigned S3 URLs + aria2c (proxy, multi-conn, resume)."""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import boto3
from botocore.config import Config

ACCESS_KEY = os.environ.get("DATAPORT_AWS_ACCESS_KEY_ID") or os.environ.get(
    "AWS_ACCESS_KEY_ID", ""
)
SECRET_KEY = os.environ.get("DATAPORT_AWS_SECRET_ACCESS_KEY") or os.environ.get(
    "AWS_SECRET_ACCESS_KEY", ""
)

ROOT = Path(
    r"F:\aicoding\powergrid_benchmark\data\public_datasets\grid_tracking\datasets\dataport"
)

ARIA2_CANDIDATES = [
    Path(r"C:\Users\10175\AppData\Local\aria2\aria2-1.37.0-win-64bit-build1\aria2c.exe"),
    Path(r"C:\Users\10175\AppData\Local\aria2c.exe"),
    Path(r"C:\Program Files\Netease\GameViewer\bin\aria2c.exe"),
]

PROXY = os.environ.get("DATAPORT_PROXY", "http://127.0.0.1:17890")
PRESIGN_EXPIRES = int(os.environ.get("DATAPORT_PRESIGN_EXPIRES", str(7 * 24 * 3600)))

DATASETS: dict[str, list[str]] = {
    "dpsyor": [
        "s3://ieee-dataport/competition/1455930/102694/Scenario_1_tieline_fault.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_1_generatordisconnect.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_2_generatordisconnect.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_3_generatordisconnect.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_1_generatordisconect_tielinefault.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_2_generatordisconnect_tielinefault.zip",
        "s3://ieee-dataport/competition/1455930/102694/Scenario_4_generatordisconect_tielinefault.zip",
        "s3://ieee-dataport/competition/1455930/102694/1996_Gov.7z",
        "s3://ieee-dataport/competition/1455930/102694/1996_Ex.7z",
    ],
    "dpsyfor": [
        "s3://ieee-dataport/data/1421872/97031/Large-WECC-Governor-Cases.7z",
        "s3://ieee-dataport/data/1421872/97031/Large-WECC-Exciter Cases.7z",
        "s3://ieee-dataport/data/1421872/97031/Mini-WECC-Case-4.7z",
        "s3://ieee-dataport/data/1421872/97031/Mini-WECC-Case-2.7z",
        "s3://ieee-dataport/data/1421872/97031/Mini-WECC-Case-3.7z",
    ],
    "ieee9_tsa": [
        "s3://ieee-dataport/data/1312450/108991/case_IEEE9BusSystem_dataset_0.mat",
    ],
}


def find_aria2() -> Path:
    for p in ARIA2_CANDIDATES:
        if p.is_file():
            return p
    which = subprocess.run(["where", "aria2c"], capture_output=True, text=True)
    if which.returncode == 0:
        line = which.stdout.strip().splitlines()[0]
        return Path(line)
    raise FileNotFoundError("aria2c not found")


def parse_s3(uri: str) -> tuple[str, str]:
    rest = uri[5:]
    bucket, key = rest.split("/", 1)
    return bucket, key


def make_client():
    # Presign should not go through broken proxy paths for signing; client can be direct.
    for k in list(os.environ):
        if "proxy" in k.lower():
            os.environ.pop(k, None)
    cfg = Config(
        region_name=os.environ.get("AWS_DEFAULT_REGION", "us-east-1"),
        signature_version="s3v4",
        retries={"max_attempts": 10, "mode": "adaptive"},
    )
    return boto3.session.Session(
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    ).client("s3", config=cfg)


def aria2_download(aria2: Path, url: str, dest: Path, remote_size: int) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size == remote_size and remote_size > 0:
        print(f"SKIP {dest.name} ({remote_size / (1024**3):.2f} GiB)", flush=True)
        return 0

    # Drop incomplete random boto temps; keep aria2 .aria2 control for resume.
    for p in dest.parent.glob(dest.name + ".part*"):
        try:
            p.unlink()
        except OSError:
            pass

    cmd = [
        str(aria2),
        f"--all-proxy={PROXY}",
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
    print(f"ARIA2 {dest.name} ({remote_size / (1024**3):.2f} GiB)", flush=True)
    t0 = time.time()
    proc = subprocess.run(cmd)
    # aria2 sometimes exits non-zero after SSL hiccups even when file is complete.
    if dest.exists() and dest.stat().st_size == remote_size and remote_size > 0:
        aria_ctl = Path(str(dest) + ".aria2")
        aria_ctl.unlink(missing_ok=True)
        dt = time.time() - t0
        speed = remote_size / max(dt, 1e-6)
        print(
            f"DONE {dest.name} in {dt / 60:.1f} min ({speed / (1024**2):.1f} MiB/s)"
            + (f" (aria2 exit {proc.returncode})" if proc.returncode else ""),
            flush=True,
        )
        return 0
    if proc.returncode != 0:
        raise RuntimeError(f"aria2c exit {proc.returncode} for {dest.name}")
    raise RuntimeError(
        f"size mismatch {dest.name}: local="
        f"{dest.stat().st_size if dest.exists() else -1} remote={remote_size}"
    )


def main() -> int:
    if not ACCESS_KEY or not SECRET_KEY:
        print("ERROR: set AWS keys", flush=True)
        return 2

    aria2 = find_aria2()
    print(f"aria2c={aria2}", flush=True)
    print(f"proxy={PROXY}", flush=True)

    client = make_client()
    try:
        sts = boto3.client(
            "sts",
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
            region_name="us-east-1",
        )
        print(f"STS: {sts.get_caller_identity().get('Arn')}", flush=True)
    except Exception as exc:
        print(f"WARN sts: {exc}", flush=True)

    only = [a for a in sys.argv[1:] if not a.startswith("-")]
    jobs: list[tuple[str, Path, int]] = []
    for ds, uris in DATASETS.items():
        if only and ds not in only:
            continue
        for uri in uris:
            bucket, key = parse_s3(uri)
            sz = int(client.head_object(Bucket=bucket, Key=key)["ContentLength"])
            jobs.append((uri, ROOT / ds / Path(key).name, sz))
    jobs.sort(key=lambda x: x[2])

    print(f"Jobs={len(jobs)} total={sum(j[2] for j in jobs)/(1024**3):.1f} GiB", flush=True)

    fails: list[str] = []
    for uri, dest, sz in jobs:
        bucket, key = parse_s3(uri)
        try:
            url = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=PRESIGN_EXPIRES,
            )
            aria2_download(aria2, url, dest, sz)
        except Exception as exc:
            print(f"FAIL {dest.name}: {exc}", flush=True)
            fails.append(f"{uri} :: {exc}")

    print(f"SUMMARY fail={len(fails)}/{len(jobs)}", flush=True)
    for f in fails:
        print(f"  {f}", flush=True)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
