# Architecture

## Overall System Architecture

The proposed method consists of three main components:
1. **WGAN-GP Scenario Generation Module** — Generates representative wind–solar time-series scenarios
2. **ADN Expansion Planning Model** — Jointly optimizes siting and sizing of all resources
3. **SCCR Solution Algorithm** — Solves the non-convex optimization problem

```
┌─────────────────────────────────────────────────────────┐
│  WGAN-GP Scenario Generation                            │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────┐  │
│  │ Generator │───>│ Discriminator│───>│ Wasserstein   │  │
│  │ (Noise→   │    │ (Real/Fake) │    │ Loss + GP     │  │
│  │  Pseudo-  │    │              │    │               │  │
│  │  samples) │    │              │    │               │  │
│  └──────────┘    └──────────────┘    └───────────────┘  │
│         │                                                │
│         ▼                                                │
│  ┌──────────────────────────────────┐                    │
│  │ Generated Wind–Solar Scenarios  │                    │
│  │ K-medoids → 4 Representative    │                    │
│  └──────────────────────────────────┘                    │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  ADN Expansion Planning Model                           │
│  Objective: min C_ann = C_inv_ann + C_op_ann           │
│                                                         │
│  Decision Variables:                                    │
│  • Substation: capacity expansion/construction          │
│  • Feeder: layout and sizing                            │
│  • DG (Wind/PV): siting and sizing                      │
│  • E-SOP (SOP + BESS): siting and sizing                │
│                                                         │
│  Constraints:                                           │
│  • Power balance (E-SOP + network)                      │
│  • Equipment capacity limits                            │
│  • Voltage/current limits                               │
│  • Network radiality and connectivity                   │
│  • BESS energy/power constraints                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  SCCR Algorithm                                         │
│  1. Initial SOCP relaxation                             │
│  2. Compute relaxation gap                              │
│  3. Add cutting-plane constraints                       │
│  4. Increase penalty coefficient                        │
│  5. Iterate until convergence (gap < ε)                │
│  6. Output optimal planning scheme                      │
└─────────────────────────────────────────────────────────┘
```

## WGAN-GP Architecture

### Generator Architecture
- Input: Random noise vector Z (128 dimensions)
- Fully Connected layer: FC, 256×6×6, with Batch Normalization (BN)
- Transposed Convolution (TCONV): 3×3, 256 filters, stride=2, padding=1, BN
- Transposed Convolution (TCONV): 3×3, 128 filters, stride=2, padding=1, BN
- Transposed Convolution (TCONV): 3×3, 64 filters, stride=1, padding=1, BN
- Transposed Convolution (TCONV): 3×3, 1 filter, stride=1, padding=1, Tanh activation
- Output: 24×24 wind–PV time series data

### Discriminator Architecture
- Input: 24×24 wind–PV time series
- Convolution (CONV): 3×3, 64 filters, stride=2, padding=1, LeakyReLU(0.2)
- Convolution (CONV): 3×3, 128 filters, stride=2, padding=1, BN
- Fully Connected: FC, 512, Dropout(0.3)
- Fully Connected: FC, 1
- Loss: Wasserstein Loss + Gradient Penalty (GP)

### Training Objective
```
min_G max_D V(G,D) = E[D(x)] - E[D(G(z))] + λ × E[(||∇_x̂ D(x̂)||_2 - 1)^2]
```
where λ is the gradient penalty coefficient.

## E-SOP Architecture

The E-SOP consists of:
- **SOP Unit**: Multiple bidirectional AC/DC converters with AC interfaces on the feeder side and interconnected DC sides via a shared DC bus
- **BESS Unit**: Connected to the shared DC bus, providing energy buffering capability

The E-SOP connects to three feeders (typically) and enables:
- **Spatial power flow regulation**: SOP controls bidirectional power flow between feeders
- **Temporal energy balancing**: BESS absorbs surplus power when DG output exceeds local demand and discharges to compensate when load is high or DG is insufficient

Candidate E-SOP branches: 6–26, 8–34, 9–22, 25–33, 38–32, 13–43, 46–50.

SOP unit rating: 100 kVA per unit
BESS total energy capacity limit: 6000 kWh
BESS total power capacity limit: 2000 kW

## Network Architecture

### Test System
- Modified Portuguese 54-bus distribution network [21]
- Four substations: S1 (existing, 16.7 MVA, expandable to 33.4 MVA), S2 (existing, 30 MVA, expandable +13.3 MVA), S3 (new, 22.2 MVA), S4 (new, 22.2 MVA)
- Feeder impedance: 0.307 + j0.380 Ω/km
- Feeder rated capacity: 6.12 MVA
- DG candidate nodes: PV at 10, 25, 38, 39, 46, 47; Wind at 24, 34, 37, 38, 39
- Maximum DG penetration: 60%
- Voltage range: [0.95, 1.05] p.u.
- Load power factor: 0.9
