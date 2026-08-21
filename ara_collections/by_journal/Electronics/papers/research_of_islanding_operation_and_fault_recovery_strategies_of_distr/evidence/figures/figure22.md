# Figure 22: Node voltage waveform for time period 1

**Source**: Figure 22, Section 6 (Experiment), pages 25-26
**Location on page**: figure spans page 25 (top panels, "Figure 22. Cont.") and page 26 (remaining
panels + final caption at bottom of page 26). Screenshot = page 26 (carries the main caption).
**Caption**: "Node voltage waveform for time period 1."
**Screenshot**: figure22.png
**Figure type**: qualitative_sample
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
- **Shows**: oscilloscope screen captures of node voltage waveforms during Island 2 islanding
  operation (time period 1), from the OPAL-RT + DSP semi-physical setup. Multiple 4-channel screens,
  each with Node 24 (blue) as phase-reference plus three other nodes (e.g. Node2/3/4, Node5/6/7,
  Node22/23, Node25/26). Channel scale 2.00 V/div.
- **Demonstrates**: after the fault, the islanded system operates stably — near-sinusoidal waveforms,
  voltage frequency near 50 Hz, node voltages ≈1.082-1.099 pu, phase angles between -10.09° and 0°
  (per text). Some channels show a flat line = "no signal access" (that node not in this island / not
  measured).
- **Supports**: C (semi-physical validation of stable islanded operation); gap on real-time
  feasibility. Qualitative evidence that the DSP-issued islanding strategy yields limit-compliant,
  stable node voltages in hardware-in-the-loop.
