# Public Dataset Cache Status

更新日期: 2026-07-25

## Summary

- Manifest rows: 49
- Downloaded/cache-ready: 43
- Partial: 1
- Metadata-only/API-ready: 5

## Zenodo download policy

Zenodo 大文件**唯一可靠方案**为本机 aria2 + 本地代理：

```powershell
python scripts/data_acquisition/download_zenodo_aria2.py
# 等价手工命令要点：
# aria2c --all-proxy=http://127.0.0.1:17890 --split=16 --max-connection-per-server=16 --continue=true --file-allocation=none <url>
```

历史验证：`large_synthetic_power_grid_ml` 经同一参数集稳定完成 19/19 文件。

## Extension batch (新能源 / 电力系统 / BMS)

| dataset_id | status | path |
|---|---|---|
| `nasa_pcoe_battery` | downloaded | `data/public_datasets/battery_bms/nasa_pcoe_battery` |
| `nasa_randomized_recommissioned_battery` | metadata-only | `data/public_datasets/battery_bms/nasa_randomized_recommissioned_battery` |
| `oxford_battery_degradation` | downloaded | `data/public_datasets/battery_bms/oxford_battery_degradation` |
| `calce_battery` | downloaded | `data/public_datasets/battery_bms/calce_battery` |
| `battery_archive` | metadata-only | `data/public_datasets/battery_bms/battery_archive` |
| `stanford_tri_high_power_battery` | downloaded | `data/public_datasets/battery_bms/stanford_tri_high_power_battery` |
| `acn_data_static` | downloaded | `data/public_datasets/distribution_ev/acn_data_static` |
| `m5bat_bess` | downloaded | `data/public_datasets/bess_grid/m5bat_bess` |
| `finland_afrr_weather` | downloaded | `data/public_datasets/bess_grid/finland_afrr_weather` |
| `bess_european_balancing_inputs` | downloaded | `data/public_datasets/bess_grid/bess_european_balancing_inputs` |
| `renewables_ninja_country_sample` | downloaded | `data/public_datasets/renewable_weather/renewables_ninja_country_sample` |
| `vce_rare_power` | downloaded | `data/public_datasets/renewable_weather/vce_rare_power` |
| `eia860_wind_solar_cf` | downloaded | `data/public_datasets/renewable_weather/eia860_wind_solar_cf` |
| `secures_energy` | downloaded | `data/public_datasets/renewable_weather/secures_energy` |
| `era5_eu_supply_demand` | downloaded | `data/public_datasets/renewable_weather/era5_eu_supply_demand` |
| `pglearn_small` | downloaded | `data/public_datasets/opf_benchmarks/pglearn_small` |
| `opfdata_landing` | downloaded | `data/public_datasets/opf_benchmarks/opfdata_landing` |

## Continuation notes (2026-07-25)

- `m5bat_bess`: RWTH `fast-challenge` 拦截非浏览器客户端；用 Playwright+代理拿到 RAW zip(~97MB)+Report PDF；Deflate64 用 `7za` 解压出 11 个 CSV（~1.5GB）。
- `acn_data_static`: sparse git 拉齐站点时序目录（约 6.7GB / 8.4万文件）；上游 session JSON 为空。
- `pglearn_small`: 缓存 `PGLearn/PGLearn-Small-14_ieee` 的 1 train + 1 test parquet（~154MB）；完整 `14_ieee.tar.gz` ~9.2GB 未下。
- `renewables_ninja_country_sample`: ninja 旧 static 链接 404；已缓存 OPSD DE renewable plants (~329MB) 等开放替代。
- 仍卡：`nasa_randomized_recommissioned_battery`（门户/联系）、`battery_archive`（条款）、`nsrdb`/`pjm_dataminer`/`tamu_test_cases`/`acn_data` API。
- `large_synthetic_power_grid_ml`：目录曾丢失，已用 aria2+代理重下完成 **19/19**（~17.8GB）；`audit_public_datasets.py` 已通过。

## Verification

```powershell
python scripts/data_acquisition/audit_public_datasets.py
```
