"""Out-of-sample volatility benchmark over the real local snapshot.

Protocol (ADR-0006 D8): for each test day, every candidate forecasts the
next day's sigma using ONLY prior data; realized returns then score them
via VaR violation rates and MAE. Structural assertions keep the harness
honest without hard-coding statistical thresholds (reported numbers are
for humans to judge).
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from sigma.data.snapshot import load_snapshot
from sigma.modeling import (
    constant_sigma,
    ewma_sigma,
    garch_sigma,
    rolling_sigma,
    simple_returns,
)

SNAPSHOT_DIR = Path("data/processed/prices")
_snapshots = sorted(SNAPSHOT_DIR.glob("research-universe-v1__*.parquet"))
LATEST_SNAPSHOT = _snapshots[-1] if _snapshots else None

BENCHMARK_ASSETS = ("equity-aapl-us", "equity-nvda-us", "etf-gld-us")
TEST_DAYS = 250  # ~1 trading year of out-of-sample evaluation
GARCH_REFIT_EVERY = 21  # monthly-ish refit cadence
ROLLING_WINDOW = 60

Z_95, Z_99 = 1.6449, 2.3263  # Normal quantiles paired with sigma forecasts


@pytest.mark.skipif(
    LATEST_SNAPSHOT is None, reason="no local snapshot; run `make download`"
)
def test_volatility_candidates_benchmark_out_of_sample() -> None:
    assert LATEST_SNAPSHOT is not None
    observations, _ = load_snapshot(LATEST_SNAPSHOT)
    returns_matrix = simple_returns(observations)

    rows: list[dict[str, object]] = []
    for asset_id in BENCHMARK_ASSETS:
        series = returns_matrix.values[asset_id].to_numpy()
        split = len(series) - TEST_DAYS
        assert split > ROLLING_WINDOW

        scores = {
            name: {"sigmas": [], "realized": []}
            for name in ("constant", "rolling60", "ewma", "garch-normal", "garch-t")
        }
        garch_cache: dict[str, float] = {}

        for day in range(split, len(series)):
            history = series[:day]
            realized = float(series[day])

            recent = history[-min(1000, len(history)) :]
            if (day - split) % GARCH_REFIT_EVERY == 0 or not garch_cache:
                garch_cache = {
                    "normal": garch_sigma(recent, dist="normal"),
                    "t": garch_sigma(recent, dist="t"),
                }

            forecasts = {
                "constant": constant_sigma(history),
                "rolling60": rolling_sigma(history, window=ROLLING_WINDOW),
                "ewma": ewma_sigma(history),
                "garch-normal": garch_cache["normal"],
                "garch-t": garch_cache["t"],
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

            # --- structural + wide-sanity assertions -----------------------
            assert len(sigmas) == TEST_DAYS
            assert np.all(np.isfinite(sigmas)) and np.all(sigmas > 0)
            assert violations_95 < 0.50 and violations_99 < 0.50

    frame = pd.DataFrame(rows)
    print(
        "\n=== Out-of-sample volatility benchmark "
        f"({TEST_DAYS} days, refit every {GARCH_REFIT_EVERY}) ==="
    )
    print(frame.to_string(index=False))

    assert len(frame) == len(BENCHMARK_ASSETS) * 5
