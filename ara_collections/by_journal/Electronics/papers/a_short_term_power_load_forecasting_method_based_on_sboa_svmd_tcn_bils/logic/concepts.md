# Concepts

## Successive Variational Mode Decomposition (SVMD)
- **Notation**: f(t) = µ_L(t) + f_r(t)
- **Definition**: A signal-decomposition method that applies VMD successively, extracting and removing one mode µ_L(t) at a time (with residual f_r(t) split into processed modes and the unprocessed part), without presetting the number of modes K. Mode extraction is cast as minimizing {η·J1 + J2 + J3} subject to reconstruction (Eqs. 1–8): J1 keeps each mode compact around its center frequency ω_L, J2 minimizes spectral overlap of residual and mode, J3 separates the L-th mode from earlier modes.
- **Boundary conditions**: Reduces mode mixing and computational cost vs VMD; still requires setting the mode-compactness coefficient (this paper optimizes it). Source §2.1.
- **Related concepts**: VMD, EMD, IMF, Mode compactness (maxAlpha)

## Secretary Bird Optimization Algorithm (SBOA)
- **Notation**: X_{i,j} = ll_j + r·(ul_j − ll_j)
- **Definition**: A population-based metaheuristic modeled on secretary-bird behavior. Each iteration runs two phases: (1) a Hunting phase split into three equal iteration intervals — searching (differential-evolution mutation, Eq. 12), consuming (Brownian motion around x_best, Eq. 15), attacking (Lévy flight with a nonlinear perturbation factor, Eq. 17); and (2) an Escape phase choosing camouflage C1 or escape C2 (Eq. 22) via a rand>0.5 gate. Positions update greedily (accept only if fitness improves).
- **Boundary conditions**: Used here only to optimize one scalar (SVMD maxAlpha); objective = minimum permutation entropy. Source §2.2, ref [29].
- **Related concepts**: SSA, GWO, Lévy flight, Permutation entropy

## Temporal Convolutional Network (TCN)
- **Notation**: F(t) = Σ_{i=0}^{k−1} f(i)·x_{t−p·i}  (Eq. 25)
- **Definition**: A CNN-based sequence model using dilated causal convolutions and residual blocks. Causal convolution makes output y_t depend only on inputs at times ≤ t (no future leakage); dilation factor p grows across layers (1→2→4) to enlarge the receptive field without pooling/information loss. Residual unit stacks dilated-causal-conv → weight norm → ReLU → dropout (×2) plus a skip connection, f(x)=h(x)−x (Eq. 26).
- **Boundary conditions**: Captures long-range and multi-scale local features; may under-capture global context alone. Source §3.1.
- **Related concepts**: Dilated causal convolution, Residual unit, CNN, BiLSTM

## Bidirectional Long Short-Term Memory (BiLSTM)
- **Notation**: i_t, f_t, o_t, c_t, h_t (Eqs. 27–32); forward h_t and backward h_i states
- **Definition**: Two LSTM chains processing the sequence forward and backward; each hidden layer combines the current input with both the previous forward state and the previous backward state, so predictions use past and future context. LSTM base cell uses input/forget/output gates and a tanh candidate to regulate a cell state.
- **Boundary conditions**: Richer context than unidirectional LSTM but higher compute/storage on very long sequences. Source §3.2.
- **Related concepts**: LSTM, GRU, TCN

## Intrinsic Mode Function (IMF)
- **Notation**: IMF1 … IMF4
- **Definition**: A single-frequency sub-sequence produced by decomposition. Here SVMD yields four: IMF1 ≈ trend (weak volatility, no zero-crossing), IMF2 = low-frequency periodic component, IMF3–IMF4 = higher-frequency, weaker-periodicity components representing regularity plus anomalies/sudden events.
- **Boundary conditions**: Count (4) is an outcome of the optimized decomposition on this dataset, not preset. Source §5.3.
- **Related concepts**: SVMD, VMD, EMD

## Mode compactness coefficient (maxAlpha)
- **Notation**: α / maxAlpha (compactness of mode = 19,990.25 optimized)
- **Definition**: The SVMD bandwidth/compactness parameter governing how tightly each mode concentrates around its center frequency; too small over-disperses modes, too large over-concentrates. Optimized by SBOA to minimize component permutation entropy.
- **Boundary conditions**: Dominant SVMD parameter; other SVMD params set empirically. Source §2.2, Table 1.
- **Related concepts**: SVMD, Permutation entropy, SBOA

## Permutation entropy
- **Notation**: PE ∈ [0, 1]
- **Definition**: A complexity measure of a time series; lower values indicate lower complexity and higher predictability, values near 1 indicate high complexity/low predictability. Used as the SBOA objective (minimize) and to compare decomposition/optimizer quality.
- **Boundary conditions**: Used as a predictability proxy (assumption A1). Source §5.3, refs [30,31].
- **Related concepts**: SVMD, SBOA, IMF

## Decomposition–prediction–reconstruction framework
- **Notation**: —
- **Definition**: The overall paradigm: decompose the load into IMFs, forecast each IMF independently, then reconstruct (sum / "hybrid computation") the component forecasts into the final prediction.
- **Boundary conditions**: The organizing framework of the whole pipeline. Source §4, §7, Figure 8.
- **Related concepts**: SVMD, TCN-BiLSTM, IMF
