# Architecture — 6-Bus Radial Test Network

Source: §4 "Network Under Examination" (Figure 3, Tables 1–2, pp.7–8). Mirrors evidence/figures/
figure3.md.

## Components
- **Bus 1**: substation / feeder source (slack), voltage held at 1.00 pu. No load.
- **Buses 2–6**: load buses (constant-power residential/commercial/industrial), demand per Table 2.
- **DER units**: dispatchable controllable sources at **buses 2, 3, and 4**, providing real and
  reactive power within inverter limits.
- **Lines L1–L5**: radial branches — L1 (1–2), L2 (2–3), L3 (3–4), L4 (4–5), L5 (5–6, per
  Table 1). Each has resistance R, reactance X, and a 200 A thermal limit (Table 1). R and X
  increase monotonically downstream (L1 smallest → L5 largest).

## Connections / topology
- Radial (tree) structure: per Table 1 and the §4 prose ("each bus being connected to its upstream
  neighbor"), a single chain feeder 1→2→3→4→5→6.
- **Source conflict on L5's upstream endpoint**: Figure 3 as drawn shows the L5 diagonal
  originating at bus 3 (not bus 5) and ending at bus 6, contradicting Table 1's "5–6" listing and
  the chain prose. See evidence/figures/figure3.md; this ARA reports both readings without
  silently preferring one.
- Power flows unidirectionally from the substation outward; exactly one path from source to each load.
- Net bus injection S_inj,i (i = 2…6) = DER output − load; drawn as injection arrows in Figure 3.

## Control interface (what the GA manipulates)
- DER real/reactive setpoints (P_DER, Q_DER) at buses 2, 3, 4
- Voltage-regulator tap settings
- Radiality-preserving reconfiguration (switchable branch status)

## Key design choices
- Simplicity: a 6-bus radial feeder is used as a proof of concept because it is a standard minimal
  system for studying voltage profiles, loss minimization, and DER integration (§4, p.8).
- DERs sited mid-feeder (buses 2–4) rather than at the ends, giving the optimizer leverage over both
  the upstream and downstream sections.
- Implementation: power flow + GA in MATLAB R2025 and PowerFactory 2024 (§4, p.8).
