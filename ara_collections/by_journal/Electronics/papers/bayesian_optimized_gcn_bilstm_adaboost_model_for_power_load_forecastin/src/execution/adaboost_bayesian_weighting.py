# Grounding: reconstructed — from explicit paper pseudocode/equations (§2.4 Steps 1–4, Eqs 11–19; §2.5)
"""Modified AdaBoost + Monte Carlo Dropout uncertainty weighting.

Reconstructed strictly from the printed algorithm in:
  Li, Li, Li, Zhang, "Bayesian-Optimized GCN-BiLSTM-Adaboost Model for Power-Load
  Forecasting," Electronics 2025, 14, 3332.
  - §2.4 AdaBoost Algorithm, Steps 1–4, Eqs (11)–(16)
  - §2.5 Bayesian Method, Eqs (17)–(19)

Only content the paper specifies is implemented. The GCN-BiLSTM base learner internals
(Eqs 1–10) and the exact training/tensor plumbing are NOT specified in enough detail to
transcribe, and are left as NotImplementedError. No API names, bodies, or constants are
invented beyond the printed constants (0.3, 1.1, 0.5, K=10, T=100, m=1200).
"""
from __future__ import annotations
from typing import Protocol, Sequence
import numpy as np

# ---- Printed constants (§2.4–2.5, Table 3 / §4.2) ----
ERROR_THRESHOLD: float = 0.3   # §2.4: up-weight only samples with e_i > 0.3
UPWEIGHT_FACTOR: float = 1.1   # Eq (14): D_{k+1}(i) = D_k(i) * 1.1
ALPHA_NUMERATOR: float = 0.5   # Eq (13): alpha_k = 0.5 / exp(weight_sum)
NUM_LEARNERS: int = 10         # §2.4: 10 weak learners
NUM_MC_SAMPLES: int = 100      # §2.5: 100 stochastic dropout predictions


class GcnBiLstmWeakLearner(Protocol):
    """A single GCN-BiLSTM base learner (Eqs 1–10). Internals not specified in paper."""

    def fit(self, X, y, sample_weight) -> None: ...
    def predict(self, X): ...
    def predict_mc(self, X, n_samples: int):
        """Return an array of `n_samples` stochastic (dropout-on) predictions per input."""
        ...


def sample_error(y_true, y_pred):
    """Eq (11): e_i = |y_hat_i - y_i|."""
    return np.abs(np.asarray(y_pred) - np.asarray(y_true))


def learner_weight(sample_weights, errors):
    """Eqs (12)-(13).

    weight_sum = sum_{i | e_i > 0.3} D_k(i)
    alpha_k    = 0.5 / exp(weight_sum)
    """
    mask = np.asarray(errors) > ERROR_THRESHOLD
    weight_sum = float(np.asarray(sample_weights)[mask].sum())
    return ALPHA_NUMERATOR / np.exp(weight_sum)


def update_sample_weights(sample_weights, errors):
    """Eqs (14)-(16): x1.1 for hard samples, unchanged otherwise, then normalize to sum 1."""
    D = np.asarray(sample_weights, dtype=float).copy()
    hard = np.asarray(errors) > ERROR_THRESHOLD
    D[hard] *= UPWEIGHT_FACTOR                      # Eq (14); Eq (15) leaves the rest unchanged
    return D / D.sum()                              # Eq (16)


def adaboost_train(learners: Sequence[GcnBiLstmWeakLearner], X, y, m: int = 1200):
    """AdaBoost training phase (§2.4, Steps 1–4).

    Returns the per-learner (un-normalized) training weights W_m = alpha_k.
    NOTE: learner.fit and the GCN-BiLSTM architecture are NOT specified in the paper.
    """
    D = np.full(m, 1.0 / m)                          # Step 1: D_1(i) = 1/m
    W = np.zeros(len(learners))
    for k, learner in enumerate(learners):
        learner.fit(X, y, sample_weight=D)           # Step 2 (training not specified)
        raise NotImplementedError("Not specified in paper")  # weak-learner training loop
        # The following would run once fit/predict were defined:
        # e = sample_error(y, learner.predict(X))     # Eq (11)
        # W[k] = learner_weight(D, e)                  # Eq (13)
        # D = update_sample_weights(D, e)              # Eqs (14)-(16)
    return W


def mc_dropout_uncertainty(learner: GcnBiLstmWeakLearner, X, n_samples: int = NUM_MC_SAMPLES):
    """Eq (17): Uncertainty = (1/100) * sum_n (y_n - y_bar)^2, over dropout passes."""
    samples = np.asarray(learner.predict_mc(X, n_samples))  # shape (n_samples, ...)
    y_bar = samples.mean(axis=0)
    variance = ((samples - y_bar) ** 2).mean(axis=0)         # per-input predictive variance
    return y_bar, variance


def attenuate_and_normalize(W_m, uncertainty):
    """Eqs (18)-(19): W'_m = W_m / (1 + uncertainty); W''_m = W'_m / sum_m W'_m."""
    W_prime = np.asarray(W_m, dtype=float) / (1.0 + np.asarray(uncertainty, dtype=float))  # Eq 18
    return W_prime / W_prime.sum()                                                          # Eq 19


def ensemble_forecast(learners, X, W_train):
    """Bayesian testing phase (§2.5): per-learner MC mean + variance -> attenuated weighted sum."""
    means, variances = [], []
    for learner in learners:
        y_bar, var = mc_dropout_uncertainty(learner, X)      # Eq (17)
        means.append(y_bar)
        variances.append(float(np.mean(var)))                # scalar reliability proxy per learner
    W_final = attenuate_and_normalize(W_train, variances)    # Eqs (18)-(19)
    return np.tensordot(W_final, np.asarray(means), axes=1)  # weighted sum of learner means
    # A 95% predictive interval (Fig 12) is formed from the pooled dropout samples;
    # the exact banding procedure is not specified in the paper.
