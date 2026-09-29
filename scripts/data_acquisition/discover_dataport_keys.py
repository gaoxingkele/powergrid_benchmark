# -*- coding: utf-8 -*-
"""Discover IEEE DataPort S3 keys by scanning dataset ID prefixes."""
from __future__ import annotations

import os
import sys

import boto3
from botocore.config import Config

NEEDLES = (
    "fo_dataset",
    "event_data",
    "14bus",
    "wecc179",
    "wecc240",
    "iso-ne",
    "pow",
    "sent_",
    "pscad",
)


def main() -> int:
    for k in list(os.environ):
        if "proxy" in k.lower():
            os.environ.pop(k, None)
    ak = os.environ.get("DATAPORT_AWS_ACCESS_KEY_ID") or os.environ.get("AWS_ACCESS_KEY_ID")
    sk = os.environ.get("DATAPORT_AWS_SECRET_ACCESS_KEY") or os.environ.get("AWS_SECRET_ACCESS_KEY")
    if not ak or not sk:
        print("missing AWS keys", flush=True)
        return 2

    s3 = boto3.session.Session(aws_access_key_id=ak, aws_secret_access_key=sk).client(
        "s3",
        config=Config(region_name="us-east-1", signature_version="s3v4", retries={"max_attempts": 3}),
    )

    start = int(sys.argv[1]) if len(sys.argv) > 1 else 2300000
    end = int(sys.argv[2]) if len(sys.argv) > 2 else 2700000
    step = int(sys.argv[3]) if len(sys.argv) > 3 else 10000

    for dsid in range(start, end, step):
        prefix = f"data/{dsid}/"
        try:
            r = s3.list_objects_v2(Bucket="ieee-dataport", Prefix=prefix, MaxKeys=50)
        except Exception as exc:
            print(f"ERR list {prefix}: {exc}", flush=True)
            continue
        for obj in r.get("Contents", []):
            key = obj["Key"]
            low = key.lower()
            if any(n in low for n in NEEDLES):
                print(f"s3://ieee-dataport/{key}  {obj['Size']}", flush=True)
            elif key.endswith(".zip") or key.endswith(".7z"):
                print(f"ZIP s3://ieee-dataport/{key}  {obj['Size']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
