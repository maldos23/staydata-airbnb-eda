"""Application use cases.

A use case orchestrates ports and pure functions; it holds no I/O details of its
own, so the same object runs from a notebook, a CLI or a test with fake
implementations injected.
"""

from __future__ import annotations

import logging
from typing import Sequence

import pandas as pd

from ..domain.entities import ExplorationReport
from ..domain.ports import ChartStrategy, FigureRenderer, ListingRepository
from .anomalies import AnomalyDetector
from .profiling import profile_dataset, summarise_categorical, summarise_numeric

LOGGER = logging.getLogger(__name__)


class RunExploratoryAnalysis:
    """Loads the dataset, profiles it, detects anomalies and renders figures."""

    def __init__(
        self,
        repository: ListingRepository,
        detector: AnomalyDetector,
        renderer: FigureRenderer,
        charts: Sequence[ChartStrategy],
    ) -> None:
        self._repository = repository
        self._detector = detector
        self._renderer = renderer
        self._charts = tuple(charts)

    def load(self) -> pd.DataFrame:
        """Expose the loaded frame so a notebook can run extra ad-hoc queries."""
        LOGGER.info("Loading data from %s", self._repository.source_description)
        return self._repository.load()

    def execute(self, frame: pd.DataFrame | None = None) -> ExplorationReport:
        """Run the full exploratory pass and return an aggregated report."""
        data = self.load() if frame is None else frame
        report = ExplorationReport(
            profile=profile_dataset(data),
            numeric=summarise_numeric(data),
            categorical=summarise_categorical(data),
            anomalies=self._detector.detect(data),
            figures=self._renderer.render_all(data, self._charts),
            extras={
                "source": self._repository.source_description,
                "malformed_records": data.attrs.get("malformed_records"),
                "spreadsheet_records": data.attrs.get("spreadsheet_records"),
            },
        )
        LOGGER.info(
            "Exploration finished: %d rows, %d findings, %d figures",
            report.profile.rows,
            len(report.anomalies),
            len(report.figures),
        )
        return report
