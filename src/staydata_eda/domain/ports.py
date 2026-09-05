"""Ports (abstract interfaces) that the application layer depends on.

Following the Dependency Inversion Principle, the application layer talks to
these small abstractions and never to a concrete file format or plotting
library. Each port is deliberately narrow (Interface Segregation Principle):
an implementation is never forced to provide behaviour it does not need.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

import pandas as pd

from .entities import AnomalyFinding


class ListingRepository(ABC):
    """Repository pattern: hides where and how the listings are stored.

    Swapping the Excel source for a CSV, a Parquet file or a SQL table only
    requires a new implementation of this port (Open/Closed Principle).
    """

    @abstractmethod
    def load(self) -> pd.DataFrame:
        """Return the listings as an in-memory table.

        Implementations MUST treat the source as read-only: Activity 2 requires
        keeping the original file untouched.
        """

    @property
    @abstractmethod
    def source_description(self) -> str:
        """Human readable description of the origin of the data."""


class AnomalyRule(ABC):
    """Strategy pattern: one interchangeable data-quality check.

    New checks are added by writing a new rule class and registering it, never
    by editing the detector that runs them (Open/Closed Principle).
    """

    @property
    @abstractmethod
    def code(self) -> str:
        """Short stable identifier of the rule."""

    @abstractmethod
    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        """Inspect the frame and return zero or more findings."""


class ChartStrategy(ABC):
    """Strategy pattern: one interchangeable exploratory figure."""

    @property
    @abstractmethod
    def filename(self) -> str:
        """File name (without directory) used to persist the figure."""

    @property
    @abstractmethod
    def title(self) -> str:
        """Figure title, reused by the report."""

    @abstractmethod
    def render(self, frame: pd.DataFrame, output_path: str) -> str:
        """Draw the figure and persist it, returning the written path."""


class FigureRenderer(ABC):
    """Port that turns a collection of chart strategies into stored files."""

    @abstractmethod
    def render_all(self, frame: pd.DataFrame, charts: Sequence[ChartStrategy]) -> Sequence[str]:
        """Render every chart and return the list of written paths."""
