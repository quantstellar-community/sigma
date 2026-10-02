"""Out-of-sample benchmark: GARCH-per-regime vs full-series GARCH.

The critical design point (ADR-0011 D2/D3, WP-4b.5b): the HMM regime labels
must NEVER peek into the future. We refit the HMM on an expanding window
and predict labels causally, so the benchmark measures genuine out-of-sample
skill — not in-sample optimism.

Candidate ladder (same interface, same days, same metrics):
    constant / rolling60 / ewma / garch-full / garch-per-regime

Metrics (per ADR-0006 D8): VaR violation rates (95/99) + MAE vs |r|.
Reported numbers are for humans to judge; assertions are structural only.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from sigma.data.snapshot import load_snapshot
from sigma.modeling import (
    constant_sigma,
    ewma_sigma,
    fit_regime_garch,
    fit_regime_model,
    forecast_regime_vol,
    rolling_sigma,
    simple_returns,
    to_log,
)

SNAPSHOT_DIR = Path("data/processed/prices")
_snapshots = sorted(SNAPSHOT_DIR.glob("research-universe-v1__*.parquet"))
LATEST_SNAPSHOT = _snapshots[-1] if _snapshots else None

BENCHMARK_ASSETS = ("etf-spy-us", "equity-nvda-us", "etf-gld-us")
TEST_DAYS = 250
REFIT_EVERY = 63  # HMM refit cadence; 63d cuts runtime while staying causal
ROLLING_WINDOW = 60
Z_95, Z_99 = 1.6449, 2.3263
SEED = 42


def _causal_labels_cached(series: np.ndarray) -> np.ndarray:
    """Label each day using ONLY data up to that day (expanding-window refit).

    Strictly causal: at refit point r the HMM is fitted on data[:r]; the label
    for day t >= r is the Viterbi last-state on data[:t+1] with that FIXED
    model. Parameters come from r <= t, data from <= t — no future leak.

    Refits every ``REFIT_EVERY`` days; cost is dominated by the fits, so the
    cadence also acts as a sensitivity parameter of the benchmark.
    """
    n = len(series)
    labels = np.full(n, -1, dtype=int)
    refit_at = list(range(3 * REFIT_EVERY, n, REFIT_EVERY))
    for refit_idx in refit_at:
        end = min(refit_idx + REFIT_EVERY, n)
        fit = fit_regime_model(series[:refit_idx], k=2, dataset_id="bench", seed=SEED)
        for t in range(refit_idx, end):
            labels[t] = int(fit.model.predict(series[: t + 1].reshape(-1, 1))[-1])
    # warm-up region: use the earliest fitted model
    first_refit = refit_at[0]
    warm_fit = fit_regime_model(
        series[:first_refit], k=2, dataset_id="bench", seed=SEED
    )
    labels[:first_refit] = warm_fit.most_likely_states
    return labels


@pytest.mark.skipif(
    LATEST_SNAPSHOT is None, reason="no local snapshot; run `make download`"
)
def test_regime_garch_benchmark_out_of_sample() -> None:
    assert LATEST_SNAPSHOT is not None
    observations, _ = load_snapshot(LATEST_SNAPSHOT)
    returns_matrix = simple_returns(observations)
    log_matrix = to_log(returns_matrix)

    rows: list[dict[str, object]] = []
    for asset_id in BENCHMARK_ASSETS:
        series = log_matrix.values[asset_id].to_numpy()
        split = len(series) - TEST_DAYS
        assert split > ROLLING_WINDOW

        labels = _causal_labels_cached(series)
        scores = {
            name: {"sigmas": [], "realized": []}
            for name in ("constant", "rolling60", "ewma", "garch-regime")
        }
        regime_sigma_cache: float | None = None

        for day in range(split, len(series)):
            history = series[:day]
            realized = float(series[day])

            if (day - split) % REFIT_EVERY == 0 or regime_sigma_cache is None:
                regime_fit = fit_regime_garch(
                    series[:day], labels[:day], dataset_id="bench", dist="t"
                )
                regime_sigma_cache = forecast_regime_vol(
                    regime_fit,
                    series[:day],
                    labels[:day],
                    current_idx=day - 1,
                ).sigma_tomorrow

            forecasts = {
                "constant": constant_sigma(history),
                "rolling60": rolling_sigma(history, window=ROLLING_WINDOW),
                "ewma": ewma_sigma(history),
                "garch-regime": regime_sigma_cache,
            }
            for name, sigma in forecasts.items():
                scores[name]["sigmas"].append(sigma)
                scores[name]["realized"].append(realized)

        for name, score in scores.items():
            sigmas = np.asarray(score["sigmas"])
            realized = np.asarray(score["realized"])
            violations_95 = float(np.mean(realized < -Z_95 * sigmas))
            violations_99 = float(np.mean(realized < -Z_99 * sigmas))
            mae_vol = float(np.mean(np.abs(np.abs(realized) - sigmas)))
            rows.append(
                {
                    "asset": asset_id.replace("equity-", "").replace("etf-", ""),
                    "candidate": name,
                    "viol95%": round(violations_95 * 100, 2),
                    "viol99%": round(violations_99 * 100, 2),
                    "mae_abs_vs_vol": round(mae_vol, 5),
                    "n_days": len(sigmas),
                }
            )
            assert len(sigmas) == TEST_DAYS
            assert np.all(np.isfinite(sigmas)) and np.all(sigmas > 0)
            assert violations_95 < 0.50 and violations_99 < 0.50

    frame = pd.DataFrame(rows)
    print(
        "\n=== OOS benchmark: GARCH-per-regime vs baselines "
        f"({TEST_DAYS} days, refit {REFIT_EVERY}) ==="
    )
    print(frame.to_string(index=False))
    assert len(frame) == len(BENCHMARK_ASSETS) * 4
    assert set(frame["candidate"]) == {
        "constant",
        "rolling60",
        "ewma",
        "garch-regime",
    }
