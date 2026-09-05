"""Unit tests for the domain and application layers.

They use a tiny in-memory fixture and a fake repository, which is only possible
because the use case depends on the ``ListingRepository`` port instead of a
concrete file reader.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from staydata_eda.application.anomalies import (  # noqa: E402
    AnomalyDetector,
    DuplicateRule,
    ImplausibleZeroRule,
    MissingValuesRule,
    PriceOutlierRule,
)
from staydata_eda.application.profiling import (  # noqa: E402
    profile_dataset,
    summarise_categorical,
    summarise_numeric,
)
from staydata_eda.domain import schema  # noqa: E402
from staydata_eda.domain.entities import Severity  # noqa: E402
from staydata_eda.domain.ports import ListingRepository  # noqa: E402


@pytest.fixture()
def sample() -> pd.DataFrame:
    """Minimal frame with the columns the rules inspect."""
    frame = pd.DataFrame(
        {
            schema.ID: ["1", "2", "3", "4"],
            schema.TARGET: [np.log(100), np.log(50), np.log(1500), np.log(10)],
            schema.ACCOMMODATES: [2, 1, 8, 2],
            schema.BEDROOMS: [1, 0, 3, 1],
            schema.BATHROOMS: [1.0, 1.0, 2.0, 0.0],
            schema.BEDS: [1, 1, 4, 1],
            schema.NUMBER_OF_REVIEWS: [10, 0, 5, 0],
            schema.REVIEW_SCORES_RATING: [95.0, np.nan, 88.0, np.nan],
            schema.CITY: ["NYC", "NYC", "SF", "LA"],
            schema.ROOM_TYPE: ["Entire home/apt", "Private room", "Entire home/apt", "Shared room"],
            schema.ZIPCODE: ["11201", "94117.0", "10019", None],
            schema.NEIGHBOURHOOD: ["A", "B", "C", None],
            schema.PROPERTY_TYPE: ["Apartment", "House", "Loft", "Apartment"],
            schema.AMENITIES: ['{"TV",Kitchen}', "{}", '{"TV"}', '{"Wifi",TV}'],
            schema.DESCRIPTION: ["a", "b", "c", "d"],
            schema.NAME: ["n1", "n2", "n3", "n4"],
        }
    )
    frame[schema.PRICE_USD] = np.exp(frame[schema.TARGET])
    return frame


class FakeRepository(ListingRepository):
    """Test double that returns a frame held in memory."""

    def __init__(self, frame: pd.DataFrame) -> None:
        self._frame = frame

    @property
    def source_description(self) -> str:
        return "in-memory fixture"

    def load(self) -> pd.DataFrame:
        return self._frame


def test_profile_counts_rows_and_missing(sample: pd.DataFrame) -> None:
    profile = profile_dataset(sample)
    assert profile.rows == 4
    assert profile.duplicated_ids == 0
    rating = next(c for c in profile.column_profiles if c.name == schema.REVIEW_SCORES_RATING)
    assert rating.missing == 2
    assert rating.is_complete is False


def test_numeric_summary_reports_quartiles(sample: pd.DataFrame) -> None:
    summaries = {s.name: s for s in summarise_numeric(sample)}
    accommodates = summaries[schema.ACCOMMODATES]
    assert accommodates.count == 4
    assert accommodates.minimum == 1
    assert accommodates.iqr >= 0


def test_categorical_summary_lists_levels(sample: pd.DataFrame) -> None:
    summaries = {s.name: s for s in summarise_categorical(sample)}
    assert summaries[schema.ROOM_TYPE].unique == 3
    assert summaries[schema.CITY].top_values["NYC"] == 2


def test_missing_rule_flags_high_share(sample: pd.DataFrame) -> None:
    findings = MissingValuesRule(high_threshold=20.0).evaluate(sample)
    assert any(schema.REVIEW_SCORES_RATING in f.affected_columns for f in findings)


def test_duplicate_rule_is_low_severity_when_clean(sample: pd.DataFrame) -> None:
    finding = DuplicateRule().evaluate(sample)[0]
    assert finding.severity is Severity.LOW


def test_price_rule_detects_both_tails(sample: pd.DataFrame) -> None:
    observed = PriceOutlierRule().evaluate(sample)[0].observed
    assert "1500" in observed or "1,500" in observed


def test_zero_rule_counts_studios(sample: pd.DataFrame) -> None:
    observed = ImplausibleZeroRule().evaluate(sample)[0].observed
    assert "bedrooms = 0 in 1 rows" in observed


def test_detector_runs_every_rule(sample: pd.DataFrame) -> None:
    findings = AnomalyDetector.with_default_rules().detect(sample)
    assert len(findings) >= 6


def test_fake_repository_is_substitutable(sample: pd.DataFrame) -> None:
    """Liskov check: the use case only needs the port, not the Excel adapter."""
    repository: ListingRepository = FakeRepository(sample)
    assert repository.load().shape == sample.shape
