"""Download Zenodo files with aria2 (proxy + multi-connection + continue).

Proven flags for this environment:
  aria2c --split=16 --max-connection-per-server=16 --continue=true
  --all-proxy=http://127.0.0.1:17890
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "public_datasets"
PROXY = "http://127.0.0.1:17890"
ARIA2_CANDIDATES = [
    Path(r"C:\Users\10175\AppData\Local\aria2\aria2-1.37.0-win-64bit-build1\aria2c.exe"),
    Path(r"C:\Users\10175\AppData\Local\aria2c.exe"),
    Path(r"C:\Program Files\Netease\GameViewer\bin\aria2c.exe"),
]

# record metadata path -> destination directory
TARGETS = [
    DATA / "bess_grid" / "finland_afrr_weather",
    DATA / "bess_grid" / "bess_european_balancing_inputs",
    DATA / "renewable_weather" / "vce_rare_power",
    DATA / "renewable_weather" / "eia860_wind_solar_cf",
    DATA / "renewable_weather" / "secures_energy",
    DATA / "renewable_weather" / "era5_eu_supply_demand",
]


def find_aria2() -> Path:
    which = shutil.which("aria2c")
    if which:
        return Path(which)
    for path in ARIA2_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("aria2c not found")


def file_url(entry: dict) -> str | None:
    links = entry.get("links") or {}
    return links.get("self") or links.get("content") or links.get("download")


def needs_download(dest: Path, expected_size: int | None) -> bool:
    if not dest.exists():
        return True
    size = dest.stat().st_size
    if expected_size and size >= expected_size:
        return False
    # Incomplete / truncated
    return True


def process_dir(aria2: Path, dest_dir: Path, max_mb: float | None, proxy: str) -> list[tuple[str, str]]:
    meta_path = dest_dir / "zenodo_record.json"
    if not meta_path.exists():
        return [(dest_dir.name, "missing_zenodo_record.json")]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    results = []
    for entry in meta.get("files") or []:
        key = entry.get("key") or "file.bin"
        size = int(entry.get("size") or 0)
        url = file_url(entry)
        out = dest_dir / key
        if max_mb is not None and size > max_mb * 1024 * 1024:
            results.append((key, f"skipped_too_large:{size/1024/1024:.1f}MB"))
            continue
        if not url:
            results.append((key, "missing_url"))
            continue
        if not needs_download(out, size):
            results.append((key, f"already_complete:{out.stat().st_size}"))
            continue
        code = aria2_get(aria2, url, out, proxy)
        final = out.stat().st_size if out.exists() else 0
        ok = code == 0 and (size == 0 or final >= size)
        results.append((key, f"{'ok' if ok else 'failed'} code={code} size={final}/{size}"))
    return results


def aria2_get(aria2: Path, url: str, dest: Path, proxy: str) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(aria2),
        f"--all-proxy={proxy}",
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
    return subprocess.call(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", default=None, help="Directory name filters")
    parser.add_argument("--max-mb", type=float, default=None, help="Skip files larger than this many MB")
    parser.add_argument("--proxy", default=PROXY)
    args = parser.parse_args()
    aria2 = find_aria2()
    print(f"aria2={aria2}", flush=True)
    print(f"proxy={args.proxy}", flush=True)

    targets = TARGETS
    if args.only:
        wanted = set(args.only)
        targets = [t for t in TARGETS if t.name in wanted]

    all_results = []
    for dest_dir in targets:
        print(f"==> {dest_dir}", flush=True)
        for item in process_dir(aria2, dest_dir, args.max_mb, args.proxy):
            all_results.append((dest_dir.name, *item))
            print(f"  {item[0]}: {item[1]}", flush=True)

    failed = [r for r in all_results if r[2].startswith("failed") or r[2].startswith("missing")]
    print("=== summary ===", flush=True)
    for row in all_results:
        print(f"{row[0]}/{row[1]}: {row[2]}", flush=True)
    print(f"failed={len(failed)} total={len(all_results)}", flush=True)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
