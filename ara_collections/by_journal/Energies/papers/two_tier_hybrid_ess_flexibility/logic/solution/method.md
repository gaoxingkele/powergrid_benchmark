# Method: PSO-VMD Hybrid ESS Power Allocation

## Purpose
Allocate the total energy storage system target power between lithium-ion batteries (short-duration) and flow batteries (long-duration) using frequency-based signal decomposition.

## Rationale
- High-frequency fluctuations (rapid, small energy) -> Li-ion batteries (millisecond response)
- Low-frequency fluctuations (slow, large energy) -> Flow batteries (large capacity, long duration)
- VMD provides mathematically rigorous decomposition superior to EMD (unique solutions, no mode mixing)
- PSO eliminates subjectivity in selecting VMD parameters (K and alpha)

## Step-by-Step Procedure

### Step 1: Parameter Optimization via PSO
**Decision variables**: Mode number K, penalty factor alpha
**Objective function** (composite loss, Equation 5):
```
Loss = (1/K*N) * sum(sum(x(t) - IMF_k(t))^2) + lambda * (K/N)
```
- First term: Full-band reconstruction Mean Square Error (MSE) normalized
- Second term: Penalty for modal redundancy (suppresses excessive K)
- lambda: Complexity penalty factor

### Step 2: VMD Decomposition
For each particle's (K, alpha) combination:

**Variational problem** (Equation 3):
```
min{ sum_k || d/dt[(delta(t) + j/(pi*t)) * u_k(t)] * e^(-j*omega_k*t) ||_2^2 }
s.t. sum_k u_k(t) = f(t)  // sum of modes = original signal
```

**Process**:
1. Hilbert transform to derive analytic signals
2. Shift to baseband using exponential tuning
3. Estimate bandwidth via squared L2 norm of demodulated signal gradient
4. Solve constrained variational problem iteratively

### Step 3: Centroid Frequency Computation (Equation 6)
For each IMF_k, compute center frequency:
```
f_ck = argmax{ Phi{IMF_k^2} }  for f in [0, fs/2]
```
Where Phi is the Fourier transform operator.

### Step 4: High/Low Frequency Separation
**Threshold**: Median frequency f_c_tilde = median of all {f_c1, f_c2, ..., f_cK}

**Assignment**:
```
High-frequency set: {IMF_k | f_ck > f_c_tilde} -> P_LiB(t)
Low-frequency set: {IMF_k | f_ck <= f_c_tilde} -> P_FB(t)
```

### Step 5: Signal Reconstruction
- High-frequency group summed -> Lithium-ion battery target power
- Low-frequency group summed with residual -> Flow battery target power

## VMD-PSO Algorithm Pseudocode (Algorithm 1)

```
Input: Total ESS power P_ESS, PSO parameters
Output: P_LIB (Li-ion power), P_FB (flow battery power)

1: Initialize PSO particles (K, alpha combinations)
2: while not converged do
3:    for each particle do
4:       Perform VMD with (K, alpha):
5:         Solve min{sum||d/dt[...]e^(-j*w*t)||^2} s.t. sum(u_k) = P_ESS
6:       Calculate composite loss = MSE + lambda*(K/N)
7:       Compute centroid frequency for each IMF
8:       Split components using median frequency threshold
9:    end for
10:   Update global best
11: end while
12: Reconstruct: high-freq -> P_LIB, low-freq -> P_FB
13: return P_LIB, P_FB
```

## Verification Metrics
- **Maximum reconstruction error**: 1.14e-13 (demonstrates near-perfect decomposition)
- **RMSE**: 4.74e-15 (demonstrates exceptional accuracy)
- **Mode count K for optimal performance**: 4 modes (IMF1-IMF4, progressively decreasing amplitudes)

## Advantages Claimed
1. Eliminates subjectivity in VMD parameter selection
2. Maintains physical integrity of output characteristics (suppresses spectral over-decomposition)
3. Achieves high tracking accuracy between frequency-divided output and target ESS power
