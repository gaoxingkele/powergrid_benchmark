# -*- coding: utf-8 -*-
"""Download gap DataPort datasets via S3 (extends download_dataport_s3)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Reuse aria2 + presign helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
from download_dataport_s3 import (  # noqa: E402
    ACCESS_KEY,
    DATASETS,
    ROOT,
    SECRET_KEY,
    aria2_download,
    find_aria2,
    make_client,
    parse_s3,
)

GAP_ROOT = ROOT.parent / "gap_dataport"

# Known / discovered S3 URIs (subscriber + open-access scripts)
GAP_DATASETS: dict[str, list[str]] = {
    "irtsd_scripts": [
        "s3://ieee-dataport/open/scripts/1315848/SENT_Automation_Funcs.zip",
        "s3://ieee-dataport/open/scripts/1315848/SENT_DataLabels_LoadProfiles.zip",
        "s3://ieee-dataport/docs/1315848/README_SENT_V02_Dataset.docx",
    ],
    # Event_Data + FO + testcases: add URIs from DataPort AWS tab when discovered
    "irtsd_event_data": [],
    "fo_ksv8": [],
    "oscillation_testcases": [],
}

# Candidate Event_Data paths to probe (IRTSD dataset id 1315848 from page scrape)
_EVENT_BATCHES = [
    108991,
    97031,
    102694,
    104617,
    105078,
    101265,
    91709,
    108000,
    109000,
    110000,
    100000,
    101000,
    102000,
]


def discover_event_data_uri() -> str | None:
    if not ACCESS_KEY or not SECRET_KEY:
        return None
    client = make_client()
    for batch in _EVENT_BATCHES:
        key = f"data/1315848/{batch}/Event_Data.zip"
        try:
            sz = int(client.head_object(Bucket="ieee-dataport", Key=key)["ContentLength"])
            if sz > 1_000_000_000:
                print(f"DISCOVERED s3://ieee-dataport/{key} ({sz / 1e9:.2f} GB)", flush=True)
                return f"s3://ieee-dataport/{key}"
        except Exception:
            continue
    for batch in _EVENT_BATCHES:
        key = f"data/1315848/{batch}/PSCAD.zip"
        try:
            client.head_object(Bucket="ieee-dataport", Key=key)
            uri = f"s3://ieee-dataport/{key}"
            print(f"DISCOVERED {uri}", flush=True)
            GAP_DATASETS.setdefault("irtsd_scripts", []).append(uri)
        except Exception:
            continue
    return None


def discover_fo_and_testcases() -> None:
    if not ACCESS_KEY or not SECRET_KEY:
        return
    client = make_client()
    targets = {
        "fo_ksv8": ["FO_datasets.zip", "FO_Datasets.zip"],
        "oscillation_testcases": [
            "14bus_data_PoW.zip",
            "WECC179_model_and_data.zip",
            "WECC240_model_and_data.zip",
            "ISO-NE_data.zip",
        ],
    }
    # Quick scan recent data ids (2025-2026 uploads)
    for dsid in range(1520000, 1680000, 800):
        prefix = f"data/{dsid}/"
        try:
            resp = client.list_objects_v2(Bucket="ieee-dataport", Prefix=prefix, MaxKeys=30)
        except Exception:
            continue
        for obj in resp.get("Contents", []):
            name = obj["Key"].split("/")[-1]
            for group, names in targets.items():
                if name in names and not GAP_DATASETS.get(group):
                    uri = f"s3://ieee-dataport/{obj['Key']}"
                    print(f"DISCOVERED {group}: {uri}", flush=True)
                    GAP_DATASETS[group] = [uri]


def main() -> int:
    if not ACCESS_KEY or not SECRET_KEY:
        print("ERROR: set AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY", flush=True)
        return 2

    event_uri = discover_event_data_uri()
    if event_uri:
        GAP_DATASETS["irtsd_event_data"] = [event_uri]
    discover_fo_and_testcases()

    aria2 = find_aria2()
    client = make_client()
    fails: list[str] = []

    for name, uris in GAP_DATASETS.items():
        if not uris:
            print(f"SKIP empty {name} (no S3 URI — copy from DataPort AWS tab)", flush=True)
            continue
        dest_dir = GAP_ROOT / name
        for uri in uris:
            bucket, key = parse_s3(uri)
            remote = int(client.head_object(Bucket=bucket, Key=key)["ContentLength"])
            dest = dest_dir / Path(key).name
            url = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": key},
                ExpiresIn=7 * 24 * 3600,
            )
            try:
                aria2_download(aria2, url, dest, remote)
            except Exception as exc:
                print(f"FAIL {dest.name}: {exc}", flush=True)
                fails.append(f"{uri} :: {exc}")

    print(f"SUMMARY fail={len(fails)}", flush=True)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
