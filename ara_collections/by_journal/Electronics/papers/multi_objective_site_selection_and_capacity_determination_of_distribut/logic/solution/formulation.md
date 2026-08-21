# Multi-Objective Siting/Sizing Formulation (Eqs. 1–3, 6–9)

The planning problem is cast as the simultaneous minimization of three objective functions
over the EVS (electric vehicle station) siting and capacity decision variables, subject to the
EVS-cluster dispatchable-storage constraints. Source: §2 (Eqs. 1–3) and §4.2 (Eqs. 6–9).

## Decision variables
- Location of EV charging stations (EVS) on the network (node indices).
- Power/capacity of the EVS storage at the selected nodes.

Case bounds (§5, p.7): "The number of system nodes that can connect to EVS energy storage
ranges from 2 to 33, the maximum number of nodes that can be connected to EVS is 2, and the
maximum installed power is 400 kW."

## Objective 1 — Node voltage fluctuation (Eq. 1)

$$f_1 = \sum_{i=1}^{N_{bus}} \sum_{j=1}^{T} \left| V_{ij} - \bar{V}_i \right|$$

- $N_{bus}$: total number of nodes; $T$ = 24 h; $V_{ij}$: voltage between the nodes; $\bar{V}_i$: standard voltage.
- Rationale (§2, citing Ref. [10]): voltage stability is an important indicator of power-system
  stability; DG access influences node voltage by affecting the reactive-power balance. The sum of
  node voltage fluctuations is selected as objective f1 (a "vulnerability" proxy).

## Objective 2 — Network loss (Eq. 2)

$$f_2 = c_{loss} \sum_{t=1}^{T} \sum_{ij \in E_{line}} I_{ij,t}^2 \, r_{ij}$$

- $c_{loss}$: unit network loss cost; $E_{line}$: set of branches in the ADN; $I_{ij,t}$: branch
  current; $r_{ij}$: branch resistance.
- Rationale (§2): after large-scale DG is connected, reactive power may be insufficient; if the DG
  access location is far from the ADN main line, the electrical distance increases, raising network loss.

## Objective 3 — Energy-storage system capacity (Eq. 3)

$$f_3 = \sum_{j=1}^{2} \sum_{ij \in E_{line}}^{t_0 + n\Delta t} P_{cha}(j)/P_{dis}(j)\,\Delta t$$

- $t_0$: time when charging starts; $P_{cha/dis}$: charging and discharging power; $\Delta t$:
  charging/discharging time of the energy storage device. (The equation is transcribed as printed;
  the outer sum over $j = 1..2$ corresponds to the two storage devices; the inner summation bound as
  printed mixes the time bound $t_0 + n\Delta t$ with the branch-set subscript.)
- Rationale (§2): to avoid large investment and low utilization of storage capacity in the early
  ADN construction stage, total storage capacity is minimized so cost, contribution to network
  loss, and voltage stability "can be balanced by a multi-objective algorithm".

## EVS cluster dispatchable-storage constraints (Eqs. 6–9, §4.2, per Refs. [31,32])

**SOC dynamics (Eq. 6)** — total SOC of the EVs in the charging station; charging/discharging
status determined using historical data:

$$S_t^{EVS} = S_{t-1}^{EVS} + \sum_{i=1}^{T}\sum_{n=1}^{N} \eta P_{cha} - \sum_{i=1}^{T}\sum_{n=1}^{N} \frac{P_{dis}}{\eta}$$

**Expected end-state SOC (Eq. 7)**:

$$S_T^{EVS} = S_{exp}^{EVS}$$

**SOC band (Eq. 8)**:

$$S_{min}^{EVS} \le S_t^{EVS} \le S_{max}^{EVS}$$

**Charge/discharge power limits (Eq. 9)**:

$$0 \le P_{cha} \le P_{cha,max}, \qquad 0 \le P_{dis} \le P_{dis,max}$$

- $S_t^{EVS}$: power level of the EVS at time t; $N$: total number of EVs; $\eta$:
  charge–discharge efficiency; $P_{cha}$/$P_{dis}$: charging/discharging power; $S_{exp}^{EVS}$:
  expected amount of power; $S_{min}^{EVS}$, $S_{max}^{EVS}$: allowable scope of SOC;
  $P_{cha,max}$, $P_{dis,max}$: allowable range of charge and discharge power (allowable ranges
  per Ref. [33]).
- Modeling assumption (§4.2): each EV type has a fixed arrival and departure time
  $T_{arrive}/T_{leave}$ and initial state of charge $S_0$ (sampling distributions in Table A1).

## What the formulation deliberately couples
Siting and power of EV charging stations are optimized **jointly** with network loss and node
voltage fluctuation ("When determining the location and capacity of EV charging stations in ADN,
it is necessary to optimize the location and power of EV charging stations. In addition, the
network loss and node voltage fluctuation of ADNs should be also taken into account." — §2).
Numerical parameter values ($c_{loss}$, $\eta$, SOC bounds, $P_{cha,max}$/$P_{dis,max}$) are
not specified in the paper. Supports claims C01, C02, C05.
