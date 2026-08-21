# Figure 21: Semi-physical experiment framework

**Source**: Figure 21, Section 6 (Experiment), page 24
**Location on page**: middle-lower half of page 24
**Caption**: "Semi-physical experiment framework."
**Screenshot**: figure21.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Components**:
  1. OPAL-RT real-time simulator hosting the "Distribution Network Environment" (the improved
     IEEE 33-node network with the S28 fault and the two islands).
  2. DSP controller = "Islanding operation and fault recovery controller" implementing the proposed
     strategy.
  3. Oscilloscope for observing node voltage waveforms.
- **Connections**:
  - OPAL-RT --(Analog Output, P, Q, ...)--> DSP controller.
  - DSP controller --(Digital input, Switch signals)--> OPAL-RT.
  - OPAL-RT --(Analog Output, v_Node)--> Oscilloscope.
- **What it conveys**: hardware-in-the-loop validation setup: the DSP detects the fault, issues
  switching signals to partition the network, each island runs the proposed islanding strategy, and
  node voltages are observed on the oscilloscope (Figures 22-24). Establishes the environment behind
  the semi-physical validation claim.

Structure mirrored into src/environment.md (semi-physical HIL platform).
