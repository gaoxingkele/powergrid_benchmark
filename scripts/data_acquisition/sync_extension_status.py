"""Sync manifest + CACHE_STATUS after continuation downloads."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "public_datasets" / "manifests" / "public_dataset_manifest.csv"
CACHE = ROOT / "data" / "public_datasets" / "CACHE_STATUS.md"
DATA = ROOT / "data" / "public_datasets"


def size(path: Path) -> int:
    if path.is_file():
        return path.stat().st_size
    if path.is_dir():
        return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())
    return 0


def decide() -> dict[str, tuple[str, str]]:
    """dataset_id -> (status, notes)"""
    out: dict[str, tuple[str, str]] = {}

    m5_zip = DATA / "bess_grid" / "m5bat_bess" / "M5BAT_04-2023_RAW.zip"
    m5_pdf = DATA / "bess_grid" / "m5bat_bess" / "Report_04-2023.pdf"
    m5_raw = DATA / "bess_grid" / "m5bat_bess" / "raw"
    csvs = list(m5_raw.glob("*.csv")) if m5_raw.exists() else []
    if m5_zip.exists() and m5_zip.stat().st_size > 50_000_000 and m5_pdf.exists() and m5_pdf.stat().st_size > 100_000:
        note = (
            f"RWTH record 985923 via Playwright (fast-challenge). "
            f"ZIP={m5_zip.stat().st_size}; PDF={m5_pdf.stat().st_size}; "
            f"extracted_csvs={len(csvs)}"
        )
        out["m5bat_bess"] = ("downloaded", note)
    elif m5_zip.exists() and m5_zip.stat().st_size > 50_000_000:
        out["m5bat_bess"] = ("partial", "RAW zip present; report/extract incomplete")
    else:
        out["m5bat_bess"] = ("metadata-only", "RWTH fast-challenge blocks non-browser clients")

    acn = DATA / "distribution_ev" / "acn_data_static"
    acn_files = [p for p in acn.rglob("*") if p.is_file() and p.name != "README.md"] if acn.exists() else []
    acn_bytes = sum(p.stat().st_size for p in acn_files)
    if acn_bytes > 1_000_000_000:
        out["acn_data_static"] = (
            "downloaded",
            f"Sparse git of ACN-Data-Static site folders; files={len(acn_files)} bytes={acn_bytes}",
        )
    elif acn_bytes > 1_000_000:
        out["acn_data_static"] = ("partial", f"files={len(acn_files)} bytes={acn_bytes}")
    else:
        out["acn_data_static"] = ("partial", "session JSON empty upstream; site folders missing")

    pg = DATA / "opf_benchmarks" / "pglearn_small" / "PGLearn-Small-14_ieee"
    pq = list(pg.rglob("*.parquet")) if pg.exists() else []
    if pq:
        out["pglearn_small"] = (
            "downloaded",
            f"HF sample shards from PGLearn/PGLearn-Small-14_ieee; parquet={len(pq)} "
            f"bytes={sum(p.stat().st_size for p in pq)} (full 14_ieee.tar.gz ~9.2GB not cached)",
        )
    else:
        out["pglearn_small"] = ("metadata-only", "HF README/collection only")

    ninja = DATA / "renewable_weather" / "renewables_ninja_country_sample"
    plants = ninja / "opsd_renewable_power_plants_DE.csv"
    stacked = ninja / "national_generation_capacity_stacked.csv"
    if plants.exists() and plants.stat().st_size > 10_000_000:
        extras = []
        if stacked.exists() and stacked.stat().st_size > 1000:
            extras.append(f"capacity_stacked={stacked.stat().st_size}")
        out["renewables_ninja_country_sample"] = (
            "downloaded",
            "OPSD renewable plant DE table as open companion to renewables.ninja UI extracts; "
            f"plants={plants.stat().st_size}; " + ",".join(extras),
        )
    elif (ninja / "renewables_ninja_landing.html").exists():
        out["renewables_ninja_country_sample"] = ("metadata-only", "landing only; ninja static downloads 404")
    else:
        out["renewables_ninja_country_sample"] = ("metadata-only", "not fetched")

    ba = DATA / "battery_bms" / "battery_archive" / "index.html"
    if ba.exists() and ba.stat().st_size > 500:
        out["battery_archive"] = (
            "metadata-only",
            "Catalogue portal cached; study CSV downloads require browser terms acceptance",
        )

    nasa = DATA / "battery_bms" / "nasa_randomized_recommissioned_battery"
    nasa_bytes = size(nasa)
    if nasa_bytes > 10_000_000:
        out["nasa_randomized_recommissioned_battery"] = ("downloaded", f"bytes={nasa_bytes}")
    else:
        out["nasa_randomized_recommissioned_battery"] = (
            "metadata-only",
            "Portal landing; direct pack download unavailable/contact required",
        )

    return out


def main() -> None:
    updates = decide()
    rows = list(csv.DictReader(MANIFEST.open(encoding="utf-8-sig")))
    fields = list(rows[0].keys())
    by = {r["dataset_id"]: r for r in rows}
    for did, (status, notes) in updates.items():
        if did not in by:
            continue
        by[did]["status"] = status
        by[did]["notes"] = notes
        if did == "m5bat_bess":
            by[did]["source_url"] = "https://publications.rwth-aachen.de/record/985923"
            by[did]["access_mode"] = "playwright_rwth"
        if did == "pglearn_small":
            by[did]["access_mode"] = "huggingface_sample"
        if did == "acn_data_static":
            by[did]["access_mode"] = "git_sparse"
        if did == "renewables_ninja_country_sample":
            by[did]["access_mode"] = "opsd_companion"

    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(by.values())

    downloaded = sum(1 for r in by.values() if r["status"] == "downloaded")
    partial = sum(1 for r in by.values() if r["status"] == "partial")
    meta = sum(1 for r in by.values() if r["status"] == "metadata-only")

    ext_ids = [
        "nasa_pcoe_battery",
        "nasa_randomized_recommissioned_battery",
        "oxford_battery_degradation",
        "calce_battery",
        "battery_archive",
        "stanford_tri_high_power_battery",
        "acn_data_static",
        "m5bat_bess",
        "finland_afrr_weather",
        "bess_european_balancing_inputs",
        "renewables_ninja_country_sample",
        "vce_rare_power",
        "eia860_wind_solar_cf",
        "secures_energy",
        "era5_eu_supply_demand",
        "pglearn_small",
        "opfdata_landing",
    ]

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
        "Zenodo 大文�?*唯一可靠方案**为本�?aria2 + 本地代理�?,
        "",
        "```powershell",
        "python scripts/data_acquisition/download_zenodo_aria2.py",
        "# 等价手工命令要点�?,
        "# aria2c --all-proxy=http://127.0.0.1:17890 --split=16 --max-connection-per-server=16 --continue=true --file-allocation=none <url>",
        "```",
        "",
        "历史验证：`large_synthetic_power_grid_ml` 经同一参数集稳定完�?19/19 文件�?,
        "",
        "## Extension batch (新能�?/ 电力系统 / BMS)",
        "",
        "| dataset_id | status | path |",
        "|---|---|---|",
    ]
    for did in ext_ids:
        r = by.get(did)
        if not r:
            continue
        lines.append(f"| `{did}` | {r['status']} | `{r['local_path']}` |")

    lines += [
        "",
        "## Continuation notes (2026-07-25)",
        "",
        "- `m5bat_bess`: RWTH fast-challenge blocks non-browser clients; Playwright+proxy got RAW zip+PDF; extract with 7za (Deflate64).",
        "- `acn_data_static`: sparse git of site time-series folders (~6.7GB / 84k files); upstream session JSON empty.",
        "- `pglearn_small`: cached 1 train + 1 test parquet from PGLearn-Small-14_ieee (~154MB); full 14_ieee.tar.gz ~9.2GB not cached.",
        "- `renewables_ninja_country_sample`: ninja static links 404; cached OPSD DE renewable plants (~329MB) as companion.",
        "- Still gated: nasa_randomized_recommissioned_battery, battery_archive, nsrdb, pjm_dataminer, tamu_test_cases, acn_data API.",
        "",
        "## Verification",
        "",
        "```powershell",
        "python scripts/data_acquisition/audit_public_datasets.py",
        "```",
        "",
    ]
    CACHE.write_text("\n".join(lines), encoding="utf-8")

    print("updates:")
    for k, v in updates.items():
        print(f"  {k}: {v[0]}")
    print(f"summary downloaded={downloaded} partial={partial} meta={meta}")


if __name__ == "__main__":
    main()
