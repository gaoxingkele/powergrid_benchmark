# Figure 7 - IEEE 33-Bus Voltage Profile with Integrated DGs and EVCSs

**Source**: Figure 7, Section 5.1.1
**Caption**: IEEE-33 bus voltage profile with integrated DGs and EVCSs.
**Screenshot**: figure7.png
**Figure type**: quantitative_plot
**Extraction method**: visual_description
**Reading confidence**: low

- **Plot kind**: line
- **Axes**: X = Bus number (1-33, linear), Y = Voltage (p.u., linear)

## Visual description
The figure shows voltage profiles across the 33 buses for:
1. Base case (no integration)
2. HF = 30%
3. HF = 40%
4. HF = 50%

The base case voltage drops below 0.92 p.u. at bus 18 and further to approximately 0.9038 p.u. at the farthest bus. All CGO-integrated cases show significantly improved voltage profiles, with all voltages remaining above approximately 0.96 p.u. across all buses. Higher EV penetration (50% HF) shows slightly lower voltages than 30% HF, particularly toward feeder ends (buses 14-18 and the branch around bus 30-33).

## Trend summary
All three CGO profiles are substantially flatter than the base case. The improvement is most dramatic at buses 14-18 and 30-33 where base-case voltages were lowest. Marginal voltage degradation is visible as EV penetration increases from 30% to 50%, confirming the literature observation that higher EV loading increases voltage drop.
