"""Register planned extension datasets in the public manifest if missing."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "data" / "public_datasets" / "manifests" / "public_dataset_manifest.csv"

ROWS = [
    ("nasa_pcoe_battery", "battery_bms", "data/public_datasets/battery_bms/nasa_pcoe_battery", "planned", "https://data.nasa.gov/dataset/li-ion-battery-aging-datasets", "direct_download", "yes", "SOC;SOH;RUL;battery aging;EIS", "NASA PCoE Li-ion aging"),
    ("nasa_randomized_recommissioned_battery", "battery_bms", "data/public_datasets/battery_bms/nasa_randomized_recommissioned_battery", "planned", "https://data.nasa.gov/dataset/randomized-and-recommissioned-battery-dataset", "metadata_and_landing", "yes", "second-life battery;pack aging", "NASA randomized/recommissioned packs"),
    ("oxford_battery_degradation", "battery_bms", "data/public_datasets/battery_bms/oxford_battery_degradation", "planned", "https://ora.ox.ac.uk/objects/uuid:03ba4b01-cfed-46d3-9b1a-7d4a7bdf6fac", "direct_download", "yes", "SOH;RUL;drive-cycle aging", "Oxford Battery Degradation Dataset 1"),
    ("calce_battery", "battery_bms", "data/public_datasets/battery_bms/calce_battery", "planned", "https://calce.umd.edu/battery-data", "landing_and_samples", "yes", "SOC;SOH;DST;FUDS", "CALCE open battery data"),
    ("battery_archive", "battery_bms", "data/public_datasets/battery_bms/battery_archive", "planned", "https://batteryarchive.org/", "landing", "yes", "battery aging catalogue", "Battery Archive catalogue"),
    ("stanford_tri_high_power_battery", "battery_bms", "data/public_datasets/battery_bms/stanford_tri_high_power_battery", "planned", "https://doi.org/10.17605/OSF.IO/9CEAV", "osf_api", "yes", "high C-rate;stochastic modeling", "Stanford-TRI high-power cells"),
    ("acn_data_static", "distribution_ev", "data/public_datasets/distribution_ev/acn_data_static", "planned", "https://github.com/tongxin-li/ACN-Data-Static", "git_sparse_clone", "yes", "EV charging", "ACN-Data sparse offline snapshot"),
    ("m5bat_bess", "bess_grid", "data/public_datasets/bess_grid/m5bat_bess", "planned", "https://doi.org/10.18154/rwth-2024-04895", "rwth_publications", "yes", "BESS FCR;SOC", "M5BAT field BESS"),
    ("finland_afrr_weather", "bess_grid", "data/public_datasets/bess_grid/finland_afrr_weather", "planned", "https://doi.org/10.5281/zenodo.17494555", "zenodo", "yes", "aFRR;weather", "Finland aFRR+weather"),
    ("bess_european_balancing_inputs", "bess_grid", "data/public_datasets/bess_grid/bess_european_balancing_inputs", "planned", "https://doi.org/10.5281/zenodo.18199323", "zenodo", "yes", "FCR;aFRR", "European BESS balancing inputs"),
    ("renewables_ninja_country_sample", "renewable_weather", "data/public_datasets/renewable_weather/renewables_ninja_country_sample", "planned", "https://www.renewables.ninja/downloads", "direct_download", "yes", "wind/solar CF", "Renewables.ninja country sample"),
    ("vce_rare_power", "renewable_weather", "data/public_datasets/renewable_weather/vce_rare_power", "planned", "https://zenodo.org/records/13937523", "zenodo_subset", "yes", "resource adequacy", "VCE RARE"),
    ("eia860_wind_solar_cf", "renewable_weather", "data/public_datasets/renewable_weather/eia860_wind_solar_cf", "planned", "https://zenodo.org/records/20518257", "zenodo_record_meta", "yes", "plant-level CF", "EIA-860 wind/solar CF"),
    ("secures_energy", "renewable_weather", "data/public_datasets/renewable_weather/secures_energy", "planned", "https://zenodo.org/records/14615500", "zenodo_record_meta", "yes", "climate-energy", "SECURES-Energy"),
    ("era5_eu_supply_demand", "renewable_weather", "data/public_datasets/renewable_weather/era5_eu_supply_demand", "planned", "https://zenodo.org/records/13938926", "zenodo_record_meta", "yes", "EU supply/demand", "ERA5 EU climate power series"),
    ("pglearn_small", "opf_benchmarks", "data/public_datasets/opf_benchmarks/pglearn_small", "planned", "https://huggingface.co/collections/PGLearn/pglearn-small", "huggingface_subset", "yes", "ML-OPF", "PGLearn Small subset"),
    ("opfdata_landing", "opf_benchmarks", "data/public_datasets/opf_benchmarks/opfdata_landing", "planned", "https://arxiv.org/abs/2406.07234", "landing", "yes", "AC-OPF topology", "OPFData landing/notes"),
]


def main() -> None:
    with MANIFEST.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
        fields = list(rows[0].keys())
    by_id = {r["dataset_id"]: r for r in rows}
    for tup in ROWS:
        row = dict(zip(fields, tup))
        if tup[0] not in by_id:
            by_id[tup[0]] = row
    with MANIFEST.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(by_id.values())
    print(f"manifest rows: {len(by_id)}")


if __name__ == "__main__":
    main()
