# Figure 3: Network under examination

- **Source**: Figure 3, Section 4 (Network Under Examination), page 7
- **Caption**: "Network under examination."
- **Screenshot**: figure3.png (lower diagram on page 7, below Figure 2 and the "4. Network Under Examination" heading)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Six buses numbered 1–6 in a radial (tree) topology. Bus 1 is the substation /
  feeder source. Five distribution lines: L1 (bus 1–2), L2 (2–3), L3 (3–4), L4 (4–5), and a
  diagonal line labeled L5 ending at bus 6.
- **Connections**: A single main feeder runs 1→2→3→4→5 left to right. The diagonal L5 line **as
  drawn originates at bus 3** and descends to bus 6 (lower right). Power injections S_inj,2,
  S_inj,3, S_inj,4, S_inj,5, S_inj,6 are drawn as arrows at buses 2–6 (net injection = DER output
  minus load). DERs are integrated at buses 2, 3, and 4.
- **Internal inconsistency (figure vs table/prose)**: Table 1 lists L5 as "5–6" and the §4 prose
  states "each bus being connected to its upstream neighbor by a single distribution line" (a
  1–2–3–4–5–6 chain), but the figure draws the L5 diagonal starting at bus 3, not bus 5. The two
  sources conflict on L5's upstream endpoint; per Table 1 it is bus 5, per Figure 3 as drawn it is
  bus 3. Neither reading is silently preferred here.
- **Annotations**: Line labels L1–L5; injection labels S_inj,k at each load bus; radial layout with
  a single path from source to each load.
- **What it conveys**: The proof-of-concept test system — a simplified 6-bus radial feeder with
  unidirectional power flow from the substation, DERs at buses 2–4, used to demonstrate the GA
  framework. Line parameters in Table 1 (R/X/thermal) and bus loads in Table 2; see the
  inconsistency note above regarding L5's drawn endpoint.
- **Supports**: Grounds `logic/solution/architecture.md` (network topology); E01–E04 setup.
