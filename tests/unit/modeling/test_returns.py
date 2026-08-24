"""Tests for asset returns computation (WP-3, ADR-0005)."""

import numpy as np
import pandas as pd
import pytest
from obs_fixtures import DATASET_ID, make_obs

from sigma.domain import MarketObservation
from sigma.modeling import ReturnMatrix, simple_returns, to_log
from sigma.modeling.errors import ModelingError


def three_day_series() -> list[MarketObservation]:
    """AAPL: 100 -> 110 -> 99 ; MSFT: 200 -> 210 -> 189 (same dates)."""
    obs: list[MarketObservation] = []
    for day, aapl, msft in [
        (17, "100", "200"),
        (18, "110", "210"),
        (19, "99", "189"),
    ]:
        obs.append(make_obs("equity-aapl-us", day, aapl))
        obs.append(make_obs("equity-msft-us", day, msft))
    return obs


def test_simple_returns_hand_computed() -> None:
    matrix = simple_returns(three_day_series())

    assert list(matrix.values.columns) == ["equity-aapl-us", "equity-msft-us"]
    assert len(matrix.values) == 2  # first day dropped
    aapl = matrix.values["equity-aapl-us"].to_numpy()
    assert np.isclose(aapl[0], 0.10)  # 100 -> 110
    assert np.isclose(aapl[1], -0.10)  # 110 -> 99
    msft = matrix.values["equity-msft-us"].to_numpy()
    assert np.isclose(msft[0], 0.05)  # 200 -> 210
    assert np.isclose(msft[1], -0.10)  # 210 -> 189


def test_method_and_provenance_metadata() -> None:
    matrix = simple_returns(three_day_series())
    assert matrix.method == "SIMPLE"
    assert matrix.dataset_id == DATASET_ID


def test_values_are_float_dtype_with_utc_index() -> None:
    matrix = simple_returns(three_day_series())
    assert all(dtype == np.float64 for dtype in matrix.values.dtypes)
    assert isinstance(matrix.values.index, pd.DatetimeIndex)
    assert matrix.values.index.tz is not None
    assert matrix.values.index.is_monotonic_increasing


def test_alignment_drops_dates_missing_any_asset_and_reports(tmp_path) -> None:
    obs = three_day_series()
    # GLD exists only on days 18 and 19 -> common grid becomes {18, 19}
    obs.append(make_obs("etf-gld-us", 18, "150"))
    obs.append(make_obs("etf-gld-us", 19, "165"))

    matrix = simple_returns(obs)

    assert set(matrix.values.columns) == {
        "equity-aapl-us",
        "equity-msft-us",
        "etf-gld-us",
    }
    assert len(matrix.values) == 1  # only one return row from 2 aligned days
    report = matrix.meta
    assert report.aligned_price_days == 2
    assert report.asset_days["etf-gld-us"] == 2
    assert report.dropped_by_alignment["equity-aapl-us"] == 1
    assert report.return_days == 1


def test_first_day_drop_is_reported() -> None:
    matrix = simple_returns(three_day_series())
    assert matrix.meta.return_days == 2
    assert matrix.meta.aligned_price_days == 3


def test_log_round_trip_is_exact_inverse() -> None:
    simple = simple_returns(three_day_series())
    log_matrix = to_log(simple)

    assert log_matrix.method == "LOG"
    assert log_matrix.dataset_id == DATASET_ID
    recovered = np.expm1(log_matrix.values.to_numpy())
    assert np.allclose(recovered, simple.values.to_numpy())


def test_to_log_matches_ln_one_plus_r() -> None:
    simple = simple_returns(three_day_series())
    log_matrix = to_log(simple)
    expected = np.log1p(simple.values["equity-aapl-us"].to_numpy())
    assert np.allclose(log_matrix.values["equity-aapl-us"].to_numpy(), expected)


def test_mixed_dataset_ids_raise() -> None:
    obs = three_day_series()
    obs.append(make_obs("etf-gld-us", 18, "150", dataset_id="other-snapshot"))
    with pytest.raises(ModelingError, match="dataset_id"):
        simple_returns(obs)


def test_single_row_asset_raises() -> None:
    obs = three_day_series()
    obs.append(make_obs("etf-gld-us", 18, "150"))  # only one day
    with pytest.raises(ModelingError, match="etf-gld-us"):
        simple_returns(obs)


def test_return_matrix_is_frozen() -> None:
    matrix: ReturnMatrix = simple_returns(three_day_series())
    with pytest.raises(Exception):  # noqa: B017 — frozen dataclass raises
        matrix.dataset_id = "tampered"  # type: ignore[misc]


def test_price_boundary_uses_float64_not_object() -> None:
    matrix = simple_returns(three_day_series())
    raw = matrix.values.iloc[0, 0]
    assert isinstance(raw, (float, np.float64))
    assert not isinstance(raw, pd.Timestamp)
