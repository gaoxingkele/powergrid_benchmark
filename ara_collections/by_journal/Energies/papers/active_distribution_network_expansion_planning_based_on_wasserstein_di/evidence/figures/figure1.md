# Figure 1: Access mode of SOP and interconnection switch

- **Source**: Figure 1, Section 2.1 (Principle and Physical Model of SOP and Interconnection Switch)
- **Caption**: "Access mode of SOP and interconnection switch."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two panels, each showing two radiating feeders F1 and F2 joined between them. Each feeder carries four sectionalizing switches labelled S11, S12, S22, S21 with intermediate nodes (dots).
  - Top panel: a two-port SOP (drawn as back-to-back AC/DC–DC/AC converters) is installed between F1 and F2, in the mid position.
  - Bottom panel: an interconnection switch (a mechanical tie switch symbol) is installed in the same mid position between F1 and F2.
- **Connections**: F1 (left) — S11 — node — S12 — [SOP or Interconnection Switch] — S22 — node — S21 — F2 (right).
- **Annotations**: "SOP" label (red) over the converter pair; "Interconnection Switch" label (red) under the tie switch.
- **What it conveys**: Both devices occupy the same tie position between two feeders, but the SOP is a full-controlled power-electronic device (back-to-back voltage-source converters) that continuously controls active and reactive port power, whereas the interconnection switch only sets the on/off state of the branch. This is the physical basis for treating them as alternative "flexible vs rigid" regulation options in the collaborative planning model.

Mirrored into `logic/solution/method.md` (device model) and `logic/concepts.md` (SOP, Interconnection switch).
