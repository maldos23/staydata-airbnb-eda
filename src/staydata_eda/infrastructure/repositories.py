"""Concrete implementations of the ListingRepository port.

The delivered workbook is not a normal spreadsheet: the whole CSV was pasted
into a single Excel column, so every record lives in one cell and records longer
than Excel's 32,767 character limit per cell spill into extra columns. The
repository is the only place in the code base that knows about that quirk; the
rest of the project just receives a clean DataFrame.
"""

from __future__ import annotations

import csv
import io
import json
import logging
from pathlib import Path
from typing import Iterator, List, Sequence

import numpy as np
import pandas as pd

from ..domain import schema
from ..domain.ports import ListingRepository

LOGGER = logging.getLogger(__name__)


class RecordReconstructionError(RuntimeError):
    """Raised when the workbook cannot be rebuilt into a tabular structure."""


class ExcelListingRepository(ListingRepository):
    """Loads the listings from the original workbook, read-only.

    Single Responsibility: parse the raw file and hand back a typed frame.
    """

    def __init__(self, path: Path, sheet_name: str = "in") -> None:
        self._path = Path(path)
        self._sheet_name = sheet_name

    @property
    def source_description(self) -> str:
        return f"Excel workbook '{self._path.name}' (sheet '{self._sheet_name}')"

    def load(self) -> pd.DataFrame:
        """Read the workbook without modifying it and return a typed frame."""
        if not self._path.exists():
            raise FileNotFoundError(
                f"Dataset not found at {self._path}. See the README for how to place it."
            )
        LOGGER.info("Reading %s", self._path)
        raw = pd.read_excel(self._path, sheet_name=self._sheet_name, dtype=str)
        header = self._parse_header(raw.columns[0])
        records = list(self._iter_records(raw))
        frame = self._to_frame(records, header)
        return self._coerce_types(frame)

    # -- internal helpers ---------------------------------------------------

    @staticmethod
    def _parse_header(first_column_name: str) -> Sequence[str]:
        """The workbook stores the CSV header inside the first column name."""
        header = [name.strip() for name in first_column_name.split(",")]
        if len(header) != len(schema.EXPECTED_COLUMNS):
            raise RecordReconstructionError(
                f"Expected {len(schema.EXPECTED_COLUMNS)} columns, found {len(header)}."
            )
        return header

    @staticmethod
    def _iter_records(raw: pd.DataFrame) -> Iterator[str]:
        """Rebuild one CSV line per spreadsheet row.

        Cells that overflowed Excel's per-cell character limit continue in the
        following (unnamed) columns of the same row, so they are concatenated
        back in order.
        """
        for row in raw.itertuples(index=False, name=None):
            parts = [value for value in row if isinstance(value, str)]
            if parts:
                yield "".join(parts)

    @staticmethod
    def _to_frame(records: Sequence[str], header: Sequence[str]) -> pd.DataFrame:
        """Parse the rebuilt CSV lines, skipping malformed ones."""
        rows: List[Sequence[str]] = []
        malformed = 0
        for record in records:
            try:
                fields = next(csv.reader(io.StringIO(record)))
            except csv.Error:
                malformed += 1
                continue
            if len(fields) != len(header):
                malformed += 1
                continue
            rows.append(fields)
        if not rows:
            raise RecordReconstructionError("No valid records could be rebuilt.")
        LOGGER.info("Rebuilt %d records (%d malformed and skipped)", len(rows), malformed)
        frame = pd.DataFrame(rows, columns=list(header))
        # Keep the count of skipped records as metadata for the quality report.
        frame.attrs["malformed_records"] = malformed
        frame.attrs["spreadsheet_records"] = len(records)
        return frame

    @staticmethod
    def _coerce_types(frame: pd.DataFrame) -> pd.DataFrame:
        """Apply minimal, non-destructive typing.

        Only type conversion is done here. Imputation, winsorising and encoding
        belong to Activity 3 and are deliberately left out.
        """
        frame = frame.replace("", np.nan)
        for column in schema.NUMERIC_COLUMNS:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
        for column in schema.DATE_COLUMNS:
            frame[column] = pd.to_datetime(frame[column], errors="coerce")
        # Convenience column: the raw file only stores the natural logarithm.
        frame[schema.PRICE_USD] = np.exp(frame[schema.TARGET])
        return frame


class ParquetCachedRepository(ListingRepository):
    """Decorator that memoises an expensive repository on disk.

    Reading the 37 MB workbook takes about a minute; caching the rebuilt table
    as Parquet keeps notebook re-runs fast without duplicating parsing logic
    (DRY) and without the inner repository knowing anything about caching.
    """

    def __init__(self, inner: ListingRepository, cache_path: Path) -> None:
        self._inner = inner
        self._cache_path = Path(cache_path)

    @property
    def source_description(self) -> str:
        return f"{self._inner.source_description} cached at '{self._cache_path.name}'"

    @property
    def _sidecar_path(self) -> Path:
        """Parquet drops ``DataFrame.attrs``, so metadata travels beside it."""
        return self._cache_path.with_suffix(".meta.json")

    def load(self) -> pd.DataFrame:
        """Return the cached table when available, otherwise build and store it."""
        if self._cache_path.exists():
            LOGGER.info("Loading cached table from %s", self._cache_path)
            frame = pd.read_parquet(self._cache_path)
            if self._sidecar_path.exists():
                frame.attrs.update(json.loads(self._sidecar_path.read_text()))
            return frame
        frame = self._inner.load()
        self._cache_path.parent.mkdir(parents=True, exist_ok=True)
        frame.to_parquet(self._cache_path, index=False)
        self._sidecar_path.write_text(json.dumps(dict(frame.attrs)))
        LOGGER.info("Cached rebuilt table at %s", self._cache_path)
        return frame


class CsvListingRepository(ListingRepository):
    """Alternative source kept to prove the port is not tied to Excel."""

    def __init__(self, path: Path) -> None:
        self._path = Path(path)

    @property
    def source_description(self) -> str:
        return f"CSV file '{self._path.name}'"

    def load(self) -> pd.DataFrame:
        frame = pd.read_csv(self._path)
        return ExcelListingRepository._coerce_types(frame)
