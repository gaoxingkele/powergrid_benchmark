# Grounding: reconstructed — from explicit paper equations §3.3.1, Eqs. (26)-(31).
# Reconstructs ONLY the improved-PSO update mechanism whose equations the paper prints.
# The objective evaluation (the bi-level upper-objective F1/F2 with a CPLEX lower-level
# solve) is NOT specified as code in the paper and is left as NotImplementedError.
# No API names, constants, or hyperparameters are invented beyond what the equations state.

import numpy as np


def inertia_weight(t, T, w_max, w_min):
    """Adaptive inertia weight, Eq. (26):
        w = w_max * ((t-1)/(T-1))**cos(t/T) * (w_max - w_min)
    t: current iteration (1-indexed), T: max iterations.
    w_max, w_min: NOT specified numerically in paper (see logic/solution/algorithm.md).
    """
    return w_max * ((t - 1) / (T - 1)) ** np.cos(t / T) * (w_max - w_min)


def learning_factors(t, T):
    """Sine-function learning factors, Eq. (27):
        c1 = 2*sqrt(1 - |sin(pi/2 * t/T)|)   (cognitive)
        c2 = 2*sqrt(   |sin(pi/2 * t/T)| )   (social)
    """
    s = abs(np.sin(np.pi / 2 * t / T))
    c1 = 2 * np.sqrt(1 - s)
    c2 = 2 * np.sqrt(s)
    return c1, c2


def update_subpop1(x, v, w, c1, c2, p_best, g_best):
    """Standard PSO update, Eq. (28). r1, r2 ~ U[0,1]."""
    r1, r2 = np.random.rand(*x.shape), np.random.rand(*x.shape)
    v_new = w * v + c1 * r1 * (p_best - x) + c2 * r2 * (g_best - x)
    x_new = x + v_new
    return x_new, v_new


def update_subpop2(x, v, w, c1, p_best):
    """Cognitive-only velocity update, Eq. (29)."""
    r1 = np.random.rand(*x.shape)
    v_new = w * v + c1 * r1 * (p_best - x)
    return x + v_new, v_new


def update_subpop3(x, v, w, c2, g_best):
    """Social-only velocity update, Eq. (30)."""
    r2 = np.random.rand(*x.shape)
    v_new = w * v + c2 * r2 * (g_best - x)
    return x + v_new, v_new


def update_subpop4(x, t, T):
    """Sine positional perturbation, Eq. (31):
        x_{i}^{t+1} = (1 + a*sin(pi/2 * t/T)) * x_i^t,  a ~ U(0,1)
    """
    a = np.random.rand(*x.shape)
    return (1 + a * np.sin(np.pi / 2 * t / T)) * x


def evaluate_upper_objective(positions):
    """Upper-level objectives F1 (Eq. 7) and F2 (Eq. 11), each particle position
    requiring a CPLEX lower-level solve (Eq. 19, 21). Not specified as code in paper."""
    raise NotImplementedError("Not specified in paper")
