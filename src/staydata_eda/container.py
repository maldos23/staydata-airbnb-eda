"""Composition root.

This is the only module allowed to know every concrete class at once. Wiring the
dependencies in a single place keeps the layers decoupled and makes it trivial to
substitute an implementation (for example a CSV repository) in a test.
"""

from __future__ import annotations

import logging

from .application.anomalies import AnomalyDetector
from .application.use_cases import RunExploratoryAnalysis
from .domain.ports import ListingRepository
from .infrastructure.config import Settings
from .infrastructure.plotting import MatplotlibFigureRenderer, default_charts
from .infrastructure.repositories import ExcelListingRepository, ParquetCachedRepository


def configure_logging(level: int = logging.INFO) -> None:
    """Set up a single, predictable logging format for every entry point."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def build_repository(settings: Settings, use_cache: bool = True) -> ListingRepository:
    """Build the listings repository, optionally wrapped in the cache decorator."""
    repository: ListingRepository = ExcelListingRepository(
        settings.raw_data_path, settings.sheet_name
    )
    if use_cache:
        repository = ParquetCachedRepository(repository, settings.cache_path)
    return repository


def build_analysis(settings: Settings | None = None, use_cache: bool = True) -> RunExploratoryAnalysis:
    """Return the fully wired exploratory analysis use case."""
    settings = settings or Settings.from_env()
    settings.ensure_directories()
    return RunExploratoryAnalysis(
        repository=build_repository(settings, use_cache=use_cache),
        detector=AnomalyDetector.with_default_rules(),
        renderer=MatplotlibFigureRenderer(settings.figures_dir),
        charts=default_charts(),
    )
