# Figure 7: Optimal Operation Dispatch

**Source**: Page 18 of the PDF.

**Visual Description**:
Two-panel figure (a, b) showing the optimal operational dispatch under a representative scenario.

## Panel (a): Power Supply-Demand Balance
- **X-axis**: Time (h), 1-24 hours
- **Y-axis**: Power (MW), ranging approximately 0-500 MW
- **Color regions** (based on the power balance Equation 13):
  - **Blue region** (positive): Wind power generation (P_WT) — high during nighttime, lower during mid-day
  - **Red region** (positive, usually at top): Power purchased from grid (P_grid_buy) — significant during 07:00-09:00 (pre-charging)
  - **Green region** (negative, below the x-axis): Power sold to grid (P_grid_sell) — represents FiT revenue
  - **Black solid line**: Total load (P_EL + P_load) — includes electrolyzer consumption
  - **Black dashed line**: Base load (P_load only, without electrolyzer)

**Key observations from text**:
- Wind power dominates during night/early morning
- Electrolyzer operates during off-peak hours (00:00-08:00 and 22:00-24:00)
- Grid imports during 07:00-09:00 (strategic pre-charging — buy power to fill H2 tank before peak prices)
- Surplus wind is exported to grid (FiT revenue)

## Panel (b): Hydrogen Balance
- **X-axis**: Time (h), 1-24 hours
- **Left Y-axis**: Hydrogen Flow (Nm³/h), ranging 0-500 Nm³/h
- **Right Y-axis**: Storage Level (Nm³), ranging 0-4×10⁴ Nm³

- **Green bars**: Hydrogen production (P_EL → electrolysis) — concentrated during 00:00-08:00
- **Black dashed line**: Hydrogen demand (D_H2) — rigid demand from 09:00-17:00
- **Pink line**: State of Charge (SoC) of the hydrogen tank
- **Red dashed line**: Capacity limit of the storage tank

**Four phases of SoC**:
1. **Charging (00:00-08:00)**: SoC rises steadily as electrolyzer runs at full capacity
2. **Standby (08:00-09:00)**: Production ceases, SoC remains high
3. **Discharging (09:00-17:00)**: Electrolyzer shut down (avoids peak prices), storage meets demand; SoC declines linearly
4. **Depletion (17:00-18:00)**: SoC drops to near-zero after demand ends

**Key observation**: Peak SoC reaches ≈4×10³ Nm³ (≈23 MWh), matching the Stage I investment decision (E_H2 = 23.23 MWh), confirming no redundant capacity.
