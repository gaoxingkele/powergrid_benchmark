# Dataset Benchmark Paper Search

- Search window: `2023-07-09` to `2026-07-09` (OpenAlex harvest); curated exemplars extend to 2021–2026.
- Source: OpenAlex works API + curated OA seed list.
- Scope: existing local public power-grid datasets (manifest, 49 IDs).
- Download policy: only open-access/public PDFs; paywalled PDFs were not fetched.
- SCI/CCF status is a candidate label and must be verified against WoS/JCR and the current CCF list.
- `metadata/dataset_paper_candidates.csv` is the raw candidate set.
- `metadata/dataset_paper_candidates_filtered.csv` is the power-grid reading list.
- **研究方向 × 近五年 SCI × Open Access 期刊匹配（中文主文档）**：[`DATASET_DIRECTION_OA_SCI.md`](DATASET_DIRECTION_OA_SCI.md)
- 机器可读精选表：`metadata/dataset_direction_sci_exemplars_curated.csv`

## Local SCI / OA PDF cache (2026-07-26)

- **49/49** datasets have **≥5** local PDFs under `pdfs/<dataset_id>/` (**245** files total).
- Index: `metadata/dataset_sci_oa_pdf_summary.csv`, `metadata/dataset_sci_oa_pdf_registry.csv`
- Prefer arXiv PDFs (SCI/top-venue preprints) + Nature OA; MDPI/IEEE stampPDF often 403 via proxy.
- Re-run (skips existing digests):

```powershell
python scripts/literature/download_dataset_sci_oa_pdfs_aria2.py
```

## Per-dataset PDF counts

| Dataset | PDFs | OK |
|---|---:|:---:|
| `matpower` | 5 | yes |
| `pandapower` | 5 | yes |
| `pglib_opf` | 5 | yes |
| `rts_gmlc` | 5 | yes |
| `simbench` | 5 | yes |
| `grid2op_datasets` | 5 | yes |
| `tamu_test_cases` | 5 | yes |
| `opsd_time_series` | 5 | yes |
| `eia_opendata` | 5 | yes |
| `entsoe_transparency` | 5 | yes |
| `pjm_dataminer` | 5 | yes |
| `nsrdb` | 5 | yes |
| `large_synthetic_power_grid_ml` | 5 | yes |
| `psml` | 5 | yes |
| `acn_data` | 5 | yes |
| `dgann_duval` | 5 | yes |
| `dgadb` | 5 | yes |
| `lbnl_pmu_event_library` | 5 | yes |
| `gridstage` | 5 | yes |
| `c2ges_nerc_reports` | 5 | yes |
| `ett` | 5 | yes |
| `uci_household_power` | 5 | yes |
| `uci_tetouan_power` | 5 | yes |
| `monash_australian_demand` | 5 | yes |
| `panama_load` | 5 | yes |
| `elia_total_load` | 5 | yes |
| `ausgrid_solar_home` | 5 | yes |
| `nrel118` | 5 | yes |
| `sgsc` | 5 | yes |
| `sgcc_electricity_theft` | 5 | yes |
| `sdwpf_kddcup2022` | 5 | yes |
| `miso_mtep` | 5 | yes |
| `nasa_pcoe_battery` | 5 | yes |
| `nasa_randomized_recommissioned_battery` | 5 | yes |
| `oxford_battery_degradation` | 5 | yes |
| `calce_battery` | 5 | yes |
| `battery_archive` | 5 | yes |
| `stanford_tri_high_power_battery` | 5 | yes |
| `acn_data_static` | 5 | yes |
| `m5bat_bess` | 5 | yes |
| `finland_afrr_weather` | 5 | yes |
| `bess_european_balancing_inputs` | 5 | yes |
| `renewables_ninja_country_sample` | 5 | yes |
| `vce_rare_power` | 5 | yes |
| `eia860_wind_solar_cf` | 5 | yes |
| `secures_energy` | 5 | yes |
| `era5_eu_supply_demand` | 5 | yes |
| `pglearn_small` | 5 | yes |
| `opfdata_landing` | 5 | yes |
