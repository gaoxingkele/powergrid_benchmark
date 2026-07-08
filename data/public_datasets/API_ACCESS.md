# API and Restricted Dataset Access

本项目会尽量缓存公开可直连数据；以下数据源需要 token/API key、账号或子集选择，不能可靠地无凭证全量下载。

## Environment Variables

建议将凭证放在本机环境变量，不写入仓库：

```powershell
$env:EIA_API_KEY="..."
$env:NREL_API_KEY="..."
$env:ENTSOE_SECURITY_TOKEN="..."
$env:ACN_API_TOKEN="..."
```

## Source Notes

- EIA Open Data: 已缓存入口页；正式批量拉取建议使用 `EIA_API_KEY`。
- NREL NSRDB: 已缓存 API 文档；正式拉取需要 `NREL_API_KEY`、地理范围、时间范围和变量选择。
- ENTSO-E Transparency: 已缓存门户页；正式 API 数据需要 security token。
- PJM Data Miner 2: 已缓存访问说明；正式批量拉取需按 endpoint 选择，部分访问依赖 PJM 账户/API 流程。
- ACN-Data: 已缓存数据集入口；正式 API 数据需要注册 token。
- Zenodo large synthetic power-grid ML dataset: 已缓存 record JSON；总量 TB 级，应按论文任务选择子集下载。

## Policy

1. 不把 API key、token、账号密码写进代码或文档。
2. 每次下载真实数据时记录 endpoint、参数、时间范围、字段和本地输出路径。
3. 对 TB 级数据只下载实验所需子集。
