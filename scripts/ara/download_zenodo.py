"""Download Zenodo large files through proxy with auto-resume.
Usage: py -3 scripts/ara/download_zenodo.py [loads|lines] <year>
Writes to data/public_datasets/renewable_weather/large_synthetic_power_grid_ml/
"""
import sys, os, time, requests

PROXY = "http://127.0.0.1:17890"
ZENODO = "https://zenodo.org/api/records/13378476/files"
DEST = "data/public_datasets/renewable_weather/large_synthetic_power_grid_ml"

def download(prefix, year):
    url = f"{ZENODO}/{prefix}_{year}.zip/content"
    dest = os.path.join(DEST, f"{prefix}_{year}.zip")

    # Check current size
    current = os.path.getsize(dest) if os.path.exists(dest) else 0

    proxies = {"http": PROXY, "https": PROXY}
    headers = {}
    if current > 0:
        headers["Range"] = f"bytes={current}-"

    start = time.perf_counter()
    resp = requests.get(url, proxies=proxies, headers=headers, stream=True, timeout=(30, 3600))

    if resp.status_code in (200, 206):
        total = current + int(resp.headers.get("content-length", 0))
        mode = "ab" if current > 0 else "wb"
        with open(dest, mode) as f:
            for chunk in resp.iter_content(chunk_size=8*1024*1024):
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())
        elapsed = time.perf_counter() - start
        final = os.path.getsize(dest)
        print(f"[{prefix}_{year}] {final} bytes in {elapsed:.0f}s ({final/elapsed/1024:.0f} KB/s)")
        return True
    else:
        print(f"[{prefix}_{year}] HTTP {resp.status_code}: {resp.text[:200]}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py -3 scripts/ara/download_zenodo.py loads|lines 2017")
        sys.exit(1)
    ok = False
    for attempt in range(10):
        ok = download(sys.argv[1], sys.argv[2])
        if ok:
            break
        print(f"Retry {attempt+2}/10 in 30s...")
        time.sleep(30)
    sys.exit(0 if ok else 1)
