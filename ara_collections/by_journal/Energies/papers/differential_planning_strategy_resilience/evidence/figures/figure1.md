# Figure 1: Sampling Process of Wind Speed Scenarios and Corresponding Failure States

- **Source**: Page 5, Section 2.2
- **Screenshot**: `figure1.png`
- **Figure type**: diagram
- **Extraction method**: exact_from_labels
- **Reading confidence**: high
- **Claims supported**: C01
- **Visual description**: Flow diagram showing the sampling pipeline for generating line failure states from wind speed scenarios. Process: generate G wind speed scenarios through random sampling -> each corresponds to a typhoon wind field -> apply wind field attenuation algorithm -> obtain time-series wind speed v^k_t for each scenario at each time t -> compute instantaneous failure probability p^d,k,s_{ij,t} via Equation (5) -> sample failure state chi^d,k,s_{ij,t} via Equation (6).
- **Key insight**: The sampling process connects disaster intensity (wind speed) to line-level failure states through the vulnerability curve (Equation 5), establishing the physical basis for the DDU model where the hardening level d controls the hardening coefficient alpha_d.
