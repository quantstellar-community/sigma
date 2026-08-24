"""End-to-end download flow tests — fully offline via monkeypatched fetch."""

from datetime import UTC, datetime

import pytest
from yf_fixtures import make_yf_frame

from sigma.data import download as dl
from sigma.data.snapshot import load_snapshot

UNIVERSE_PATH_NAME = "universe.yaml"

UNIVERSE_YAML = """
universe:
  name: research-universe-v1
  frequency: 1d
  calendar: NYSE
  timezone: America/New_York
  period:
    start: 2026-08-01
assets:
  - { asset_id: equity-aapl-us, symbol: AAPL, asset_type: EQUITY, currency: USD }
"""


@pytest.fixture()
def universe_file(tmp_path):
    path = tmp_path / UNIVERSE_PATH_NAME
    path.write_text(UNIVERSE_YAML, encoding="utf-8")
    return path


def test_run_download_produces_raw_and_processed_artifacts(
    monkeypatch, tmp_path, universe_file
) -> None:
    monkeypatch.setattr(dl, "fetch_raw", lambda *a, **kw: make_yf_frame(["AAPL"]))
    data_dir = tmp_path / "data"

    summary = dl.run_download(universe_file, data_dir=data_dir)

    raw_files = list((data_dir / "raw" / "yfinance").glob("AAPL__*.parquet"))
    assert len(raw_files) == 1
    assert summary.prices.exists() and summary.meta.exists()
    assert summary.rows == 5
    assert summary.dropped_rows == 0

    observations, meta = load_snapshot(summary.prices)
    assert len(observations) == 5
    assert meta.provider == "yfinance"
    assert meta.retrieved_at.tzinfo == UTC


def test_dataset_id_embeds_universe_name_and_utc_stamp(
    monkeypatch, tmp_path, universe_file
) -> None:
    monkeypatch.setattr(dl, "fetch_raw", lambda *a, **kw: make_yf_frame(["AAPL"]))

    summary = dl.run_download(universe_file, data_dir=tmp_path / "d")

    assert summary.dataset_id.startswith("research-universe-v1__")


def test_two_runs_do_not_overwrite_each_other(
    monkeypatch, tmp_path, universe_file
) -> None:
    monkeypatch.setattr(dl, "fetch_raw", lambda *a, **kw: make_yf_frame(["AAPL"]))
    data_dir = tmp_path / "data"
    ticks = iter(
        [
            datetime(2026, 8, 24, 15, 0, tzinfo=UTC),
            datetime(2026, 8, 24, 15, 1, tzinfo=UTC),
        ]
    )

    first = dl.run_download(universe_file, data_dir=data_dir, now=lambda: next(ticks))
    second = dl.run_download(universe_file, data_dir=data_dir, now=lambda: next(ticks))

    assert first.prices != second.prices
    assert first.meta != second.meta
