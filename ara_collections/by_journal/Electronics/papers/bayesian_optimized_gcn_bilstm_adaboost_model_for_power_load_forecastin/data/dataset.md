# Dataset

- **Provenance**: Hourly electricity-load data from a specific (unnamed) region.
- **Time span**: 00:00 on 1 January 2018 to 23:00 on 28 December 2018 (~one year, hourly).
- **Size**: Hourly resolution over ~362 days; the paper states m = 1200 training samples (test size not
  explicitly stated).
- **Columns (10 total; §2.1, §3.1, Table 1)**: date (year-month-day hour), load value, humidity,
  temperature, wind speed, atmospheric pressure, precipitation, visibility, water vapor pressure,
  perceived (sensible) temperature.
- **Input features**: described as "9 feature columns" in §2.1 (load + 8 weather features); the GCN
  operates on "8-dimensional feature vectors" of meteorological factors and the model input tensor is
  24 × 8 (Table 3). (8-vs-9 ambiguity noted in `logic/solution/constraints.md`, item 6.)
- **Target**: next-hour load value (MW).
- **Units (Table 1 example row, 1 Jan 2018 00:00)**: Load 174 MW; Humidity 53 %; Temperature −3.6 °C;
  Pressure 1024.4 Pa; Wind Speed 0.4 m/s; Precipitation 0 mm; Visibility 5.25 km; Vapor Pressure
  2.48 hPa; Sensible Temperature −6.32 °C.
- **Licensing / availability**: **Not publicly available** due to privacy restrictions; available upon
  reasonable request from the corresponding author (Data Availability Statement).
- **Ethics/consent**: Not specified in paper (regional grid load data).

## Source
Table 1 (data example), §3.1 (data description).
