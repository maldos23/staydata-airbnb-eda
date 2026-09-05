"""Structural profiling and descriptive statistics.

Every function here is a pure transformation from a DataFrame to domain value
objects, which keeps the layer testable and free of presentation concerns.
"""

from __future__ import annotations

from typing import Sequence

import pandas as pd

from ..domain import schema
from ..domain.entities import (
    CategoricalSummary,
    ColumnProfile,
    DatasetProfile,
    NumericSummary,
)

_SAMPLE_LENGTH = 60


def _first_sample(series: pd.Series) -> str:
    """Return a short, printable sample value for a column."""
    non_null = series.dropna()
    if non_null.empty:
        return ""
    value = str(non_null.iloc[0])
    return value if len(value) <= _SAMPLE_LENGTH else value[: _SAMPLE_LENGTH - 1] + "…"


def profile_dataset(frame: pd.DataFrame) -> DatasetProfile:
    """Describe rows, columns, dtypes and completeness of the whole table."""
    total = len(frame)
    profiles = [
        ColumnProfile(
            name=str(column),
            dtype=str(frame[column].dtype),
            non_null=int(frame[column].notna().sum()),
            missing=int(frame[column].isna().sum()),
            missing_pct=round(float(frame[column].isna().mean() * 100), 2),
            unique=int(frame[column].nunique(dropna=True)),
            sample=_first_sample(frame[column]),
        )
        for column in frame.columns
    ]
    duplicated_ids = (
        int(frame[schema.ID].duplicated().sum()) if schema.ID in frame.columns else 0
    )
    return DatasetProfile(
        rows=total,
        columns=frame.shape[1],
        column_profiles=tuple(profiles),
        duplicated_rows=int(frame.duplicated().sum()),
        duplicated_ids=duplicated_ids,
    )


def summarise_numeric(
    frame: pd.DataFrame, columns: Sequence[str] = schema.NUMERIC_COLUMNS
) -> Sequence[NumericSummary]:
    """Compute descriptive statistics for the requested numeric columns."""
    summaries = []
    for column in columns:
        if column not in frame.columns:
            continue
        series = pd.to_numeric(frame[column], errors="coerce").dropna()
        if series.empty:
            continue
        summaries.append(
            NumericSummary(
                name=column,
                count=int(series.size),
                mean=float(series.mean()),
                std=float(series.std()),
                minimum=float(series.min()),
                q1=float(series.quantile(0.25)),
                median=float(series.median()),
                q3=float(series.quantile(0.75)),
                maximum=float(series.max()),
            )
        )
    return tuple(summaries)


def summarise_categorical(
    frame: pd.DataFrame,
    columns: Sequence[str] = schema.CATEGORICAL_COLUMNS,
    top: int = 6,
) -> Sequence[CategoricalSummary]:
    """Compute frequency tables for the requested categorical columns."""
    summaries = []
    for column in columns:
        if column not in frame.columns:
            continue
        series = frame[column]
        counts = series.value_counts(dropna=True).head(top)
        summaries.append(
            CategoricalSummary(
                name=column,
                unique=int(series.nunique(dropna=True)),
                top_values={str(k): int(v) for k, v in counts.items()},
                missing_pct=round(float(series.isna().mean() * 100), 2),
            )
        )
    return tuple(summaries)


def to_frame(summaries: Sequence[object]) -> pd.DataFrame:
    """Render any sequence of frozen dataclasses as a DataFrame for display.

    Written once and reused by the notebook for every summary type (DRY).
    """
    return pd.DataFrame([vars(item) for item in summaries])
