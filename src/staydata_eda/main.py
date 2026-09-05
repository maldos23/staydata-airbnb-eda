"""Command line entry point.

Running ``python -m staydata_eda.main`` reproduces the whole exploratory pass and
writes the figures, which is what the Docker image executes by default.
"""

from __future__ import annotations

import argparse
import json
import logging
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from .application.profiling import to_frame
from .container import build_analysis, configure_logging
from .domain import schema
from .domain.entities import ExplorationReport
from .infrastructure.config import Settings
from .infrastructure.plotting import default_charts


def _print_report(report: ExplorationReport) -> None:
    """Print a compact console summary of the exploration."""
    profile = report.profile
    print("\n=== DATASET STRUCTURE ===")
    print(f"source              : {report.extras.get('source')}")
    print(f"rows x columns      : {profile.rows:,} x {profile.columns}")
    print(f"duplicated ids/rows : {profile.duplicated_ids} / {profile.duplicated_rows}")
    print(f"skipped records     : {report.extras.get('malformed_records')}")

    print("\n=== NUMERIC SUMMARY ===")
    print(to_frame(report.numeric).to_string(index=False))

    print("\n=== CATEGORICAL SUMMARY ===")
    for summary in report.categorical:
        top = ", ".join(f"{k} ({v:,})" for k, v in summary.top_values.items())
        print(f"- {summary.name}: {summary.unique} levels | missing {summary.missing_pct}% | {top}")

    print("\n=== DATA QUALITY FINDINGS ===")
    for finding in report.anomalies:
        print(f"[{finding.severity.value.upper():6}] {finding.code}: {finding.title}")
        print(f"         observed : {finding.observed}")
        print(f"         proposal : {finding.proposed_treatment}")

    print("\n=== FIGURES ===")
    for path in report.figures:
        print(f"- {path}")


def _grouped_price(frame: pd.DataFrame, column: str) -> list[dict]:
    """Listings count and median nightly price per level of a categorical column."""
    grouped = frame.groupby(column)[schema.PRICE_USD]
    rows = [
        {"label": str(level), "listings": int(values.size), "median_price": round(float(values.median()), 2)}
        for level, values in grouped
    ]
    return sorted(rows, key=lambda row: row["median_price"], reverse=True)


def _export_site(report: ExplorationReport, frame: pd.DataFrame, out_dir: Path) -> Path:
    """Write the figures and every number of this run into ``site/data.js``.

    The static site reads a plain ``window.DATA`` global, so it needs no server,
    no build step and no fetch: publishing is just copying the folder.
    """
    figures_dir = out_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    titles = {chart.filename: chart.title for chart in default_charts()}
    for path in report.figures:
        shutil.copy2(path, figures_dir / Path(path).name)

    price = frame[schema.PRICE_USD].dropna()
    payload = {
        **asdict(report),
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "figures": [
            {"file": Path(p).name, "title": titles.get(Path(p).name, Path(p).stem)}
            for p in report.figures
        ],
        "price": {
            "median": round(float(price.median()), 2),
            "mean": round(float(price.mean()), 2),
            "p10": round(float(price.quantile(0.10)), 2),
            "p90": round(float(price.quantile(0.90)), 2),
            "maximum": round(float(price.max()), 2),
        },
        "by_city": _grouped_price(frame, schema.CITY),
        "by_room_type": _grouped_price(frame, schema.ROOM_TYPE),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "data.js"
    target.write_text(
        "window.DATA = " + json.dumps(payload, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    return target


def main() -> None:
    """Parse arguments, run the use case and print the summary."""
    parser = argparse.ArgumentParser(description="StayData Lab exploratory analysis")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore the Parquet cache and rebuild the table from the workbook.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    parser.add_argument(
        "--site",
        nargs="?",
        const="site",
        default=None,
        metavar="DIR",
        help="Also export the results as site/data.js and copy the figures there.",
    )
    args = parser.parse_args()

    configure_logging(logging.DEBUG if args.verbose else logging.INFO)
    analysis = build_analysis(Settings.from_env(), use_cache=not args.no_cache)
    frame = analysis.load()
    report = analysis.execute(frame)
    _print_report(report)
    if args.site:
        print(f"\n=== SITE ===\n- {_export_site(report, frame, Path(args.site))}")


if __name__ == "__main__":
    main()
