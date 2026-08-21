# Grounding: reconstructed — from printed pseudocode (Algorithm 1), flowchart (Figure 7),
# and equations (Eqs. 16-38) of Demirbas et al., IEEE Access 2025, DOI 10.1109/ACCESS.2025.3544523.
# The paper releases no code; only the mechanism below is stated. Everything the paper does not
# specify is left as NotImplementedError. Do NOT treat this as runnable — it is a faithful stub of
# the novel mechanism (FDB placement + Elite-OBL seeding) on top of the base COA.

from __future__ import annotations
import numpy as np


def fdb_scores(P: np.ndarray, F: np.ndarray, best_idx: int, omega: float) -> np.ndarray:
    """Fitness-Distance Balance scores (Eqs. 24-28).

    SP_i = omega * normF_i + (1 - omega) * normD_i, where D_i is the Euclidean distance
    of candidate i to the current best P_best (Eq. 25). `omega` value is Not specified in paper.
    """
    d = np.sqrt(((P - P[best_idx]) ** 2).sum(axis=1))          # Eq. 25 distance vector D_P
    normF = _normalize(F)
    normD = _normalize(d)
    return omega * normF + (1.0 - omega) * normD                # Eq. 27


def _normalize(v: np.ndarray) -> np.ndarray:
    rng = v.max() - v.min()
    if rng == 0:
        return np.zeros_like(v)
    return (v - v.min()) / rng


def elite_obl_init(P: np.ndarray, lb: np.ndarray, ub: np.ndarray,
                   rng: np.random.Generator) -> np.ndarray:
    """Elite OBL opposition population (Eqs. 34-35) — the selected OBL5 seeding scheme.

    x_bar^E_ij = rand * (lb_j + ub_j) - x^E_ij  (Eq. 34)
    If x_bar^E_ij is out of [lb_j, ub_j], reset: x_bar^E_ij = rand * (ub_j - lb_j)  (Eq. 35)
    """
    r = rng.random(P.shape)
    opp = r * (lb + ub) - P                                     # Eq. 34
    out = (opp < lb) | (opp > ub)
    opp[out] = (rng.random(P.shape) * (ub - lb))[out]           # Eq. 35 reset within bounds
    return opp


def coa_initialize(N: int, m: int, lb: np.ndarray, ub: np.ndarray,
                   rng: np.random.Generator) -> np.ndarray:
    """Random COA population (Eq. 16): x_ij = lb_j + r*(ub_j - lb_j)."""
    r = rng.random((N, m))
    return lb + r * (ub - lb)


def fdbcoa_obl_step(X: np.ndarray, F: np.ndarray, iguana: np.ndarray,
                    lb: np.ndarray, ub: np.ndarray, t: int, T: int,
                    objective, omega: float, rng: np.random.Generator) -> np.ndarray:
    """One iteration of FDBCOA1 (FDB placed in the Stage-1 exploration update, Eq. 17).

    Phase 1 (Exploration), i = 1..N/2 — FDBCOA1 variant:
        compute FDB scores (Eq. 25, 27), pick x_FDB, then
        x_ij^{P1} = x_FDB_j + r*(Iguana_j - I*x_ij)              # FDBCOA1 form of Eq. 17
        greedy accept via Eq. 20.
    Phase 1, i = N/2+1..N: ground update Eq. 19 (FDBCOA2/3 place FDB here instead).
    Phase 2 (Exploitation): Eqs. 21-22 escape update, greedy accept Eq. 23.
    """
    N, m = X.shape
    best_idx = int(np.argmin(F))
    SP = fdb_scores(X, F, best_idx, omega)                      # Eqs. 24-28
    fdb_idx = int(np.argmax(SP))                                # candidate that is fit AND far
    x_fdb = X[fdb_idx]

    half = N // 2
    Xnew = X.copy()
    # --- Phase 1: exploration, tree-climbing coatis (FDBCOA1 uses x_fdb here) ---
    for i in range(half):
        I = rng.choice([1, 2])                                  # I in {1, 2}
        r = rng.random(m)
        cand = x_fdb + r * (iguana - I * X[i])                  # FDBCOA1 form of Eq. 17
        cand = np.clip(cand, lb, ub)
        Xnew[i] = _greedy(X[i], cand, F[i], objective)          # Eq. 20
    # --- Phase 1: ground coatis (Eq. 18-19). FDBCOA2/FDBCOA3 inject x_fdb in the branches. ---
    raise NotImplementedError(
        "Ground-coati update (Eq. 18-19), Phase-2 escape update (Eq. 21-23), the outer maxFEs "
        "loop, and the FDB weighting coefficient omega are not fully specified in the paper."
    )


def _greedy(x_old: np.ndarray, x_new: np.ndarray, f_old: float, objective) -> np.ndarray:
    """Greedy acceptance (Eq. 20 / Eq. 23): keep new position only if it improves the objective."""
    return x_new if objective(x_new) < f_old else x_old
