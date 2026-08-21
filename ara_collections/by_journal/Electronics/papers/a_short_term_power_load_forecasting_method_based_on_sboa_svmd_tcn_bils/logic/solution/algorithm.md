# Algorithm — SBOA-optimized SVMD

Covers the two novel algorithmic pieces: (A) SVMD mode extraction and (B) SBOA optimizing SVMD's compactness parameter. Neural-net forward passes (TCN/BiLSTM) are standard and specified in architecture.md.

## A. SVMD mode extraction (§2.1, Eqs. 1–8)

### Mathematical formulation
Decompose input f(t) = µ_L(t) + f_r(t), where µ_L(t) is the L-th mode and f_r(t) the residual (processed modes Σ_{i=1}^{L−1} u_i(t) plus unprocessed f_u(t)).

Constraints:
- Compactness of L-th mode around center frequency ω_L:
  J1 = ‖ ∂_t[ (δ(t) + j/(πt)) * µ_k(t) ] e^{−jω_L t} ‖₂²   (Eq. 2)
- Filter minimizing residual/mode spectral overlap: β̂_L(ω) = 1 / (α(ω − ω_L)²)   (Eq. 3);
  J2 = ‖ β_L(ω) × f_r(t) ‖₂²   (Eq. 4)
- Separation from earlier modes via β̂_i(ω) = 1/(α(ω − ω_i)²), i=1..L−1   (Eq. 5);
  J3 = Σ_{i=1}^{L−1} ‖ β_i(ω) × µ_L(t) ‖₂²   (Eq. 6)
- Reconstruction: f(t) = µ_L(t) + f_u(t) + Σ_{i=1}^{L−1} u_i(t)   (Eq. 7)

Objective:
  min { η·J1 + J2 + J3 }  s.t.  u_L(t) + f_r(t) = f(t)   (Eq. 8)
where η balances the three terms, α is the bandwidth/compactness parameter (maxAlpha).

### Procedure (Figure 1)
1. Initialize SVMD parameters.
2. Decompose the data; extract global signal features; compute each mode's center frequency.
3. If the modal center frequency component is below the intrinsic-mode-component threshold → sum extracted IMFs to reconstruct; else reinitialize parameters and re-decompose.
4. Repeat until the condition is met.

### Complexity
Not specified in paper (states only that SVMD "significantly reduces computational complexity" vs VMD).

## B. SBOA optimizing SVMD compactness (§2.2, Eqs. 9–24)

### Objective
Minimize the permutation entropy of the SVMD-decomposed components by choosing the compactness coefficient maxAlpha (a 1-D search here). Population 30, 60 iterations.

### Initialization
X_{i,j} = ll_j + r·(ul_j − ll_j),  i=1..N, j=1..Dim   (Eq. 9); population matrix X (Eq. 10); fitness vector F = [F(X_1)…F(X_N)]ᵀ (Eq. 11).

### Per-iteration update — Hunting phase (three equal intervals)
- Searching (t < T/3), differential evolution:
  x_{i,j}^{newP1} = x_{i,j} + (x_{random_1} − x_{random_2})·R1   (Eq. 12); greedy accept (Eq. 13).
- Consuming (T/3 < t < 2T/3), Brownian motion RB = randn(1,Dim) (Eq. 14):
  x_{i,j}^{newP1} = x_best + exp((t/T)^4)·(RB − 0.5)·(x_best − x_{i,j})   (Eq. 15); greedy accept (Eq. 16).
- Attacking (t > 2T/3), Lévy flight with nonlinear factor:
  x_{i,j}^{newP1} = x_best + ((1 − t/T)^{(2·t/T)})·x_{i,j}·RL   (Eq. 17); greedy accept (Eq. 18),
  where RL = 0.5·Levy(Dim) (Eq. 19), Levy(D) = s·(u·σ)/|v|^{1/η} (Eq. 20), s=0.01, η=1.5,
  σ = [ Γ(1+η)·sin(πη/2) / (Γ((1+η)/2)·η·2^{((η−1)/2)}) ]^{1/η}   (Eq. 21).

### Per-iteration update — Escape phase (Eq. 22)
- C1 (camouflage, if rand < r_i): x_{i,j}^{new,P2} = x_best + (2·RB − 1)·(1 − t/T)²·x_{i,j}
- C2 (escape, else): x_{i,j}^{new,P2} = x_{i,j} + R2·(x_random − K·x_{i,j})
  with r_i = 0.5, K = round(1 + rand(1,1)) (Eq. 24); greedy accept (Eq. 23).

### Procedure (Figure 2)
1. Initialize parameters; evaluate fitness; find best position.
2. Hunting: by interval of t/T, update Xi via Eq. 12 / 15 / 17.
3. Escape: if rand > 0.5 use C1 else C2 (Eq. 22).
4. Update Xi and x_best; if max iterations reached output x_best, else return to step 2.

### Complexity
Not specified in paper.

## Pseudocode note
No printed pseudocode listing (algorithm given as equations + flowcharts). Steps above are reconstructed from the paper's stated equations and Figures 1–2; no code is transcribed (see src/environment.md — no released implementation).
