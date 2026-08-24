"""Download entry point: universe -> raw -> validation -> snapshot (ADR-0003 D4).

Usage::

    python -m sigma.data.download --universe configs/universe.yaml
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sigma.data.snapshot import SnapshotMeta, SnapshotPaths, save_snapshot
from sigma.data.universe import Universe, load_universe
from sigma.data.validation import validate_observations
from sigma.data.yfinance_loader import fetch_raw, parse_observations

__all__ = ["DownloadSummary", "main", "run_download"]


@dataclass(frozen=True)
class DownloadSummary:
    dataset_id: str
    prices: Path
    meta: Path
    raw_paths: list[Path]
    rows: int
    dropped_rows: int


def run_download(
    universe_path: Path,
    *,
    data_dir: Path = Path("data"),
    end: datetime | None = None,
    now: Callable[[], datetime] = lambda: datetime.now(UTC),
) -> DownloadSummary:
    """Execute the full download pipeline for one universe.

    ``now`` is injectable so callers (and tests) control snapshot stamping.
    """
    universe: Universe = load_universe(universe_path)

    retrieved_at = now()
    stamp = retrieved_at.strftime("%Y%m%dT%H%M%SZ")
    dataset_id = f"{universe.name}__{stamp}"

    frame = fetch_raw(universe, end=end.date() if end else None)
    raw_paths = _write_raw(frame, universe, data_dir / "raw" / "yfinance", stamp)

    parsed = parse_observations(frame, universe=universe, dataset_id=dataset_id)
    required_symbols = {asset.symbol: asset.asset_id for asset in universe.assets}
    validate_observations(parsed.observations, required_symbols)

    meta = SnapshotMeta(
        universe=universe.name,
        provider="yfinance",
        symbols=[asset.symbol for asset in universe.assets],
        frequency=universe.frequency,
        calendar=universe.calendar,
        timezone=universe.timezone,
        retrieved_at=retrieved_at,
        period_start=universe.period_start,
        rows=len(parsed.observations),
        dropped_rows=parsed.dropped_rows,
    )
    paths: SnapshotPaths = save_snapshot(
        parsed.observations, meta=meta, out_dir=data_dir / "processed" / "prices"
    )

    return DownloadSummary(
        dataset_id=dataset_id,
        prices=paths.prices,
        meta=paths.meta,
        raw_paths=raw_paths,
        rows=len(parsed.observations),
        dropped_rows=parsed.dropped_rows,
    )


def _write_raw(frame, universe: Universe, out_dir: Path, stamp: str) -> list[Path]:
    """Persist provider output verbatim per symbol (ADR-0003 D2)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for symbol in frame.columns.get_level_values(-1).unique():
        bars = frame.xs(symbol, axis=1, level=-1)
        path = out_dir / f"{symbol}__{stamp}.parquet"
        bars.to_parquet(path)
        paths.append(path)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m sigma.data.download",
        description="Download a universe into raw + processed snapshots.",
    )
    parser.add_argument("--universe", type=Path, required=True)
    parser.add_argument("--data-dir", type=Path, default=Path("data"))
    parser.add_argument("--end", type=str, default=None, help="YYYY-MM-DD")
    args = parser.parse_args(argv)

    end = (
        datetime.strptime(args.end, "%Y-%m-%d").replace(tzinfo=UTC)
        if args.end
        else None
    )
    summary = run_download(args.universe, data_dir=args.data_dir, end=end)

    print(f"dataset_id   : {summary.dataset_id}")
    print(f"raw files    : {len(summary.raw_paths)}")
    print(f"observations : {summary.rows}")
    print(f"dropped rows : {summary.dropped_rows}")
    print(f"snapshot     : {summary.prices}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
