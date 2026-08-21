# Method — DLR + Transformer-Life-Loss-Aware Unit Commitment (TL-TF)

## Pipeline overview

The method (paper's "TL-TF" model) chains three stages into one optimization:

1. **DLR stage (§2).** From day-ahead ambient temperature, wind speed, and solar irradiance, compute
   the conductor thermal-balance parameters β0, β1, β2 (Eqs. 5-8) and the temperature-dependent
   maximum current Imax (Eq. 10), yielding a per-line, per-hour capacity limit Pmax(Ta). This replaces
   the static line rating with a real-time, weather-driven limit.

2. **Transformer hot-spot / life-loss stage (§3).** From the load factor KL and ambient temperature,
   compute top-oil temperature (Eqs. 13-16), ultimate hot-spot temperature TH (Eqs. 17-19), the
   per-condition loss-of-life rate D_i (Eq. 21, Arrhenius), and the monetized life-loss cost CTF
   (Eq. 20, linear/Miner damage accumulation). This makes transformer aging a dispatch-dependent cost.

3. **UC optimization stage (§4).** Minimize the composite objective F = Ccoal + CTF + CW + CUD
   (Eq. 22) subject to wind decomposition, power balance, generation/ramp/reserve limits, GSDF line
   flows, interface limits, and — the key coupling — the temperature-dependent capacity constraint
   (Eq. 31). Solved as a mixed-integer program in Gurobi.

## Data flow (diagram, from Figure 1 and text)

```
Day-ahead inputs                DLR sub-model            UC optimization
  Ta (5 regional zones) ─┐       θss = β0+β1 I^2+β2 I^4   min F = Ccoal+CTF+CW+CUD
  wind speed, solar    ──┼────►  Imax(Ta) (Eq.10) ──────► Pmax(Ta) capacity bound (Eq.31)
  load forecast D_t    ──┤                                 + power balance / ramp / reserve
  wind forecast P̂wind ──┘       KL, Ta ──► TH (Eq.17) ──► CTF life-loss cost (Eq.20-21)
                                                          │
  IEEE 39-bus GSDF ──────────────────────────────────────┘ line flows (Eq.28) + interfaces (Eq.29-30)
                                                          ▼
                                          Gurobi 12.0.1 → unit outputs P_{i,t}^th, commitment u_{i,t}
```

## Network / regional structure (from Figure 1)

- IEEE 39-bus system: 10 synchronous generators, 39 buses; bus #31 is the slack bus.
- Equivalent wind turbines (DFIG, PSASP model) connected at buses #17 and #21.
- System partitioned into five regions (Area1-Area5) by transmission lines; each region carries its
  own 24 h ambient-temperature curve (Figure 2).
- Interface 1 = tie lines 1-2, 1-39, 3-4 (northwest power-flow corridor); interface flow bounded by
  a transmission-section capacity / transfer-corridor limit (Figure 5).

## Why the coupling matters (mechanism)

Regional temperature heterogeneity is the lever: a hot region (e.g., area 3 / Unit 2) has both
reduced line ampacity (via the DLR bound) and elevated transformer hot-spot temperature (via the
life-loss cost). The optimizer therefore suppresses the otherwise-economic hot-region unit and
compensates with cooler-region or spare-capacity units — simultaneously relieving the transmission
bottleneck, reducing wind curtailment, and holding transformer hot-spot near 98 C. This is the
reallocation visible between Figure 4a (conventional) and Figure 4b (TL-TF).

## Comparison configurations

- **Conventional model ("Con-Model")**: static thermal stability — no temperature-dependent line
  limit, no transformer life-loss cost.
- **Proposed model ("TL-TF")**: DLR capacity constraint + transformer life-loss cost term.
