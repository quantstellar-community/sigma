"""HMM regime layer (WP-4b, ADR-0009).

The research center of Sigma: infer latent market regimes from log returns,
characterize them statistically, assign financial labels AFTER measurement,
and select the number of regimes by evidence (BIC + stability).
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module

import numpy as np

from sigma.modeling.errors import ModelingError

__all__ = [
    "GaussianParams",
    "KSelection",
    "RegimeCharacterization",
    "RegimeFit",
    "characterize_regimes",
    "fit_regime_model",
    "label_regimes",
    "select_k",
]

_TRADING_DAYS = 252
_MIN_OBS_PER_REGIME = 20
_DEFAULT_SEED = 42
_MAX_STABILITY_RELABEL_TRIES = 5


@dataclass(frozen=True)
class GaussianParams:
    mean: float
    std: float


@dataclass(frozen=True)
class RegimeFit:
    """Fitted HMM with full provenance."""

    k: int
    state_probabilities: np.ndarray  # (T, k) filtered probabilities
    most_likely_states: np.ndarray  # (T,) Viterbi path
    emissions: dict[int, GaussianParams]
    transition_matrix: np.ndarray  # (k, k)
    dataset_id: str


@dataclass(frozen=True)
class RegimeCharacterization:
    """Statistical profile of each ACTIVE regime, measured AFTER the fit.

    States that received no observations during the fit are excluded
    (an empty state is not a regime — it is a modeling artifact).
    """

    annualized_vol: dict[int, float]
    mean_return: dict[int, float]
    skewness: dict[int, float]
    kurtosis: dict[int, float]
    duration: dict[int, float]

    @property
    def active_states(self) -> tuple[int, ...]:
        return tuple(sorted(self.annualized_vol))


@dataclass(frozen=True)
class KSelection:
    """Evidence-based choice of the number of regimes."""

    best_k: int
    bic_by_k: dict[int, float]
    stability_by_k: dict[int, float]
    recommendation: str


def _validate_inputs(returns: np.ndarray, k: int) -> np.ndarray:
    values = np.asarray(returns, dtype=float)
    if values.ndim != 1 or len(values) < 2 * _MIN_OBS_PER_REGIME:
        msg = f"need a 1-D return series with at least {2 * _MIN_OBS_PER_REGIME} observations"
        raise ModelingError(msg)
    if not np.all(np.isfinite(values)):
        msg = "return series contains non-finite values"
        raise ModelingError(msg)
    if k < 2:
        msg = f"k must be at least 2, got {k}"
        raise ModelingError(msg)
    if len(values) < k * _MIN_OBS_PER_REGIME:
        msg = f"series too short for k={k}: need >= {k * _MIN_OBS_PER_REGIME} observations"
        raise ModelingError(msg)
    return values


def fit_regime_model(
    returns: np.ndarray,
    *,
    k: int,
    dataset_id: str,
    seed: int = _DEFAULT_SEED,
) -> RegimeFit:
    """Fit a Gaussian HMM with ``k`` hidden states on log returns.

    Deterministic given a fixed seed (ADR-0009 D5).
    """
    values = _validate_inputs(returns, k)

    hmmlearn = import_module("hmmlearn.hmm")

    # hmmlearn does not support multi-init like sklearn's GaussianMixture;
    # we run several deterministic initialisations (fixed seed sequence)
    # and keep the best-scoring fit. This reduces local-optimum traps
    # while staying reproducible (ADR-0009 D5).
    best_model = None
    best_score = -np.inf
    for init_seed in range(seed, seed + 5):
        candidate = hmmlearn.GaussianHMM(
            n_components=k,
            covariance_type="full",
            random_state=init_seed,
            n_iter=200,
            tol=1e-4,
        )
        candidate.fit(values.reshape(-1, 1))
        score = candidate.score(values.reshape(-1, 1))
        if score > best_score:
            best_score = score
            best_model = candidate
    assert best_model is not None
    model = best_model

    states = model.predict(values.reshape(-1, 1))
    probabilities = model.predict_proba(values.reshape(-1, 1))

    if not np.all(np.isfinite(states)) or not np.all(np.isfinite(probabilities)):
        msg = (
            f"HMM fit produced non-finite states/probabilities for k={k} "
            f"on {len(values)} observations; the model did not converge. "
            "Provide more data or try a different k."
        )
        raise ModelingError(msg)

    emissions: dict[int, GaussianParams] = {}
    for state in range(k):
        mask = states == state
        if mask.any():
            state_returns = values[mask]
            emissions[state] = GaussianParams(
                mean=float(np.mean(state_returns)),
                std=float(np.std(state_returns, ddof=1)),
            )

    return RegimeFit(
        k=k,
        state_probabilities=probabilities,
        most_likely_states=states,
        emissions=emissions,
        transition_matrix=np.asarray(model.transmat_),
        dataset_id=dataset_id,
    )


def characterize_regimes(
    fit: RegimeFit,
    *,
    returns: np.ndarray,
) -> RegimeCharacterization:
    """Measure the financial profile of each regime from the assigned data."""
    values = np.asarray(returns, dtype=float)
    if len(values) != len(fit.most_likely_states):
        msg = "returns length does not match fitted states length"
        raise ModelingError(msg)

    annualized_vol: dict[int, float] = {}
    mean_return: dict[int, float] = {}
    skewness: dict[int, float] = {}
    kurtosis: dict[int, float] = {}
    duration: dict[int, float] = {}

    for state in range(fit.k):
        mask = fit.most_likely_states == state
        if mask.sum() < 2:
            # empty or single-observation state: artifact, not a regime
            continue
        state_returns = values[mask]
        std = float(np.std(state_returns, ddof=1))
        annualized_vol[state] = std * np.sqrt(_TRADING_DAYS)
        mean_return[state] = float(np.mean(state_returns))
        skewness[state] = float(
            _moments_ratio(state_returns - mean_return[state], 3, std)
        )
        kurtosis[state] = float(
            _moments_ratio(state_returns - mean_return[state], 4, std)
        )
        persistence = float(np.diag(fit.transition_matrix)[state])
        duration[state] = (
            float(1.0 / (1.0 - persistence)) if persistence < 1.0 else float("inf")
        )

    return RegimeCharacterization(
        annualized_vol=annualized_vol,
        mean_return=mean_return,
        skewness=skewness,
        kurtosis=kurtosis,
        duration=duration,
    )


def _moments_ratio(centered: np.ndarray, power: int, std: float) -> float:
    if std == 0:
        return 0.0
    return float(np.mean(centered**power) / std**power)


def label_regimes(
    characterization: RegimeCharacterization,
) -> dict[int, str]:
    """Assign financial labels AFTER measurement, never before (ADR-0008 §3).

    Rules:
    - state with the LOWEST annualized vol  -> "Calm"
    - state with the HIGHEST annualized vol -> "Crisis"
    - any remaining states                  -> "Volatile"
    """
    ordered = sorted(
        characterization.active_states,
        key=lambda state: characterization.annualized_vol[state],
    )
    if not ordered:
        msg = "no active regimes to label"
        raise ModelingError(msg)
    if len(ordered) == 2:
        labels = {ordered[0]: "Calm", ordered[1]: "Crisis"}
    else:
        labels = {ordered[0]: "Calm", ordered[-1]: "Crisis"}
        for state in ordered[1:-1]:
            labels[state] = "Volatile"
    return labels


def select_k(
    returns: np.ndarray,
    *,
    candidates: tuple[int, ...],
    dataset_id: str,
    seed: int = _DEFAULT_SEED,
) -> KSelection:
    """Choose the number of regimes by BIC + stability evidence (ADR-0009 D4)."""
    values = np.asarray(returns, dtype=float)
    split = len(values) // 2

    bic_by_k: dict[int, float] = {}
    stability_by_k: dict[int, float] = {}

    for k in candidates:
        if len(values) < k * _MIN_OBS_PER_REGIME:
            bic_by_k[k] = float("inf")
            stability_by_k[k] = 0.0
            continue

        fit = fit_regime_model(values, k=k, dataset_id=dataset_id, seed=seed)
        bic_by_k[k] = _gaussian_bic(fit, values)

        # Stability: refit on each half separately, then compare label meaning.
        # A non-converging half-fit is evidence of low stability (0%), not an error.
        try:
            fit_half_1 = fit_regime_model(
                values[:split], k=k, dataset_id=dataset_id, seed=seed
            )
            labels_half_1 = label_regimes(
                characterize_regimes(fit_half_1, returns=values[:split])
            )
        except ModelingError:
            labels_half_1 = {}
        try:
            fit_half_2 = fit_regime_model(
                values[split:], k=k, dataset_id=dataset_id, seed=seed
            )
            labels_half_2 = label_regimes(
                characterize_regimes(fit_half_2, returns=values[split:])
            )
        except ModelingError:
            labels_half_2 = {}

        stability_by_k[k] = _label_alignment(labels_half_1, labels_half_2)

    # Primary: lowest BIC. Tie-break: higher stability.
    # BIC with Gaussian emissions is biased toward extra states on
    # fat-tailed data (it "shaves" the tail with an extra component);
    # an unstable extra regime is economically meaningless, so a large
    # stability gap overrides a small BIC gap.
    finite = {k: bic for k, bic in bic_by_k.items() if np.isfinite(bic)}
    if not finite:
        msg = f"all candidates {candidates} failed to produce a finite BIC"
        raise ModelingError(msg)

    sorted_by_bic = sorted(finite, key=lambda k: (finite[k], -stability_by_k[k]))
    best_k = sorted_by_bic[0]

    stability_gap = max(stability_by_k.values()) - stability_by_k[best_k]
    bic_gap = finite[best_k] - min(finite.values())
    if stability_gap > 0.3 and bic_gap < 50.0:
        # a materially more stable candidate exists with a comparable BIC
        more_stable = max(
            (k for k in finite if k != best_k),
            key=lambda k: stability_by_k[k],
        )
        if stability_by_k[more_stable] > stability_by_k[best_k]:
            best_k = more_stable

    recommendation = (
        f"k={best_k}: BIC {finite[best_k]:.2f}, stability {stability_by_k[best_k]:.0%}"
    )
    return KSelection(
        best_k=best_k,
        bic_by_k=bic_by_k,
        stability_by_k=stability_by_k,
        recommendation=recommendation,
    )


def _gaussian_bic(fit: RegimeFit, values: np.ndarray) -> float:
    """BIC: -2*logL + k_params*log(T), with logL from the fitted HMM itself.

    We refit briefly inside select_k to recover the model object (fit
    objects do not carry it), then use its native score() — our own
    weighted re-scoring was biased (filtered weights are not likelihoods).
    """
    hmmlearn = import_module("hmmlearn.hmm")
    model = hmmlearn.GaussianHMM(
        n_components=fit.k,
        covariance_type="full",
        random_state=_DEFAULT_SEED,
        n_iter=200,
        tol=1e-4,
    )
    model.startprob_ = np.full(fit.k, 1.0 / fit.k)
    model.transmat_ = fit.transition_matrix
    model.means_ = np.array([[fit.emissions[s].mean] for s in range(fit.k)])
    model.covars_ = np.array([[[fit.emissions[s].std ** 2]] for s in range(fit.k)])
    log_likelihood = float(model.score(values.reshape(-1, 1)))
    n_params = fit.k * (fit.k - 1) + 2 * fit.k + (fit.k - 1)
    return -2.0 * log_likelihood + n_params * np.log(len(values))


def _gaussian_log_density(values: np.ndarray, mean: float, std: float) -> np.ndarray:
    if std <= 0:
        return -np.inf * np.ones_like(values)
    variance = std * std
    return -0.5 * np.log(2 * np.pi * variance) - (values - mean) ** 2 / (2 * variance)


def _label_alignment(labels_a: dict[int, str], labels_b: dict[int, str]) -> float:
    """Fraction of label pairs that agree in *meaning* across two fits."""
    if len(labels_a) != len(labels_b):
        return 0.0
    matches = sum(1 for label in labels_a.values() if label in labels_b.values())
    return matches / len(labels_a)
