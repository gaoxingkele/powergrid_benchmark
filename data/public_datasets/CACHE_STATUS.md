# Public Dataset Cache Status

更新日期: 2026-07-07

## Summary

- Manifest rows: 19
- Downloaded/cache-ready: 12
- Metadata-only/API-ready: 7
- Planned without local path: 0

## Downloaded

- `matpower`
- `pandapower`
- `pglib_opf`
- `rts_gmlc`
- `simbench`
- `grid2op_datasets`
- `opsd_time_series`
- `psml`
- `dgann_duval`
- `dgadb`
- `lbnl_pmu_event_library`
- `gridstage`

## Metadata-Only / API-Ready

- `tamu_test_cases`: case portal cached; download selected cases as needed.
- `eia_opendata`: API page cached; use `EIA_API_KEY` for bulk data.
- `entsoe_transparency`: portal pages cached; use `ENTSOE_SECURITY_TOKEN` for API data.
- `pjm_dataminer`: access article cached; configure endpoint-specific downloads.
- `nsrdb`: API page cached; use `NREL_API_KEY` for weather/solar data.
- `large_synthetic_power_grid_ml`: Zenodo record cached; TB-scale data requires subset selection.
- `acn_data`: dataset page cached; use `ACN_API_TOKEN` for session data.

## Verification

Run:

```powershell
python scripts/data_acquisition/audit_public_datasets.py
```
