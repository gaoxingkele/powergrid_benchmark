# Public Datasets

本目录缓存公开电网 benchmark 数据和访问入口。大体量、需要 token 或需注册的数据源默认只保存 metadata，不全量下载。

## Layout

- `grid_cases/`: 标准网架和合成系统。
- `opf_benchmarks/`: OPF 专用 benchmark。
- `production_cost/`: 生产成本、机组组合和可靠性数据。
- `time_series_market/`: 负荷、发电、市场和价格时序。
- `renewable_weather/`: 天气、太阳能、风电和可再生能源数据。
- `rl_control/`: Grid2Op/L2RPN 等交互控制环境索引。
- `distribution_ev/`: EV 充电和用户侧数据入口。
- `equipment_fault_pmu/`: DGA、PMU、故障和扰动数据候选。
- `manifests/`: 机器可读数据清单。

## Scripts

- `scripts/data_acquisition/download_public_datasets.py`: 获取或更新公开数据源。
- `scripts/data_acquisition/audit_public_datasets.py`: 审计本地数据源状态。
