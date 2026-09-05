"""Domain entities and value objects for the exploratory analysis.

These types are pure data structures: they carry no I/O, no pandas dependency
and no formatting logic, so the domain layer stays framework agnostic and can be
unit tested in isolation (Dependency Inversion Principle).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping, Sequence


class Severity(str, Enum):
    """Relative importance of a data-quality finding."""

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class VariableGroup(str, Enum):
    """Analytical groups defined in Activity 1 of the challenge."""

    TARGET = "target"
    LOCATION = "location"
    PROPERTY = "property"
    HOST = "host"
    REVIEWS = "reviews"
    POLICY = "policy"
    DESCRIPTIVE = "descriptive"


@dataclass(frozen=True)
class ColumnProfile:
    """Structural description of a single column."""

    name: str
    dtype: str
    non_null: int
    missing: int
    missing_pct: float
    unique: int
    sample: str

    @property
    def is_complete(self) -> bool:
        """True when the column has no missing values at all."""
        return self.missing == 0


@dataclass(frozen=True)
class DatasetProfile:
    """Structural description of the whole dataset."""

    rows: int
    columns: int
    column_profiles: Sequence[ColumnProfile]
    duplicated_rows: int
    duplicated_ids: int

    def worst_missing(self, limit: int = 5) -> Sequence[ColumnProfile]:
        """Return the columns with the highest share of missing values."""
        ordered = sorted(self.column_profiles, key=lambda c: c.missing_pct, reverse=True)
        return ordered[:limit]


@dataclass(frozen=True)
class AnomalyFinding:
    """A single data-quality observation.

    Activity 2 explicitly forbids deep cleaning, so a finding only *describes*
    the issue and the treatment proposed for a later stage; it never mutates
    the dataset.
    """

    code: str
    title: str
    affected_columns: Sequence[str]
    observed: str
    severity: Severity
    proposed_treatment: str


@dataclass(frozen=True)
class NumericSummary:
    """Descriptive statistics for one numeric variable."""

    name: str
    count: int
    mean: float
    std: float
    minimum: float
    q1: float
    median: float
    q3: float
    maximum: float

    @property
    def iqr(self) -> float:
        """Interquartile range, used by the outlier detection rule."""
        return self.q3 - self.q1


@dataclass(frozen=True)
class CategoricalSummary:
    """Frequency description for one categorical variable."""

    name: str
    unique: int
    top_values: Mapping[str, int]
    missing_pct: float


@dataclass(frozen=True)
class ExplorationReport:
    """Aggregated output of the exploratory analysis use case."""

    profile: DatasetProfile
    numeric: Sequence[NumericSummary]
    categorical: Sequence[CategoricalSummary]
    anomalies: Sequence[AnomalyFinding]
    figures: Sequence[str] = field(default_factory=tuple)
    extras: Mapping[str, Any] = field(default_factory=dict)
