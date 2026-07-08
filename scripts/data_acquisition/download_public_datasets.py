"""Download or refresh public power-grid benchmark data sources.

The script keeps large/API-token datasets metadata-only by default. It is safe
to rerun: existing git repositories are updated with `git pull`, and metadata
files are overwritten from their public endpoints.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data" / "public_datasets"


@dataclass(frozen=True)
class Source:
    dataset_id: str
    path: Path
    kind: str
    url: str
    default: bool = True
    large: bool = False


SOURCES = [
    Source(
        "matpower",
        DATA_ROOT / "grid_cases" / "matpower",
        "git_sparse_matpower_data",
        "https://github.com/MATPOWER/matpower.git",
    ),
    Source(
        "pglib_opf",
        DATA_ROOT / "opf_benchmarks" / "pglib-opf",
        "git",
        "https://github.com/power-grid-lib/pglib-opf.git",
    ),
    Source(
        "pandapower",
        DATA_ROOT / "grid_cases" / "pandapower",
        "git_sparse_pandapower_networks",
        "https://github.com/e2nIEE/pandapower.git",
    ),
    Source(
        "rts_gmlc",
        DATA_ROOT / "production_cost" / "rts-gmlc",
        "git",
        "https://github.com/GridMod/RTS-GMLC.git",
    ),
    Source(
        "simbench",
        DATA_ROOT / "grid_cases" / "simbench",
        "git",
        "https://github.com/e2nIEE/simbench.git",
    ),
    Source(
        "grid2op_datasets",
        DATA_ROOT / "rl_control" / "grid2op-datasets",
        "git",
        "https://github.com/Grid2op/grid2op-datasets.git",
    ),
    Source(
        "opsd_time_series_datapackage",
        DATA_ROOT / "time_series_market" / "opsd_time_series_datapackage.json",
        "file",
        "https://data.open-power-system-data.org/time_series/latest/datapackage.json",
    ),
    Source(
        "opsd_time_series_readme",
        DATA_ROOT / "time_series_market" / "opsd_time_series_README.md",
        "file",
        "https://data.open-power-system-data.org/time_series/latest/README.md",
    ),
    Source(
        "opsd_time_series_60min",
        DATA_ROOT / "time_series_market" / "opsd_time_series" / "time_series_60min_singleindex.csv",
        "file",
        "https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv",
    ),
    Source(
        "entsoe_transparency_home",
        DATA_ROOT / "time_series_market" / "entsoe_transparency" / "transparency_platform.html",
        "file",
        "https://transparency.entsoe.eu/",
    ),
    Source(
        "entsoe_data_portal",
        DATA_ROOT / "time_series_market" / "entsoe_transparency" / "entsoe_data_portal.html",
        "file",
        "https://www.entsoe.eu/data/",
    ),
    Source(
        "pjm_dataminer_access",
        DATA_ROOT / "time_series_market" / "pjm_dataminer" / "dataminer_access_article.html",
        "file",
        "https://pjm.my.site.com/publicknowledge/s/article/Getting-access-to-Data-Miner",
    ),
    Source(
        "large_synthetic_power_grid_ml_zenodo",
        DATA_ROOT / "renewable_weather" / "large_synthetic_power_grid_ml_zenodo_record.json",
        "file",
        "https://zenodo.org/api/records/13378476",
        default=False,
        large=True,
    ),
    Source(
        "psml",
        DATA_ROOT / "renewable_weather" / "psml",
        "git",
        "https://github.com/tamu-engineering-research/Open-source-power-dataset.git",
    ),
    Source(
        "dgann_duval",
        DATA_ROOT / "equipment_fault_pmu" / "dgann_duval",
        "git",
        "https://github.com/fedebenelli/DGANN.git",
    ),
    Source(
        "dgadb",
        DATA_ROOT / "equipment_fault_pmu" / "dgadb",
        "git",
        "https://github.com/bmrayan/dgadb.git",
    ),
    Source(
        "lbnl_pmu_event_library",
        DATA_ROOT / "equipment_fault_pmu" / "lbnl_pmu_event_library",
        "git",
        "https://github.com/LBNL-ETA/pmu_event_library.git",
    ),
    Source(
        "gridstage",
        DATA_ROOT / "equipment_fault_pmu" / "gridstage",
        "git",
        "https://github.com/pnnl/GridSTAGE.git",
    ),
]


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=cwd, check=True)


def clone_or_pull(src: Source) -> None:
    src.path.parent.mkdir(parents=True, exist_ok=True)
    if (src.path / ".git").exists():
        print(f"update {src.dataset_id}: {src.path}")
        run(["git", "pull", "--ff-only"], cwd=src.path)
        return

    print(f"clone {src.dataset_id}: {src.url}")
    run(["git", "clone", "--depth", "1", src.url, str(src.path)])


def clone_sparse_matpower(src: Source) -> None:
    src.path.parent.mkdir(parents=True, exist_ok=True)
    if (src.path / ".git").exists():
        print(f"update {src.dataset_id}: {src.path}")
        run(["git", "pull", "--ff-only"], cwd=src.path)
        return

    print(f"sparse clone {src.dataset_id}: {src.url}")
    run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", src.url, str(src.path)])
    run(["git", "sparse-checkout", "set", "data", "README.md", "LICENSE", "CITATION"], cwd=src.path)


def clone_sparse_pandapower(src: Source) -> None:
    src.path.parent.mkdir(parents=True, exist_ok=True)
    if (src.path / ".git").exists():
        print(f"update {src.dataset_id}: {src.path}")
        run(["git", "pull", "--ff-only"], cwd=src.path)
        return

    print(f"sparse clone {src.dataset_id}: {src.url}")
    run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse", src.url, str(src.path)])
    run(["git", "sparse-checkout", "set", "pandapower/networks"], cwd=src.path)


def download_file(src: Source) -> None:
    src.path.parent.mkdir(parents=True, exist_ok=True)
    if src.path.exists() and src.path.stat().st_size > 0:
        print(f"exists {src.dataset_id}: {src.path}")
        return
    print(f"download metadata {src.dataset_id}: {src.url}")
    urllib.request.urlretrieve(src.url, src.path)


def selected_sources(dataset_ids: set[str], include_large: bool) -> list[Source]:
    selected = []
    for src in SOURCES:
        if dataset_ids and src.dataset_id not in dataset_ids:
            continue
        if not dataset_ids and not src.default:
            continue
        if src.large and not include_large:
            print(f"skip {src.dataset_id}: marked large/metadata-only; use --include-large or --dataset")
            continue
        selected.append(src)
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", action="append", default=[], help="Dataset id to fetch. Repeatable.")
    parser.add_argument("--include-large", action="store_true", help="Include sources marked large/metadata-only.")
    args = parser.parse_args()

    dataset_ids = set(args.dataset)
    known_ids = {src.dataset_id for src in SOURCES}
    unknown = dataset_ids - known_ids
    if unknown:
        print(f"unknown dataset id(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    for src in selected_sources(dataset_ids, args.include_large):
        if src.kind == "git":
            clone_or_pull(src)
        elif src.kind == "git_sparse_matpower_data":
            clone_sparse_matpower(src)
        elif src.kind == "git_sparse_pandapower_networks":
            clone_sparse_pandapower(src)
        elif src.kind == "file":
            download_file(src)
        else:
            raise ValueError(f"unsupported source kind: {src.kind}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
