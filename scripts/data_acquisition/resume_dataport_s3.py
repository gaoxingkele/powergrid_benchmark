# -*- coding: utf-8 -*-
"""Resume DataPort downloads: Range-finish partials, aria2 for empty/large remainders."""
from __future__ import annotations

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# Keys must already be in env before importing sibling (it reads them at import).
from download_dataport_s3 import (  # noqa: E402
    ACCESS_KEY,
    DATASETS,
    PROXY,
    ROOT,
    SECRET_KEY,
    aria2_download,
    find_aria2,
    make_client,
    parse_s3,
)

CHUNK = 16 * 1024 * 1024


def clear_proxy() -> None:
    for k in list(os.environ):
        if "proxy" in k.lower():
            os.environ.pop(k, None)


def finish_partial(client, uri: str, dest: Path) -> None:
    bucket, key = parse_s3(uri)
    remote = int(client.head_object(Bucket=bucket, Key=key)["ContentLength"])
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and dest.stat().st_size > remote:
        with open(dest, "r+b") as f:
            f.truncate(remote)

    if dest.exists() and dest.stat().st_size == remote:
        print(f"SKIP {dest.name}", flush=True)
        Path(str(dest) + ".aria2").unlink(missing_ok=True)
        return

    have = dest.stat().st_size if dest.exists() else 0
    print(
        f"RANGE {dest.name}: {have / (1024**3):.2f}/{remote / (1024**3):.2f} GiB",
        flush=True,
    )
    t0 = time.time()
    last = t0
    start_have = have
    pos = have
    mode = "r+b" if dest.exists() else "wb"
    with open(dest, mode) as f:
        if mode == "r+b":
            f.seek(have)
        while pos < remote:
            end = min(pos + CHUNK - 1, remote - 1)
            resp = client.get_object(
                Bucket=bucket, Key=key, Range=f"bytes={pos}-{end}"
            )
            data = resp["Body"].read()
            if len(data) != end - pos + 1:
                raise RuntimeError(
                    f"short read {len(data)} != {end - pos + 1} at {pos}"
                )
            f.write(data)
            pos += len(data)
            now = time.time()
            if now - last >= 10 or pos >= remote:
                speed = (pos - start_have) / max(now - t0, 1e-6)
                print(
                    f"PROG {dest.name}: {pos / (1024**3):.2f}/{remote / (1024**3):.2f} "
                    f"({100 * pos / remote:.1f}%) {speed / (1024**2):.1f} MiB/s",
                    flush=True,
                )
                last = now
    Path(str(dest) + ".aria2").unlink(missing_ok=True)
    if dest.stat().st_size != remote:
        raise RuntimeError(
            f"size mismatch {dest.name}: {dest.stat().st_size} != {remote}"
        )
    print(f"DONE {dest.name}", flush=True)


def main() -> int:
    if not ACCESS_KEY or not SECRET_KEY:
        print("ERROR: missing AWS keys in env", flush=True)
        return 2

    clear_proxy()
    client = make_client()
    aria2 = find_aria2()
    print(f"aria2c={aria2}", flush=True)

    jobs: list[tuple[str, Path, int, int]] = []
    for ds, uris in DATASETS.items():
        for uri in uris:
            bucket, key = parse_s3(uri)
            remote = int(client.head_object(Bucket=bucket, Key=key)["ContentLength"])
            dest = ROOT / ds / Path(key).name
            local = dest.stat().st_size if dest.exists() else 0
            if local != remote:
                jobs.append((uri, dest, remote, local))
    jobs.sort(key=lambda x: x[2] - x[3])

    print(
        f"Pending={len(jobs)} remain_GiB={sum(r - l for _, _, r, l in jobs) / (1024**3):.2f}",
        flush=True,
    )
    fails: list[str] = []
    for uri, dest, remote, local in jobs:
        remain = remote - local
        try:
            if local > 0 and (local > remote * 0.3 or remain < 8 * 1024**3):
                clear_proxy()
                finish_partial(make_client(), uri, dest)
            else:
                clear_proxy()
                bucket, key = parse_s3(uri)
                url = make_client().generate_presigned_url(
                    "get_object",
                    Params={"Bucket": bucket, "Key": key},
                    ExpiresIn=7 * 24 * 3600,
                )
                aria2_download(aria2, url, dest, remote)
        except Exception as exc:
            print(f"FAIL {dest.name}: {exc}", flush=True)
            fails.append(f"{uri} :: {exc}")

    print(f"SUMMARY fail={len(fails)}/{len(jobs)}", flush=True)
    for f in fails:
        print(f"  {f}", flush=True)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
