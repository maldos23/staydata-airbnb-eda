"""Command line entry point.

Running ``python -m staydata_eda.main`` reproduces the whole exploratory pass and
writes the figures, which is what the Docker image executes by default.
"""

from __future__ import annotations

import argparse
import logging

from .application.profiling import to_frame
from .container import build_analysis, configure_logging
from .domain.entities import ExplorationReport
from .infrastructure.config import Settings


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


def main() -> None:
    """Parse arguments, run the use case and print the summary."""
    parser = argparse.ArgumentParser(description="StayData Lab exploratory analysis")
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore the Parquet cache and rebuild the table from the workbook.",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging.")
    args = parser.parse_args()

    configure_logging(logging.DEBUG if args.verbose else logging.INFO)
    analysis = build_analysis(Settings.from_env(), use_cache=not args.no_cache)
    _print_report(analysis.execute())


if __name__ == "__main__":
    main()
