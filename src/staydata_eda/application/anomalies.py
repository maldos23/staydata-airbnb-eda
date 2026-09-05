"""Data-quality rules.

Each rule is an independent Strategy implementing ``AnomalyRule``. The detector
simply runs whatever rules it is given, so a new check never requires editing
existing code (Open/Closed Principle).

Important: rules only *describe* problems. Activity 2 forbids deep cleaning, so
nothing here mutates the DataFrame.
"""

from __future__ import annotations

from typing import Sequence

import numpy as np
import pandas as pd

from ..domain import schema
from ..domain.entities import AnomalyFinding, Severity
from ..domain.ports import AnomalyRule


class MissingValuesRule(AnomalyRule):
    """Flags columns whose share of missing values exceeds a threshold."""

    def __init__(self, high_threshold: float = 20.0, low_threshold: float = 1.0) -> None:
        self._high = high_threshold
        self._low = low_threshold

    @property
    def code(self) -> str:
        return "MISSING"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        missing = (frame.isna().mean() * 100).round(2)
        high = missing[missing >= self._high].sort_values(ascending=False)
        moderate = missing[(missing >= self._low) & (missing < self._high)].sort_values(
            ascending=False
        )
        findings = []
        if not high.empty:
            findings.append(
                AnomalyFinding(
                    code=f"{self.code}-HIGH",
                    title="Columns with a high share of missing values",
                    affected_columns=tuple(high.index),
                    observed="; ".join(f"{name}: {pct}%" for name, pct in high.items()),
                    severity=Severity.HIGH,
                    proposed_treatment=(
                        "Do not drop rows. Add a 'no reviews / unknown' flag and impute "
                        "separately during Activity 3."
                    ),
                )
            )
        if not moderate.empty:
            findings.append(
                AnomalyFinding(
                    code=f"{self.code}-MODERATE",
                    title="Columns with a moderate share of missing values",
                    affected_columns=tuple(moderate.index),
                    observed="; ".join(f"{name}: {pct}%" for name, pct in moderate.items()),
                    severity=Severity.MEDIUM,
                    proposed_treatment=(
                        "Use an 'Unknown' category for text columns and per-city medians "
                        "for numeric ones."
                    ),
                )
            )
        return tuple(findings)


class DuplicateRule(AnomalyRule):
    """Checks for repeated identifiers and fully duplicated rows."""

    @property
    def code(self) -> str:
        return "DUPLICATES"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        duplicated_ids = int(frame[schema.ID].duplicated().sum())
        duplicated_rows = int(frame.duplicated().sum())
        severity = Severity.HIGH if duplicated_ids or duplicated_rows else Severity.LOW
        return (
            AnomalyFinding(
                code=self.code,
                title="Duplicated records",
                affected_columns=(schema.ID,),
                observed=f"{duplicated_ids} repeated ids and {duplicated_rows} identical rows",
                severity=severity,
                proposed_treatment="Re-check after cleaning; no action needed if both are zero.",
            ),
        )


class PriceOutlierRule(AnomalyRule):
    """Flags extreme prices and possible censoring of the target variable."""

    def __init__(self, low_usd: float = 20.0, high_usd: float = 1000.0) -> None:
        self._low = low_usd
        self._high = high_usd

    @property
    def code(self) -> str:
        return "PRICE_OUTLIERS"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        price = frame[schema.PRICE_USD]
        low = int((price <= self._low).sum())
        high = int((price >= self._high).sum())
        maximum = float(price.max())
        per_guest = price / frame[schema.ACCOMMODATES].replace(0, np.nan)
        cheap_per_guest = int((per_guest < 10).sum())
        return (
            AnomalyFinding(
                code=self.code,
                title="Extreme prices and possible upper censoring",
                affected_columns=(schema.TARGET, schema.PRICE_USD),
                observed=(
                    f"{low} listings at USD {self._low:.0f} or less (minimum USD "
                    f"{price.min():.0f}); {high} at USD {self._high:.0f} or more; "
                    f"maximum USD {maximum:.0f}; {cheap_per_guest} below USD 10 per guest"
                ),
                severity=Severity.HIGH,
                proposed_treatment=(
                    "Review both tails, document the apparent USD 1,999 cap and consider "
                    "trimming the 1st and 99th percentiles before modelling."
                ),
            ),
        )


class ImplausibleZeroRule(AnomalyRule):
    """Distinguishes legitimate zeros (studios) from hidden missing values."""

    @property
    def code(self) -> str:
        return "ZEROS"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        counts = {
            column: int((frame[column] == 0).sum())
            for column in (schema.BEDROOMS, schema.BATHROOMS, schema.BEDS)
            if column in frame.columns
        }
        return (
            AnomalyFinding(
                code=self.code,
                title="Zero values that may be legitimate or hidden gaps",
                affected_columns=tuple(counts),
                observed="; ".join(f"{name} = 0 in {value} rows" for name, value in counts.items()),
                severity=Severity.MEDIUM,
                proposed_treatment=(
                    "Treat bedrooms = 0 as a studio flag; review zeros in bathrooms and "
                    "beds individually."
                ),
            ),
        )


class InconsistentFormatRule(AnomalyRule):
    """Detects values stored with the wrong or mixed textual format."""

    @property
    def code(self) -> str:
        return "FORMATS"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        findings = []
        zipcode = frame[schema.ZIPCODE].dropna().astype(str)
        malformed_zip = int((~zipcode.str.fullmatch(r"\d{5}")).sum())
        findings.append(
            AnomalyFinding(
                code=f"{self.code}-ZIP",
                title="Inconsistent postal code format",
                affected_columns=(schema.ZIPCODE,),
                observed=(
                    f"{malformed_zip} values do not match a 5-digit pattern "
                    f"(e.g. '94117.0'); {zipcode.nunique()} distinct values in total"
                ),
                severity=Severity.MEDIUM,
                proposed_treatment="Normalise to five digits before using it as a location key.",
            )
        )
        findings.append(
            AnomalyFinding(
                code=f"{self.code}-BOOL",
                title="Numeric and boolean values stored as text",
                affected_columns=(
                    schema.HOST_RESPONSE_RATE,
                    schema.CLEANING_FEE,
                    schema.INSTANT_BOOKABLE,
                ),
                observed=(
                    "host_response_rate keeps the '%' sign; cleaning_fee uses "
                    "'True'/'False' while the other boolean columns use 't'/'f'"
                ),
                severity=Severity.MEDIUM,
                proposed_treatment="Convert the rate to a decimal and unify booleans to 0/1.",
            )
        )
        return tuple(findings)


class HighCardinalityRule(AnomalyRule):
    """Flags categorical columns that would explode under one-hot encoding."""

    def __init__(self, threshold: int = 30) -> None:
        self._threshold = threshold

    @property
    def code(self) -> str:
        return "CARDINALITY"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        counts = {
            column: int(frame[column].nunique(dropna=True))
            for column in (schema.NEIGHBOURHOOD, schema.ZIPCODE, schema.PROPERTY_TYPE)
            if column in frame.columns
        }
        offenders = {k: v for k, v in counts.items() if v > self._threshold}
        if not offenders:
            return ()
        return (
            AnomalyFinding(
                code=self.code,
                title="High-cardinality categorical variables",
                affected_columns=tuple(offenders),
                observed="; ".join(f"{name}: {value} levels" for name, value in offenders.items()),
                severity=Severity.MEDIUM,
                proposed_treatment=(
                    "Group rare levels into 'Other' and use frequency or target encoding "
                    "validated inside each city."
                ),
            ),
        )


class UnstructuredTextRule(AnomalyRule):
    """Reports free-text columns that need extraction before modelling."""

    @property
    def code(self) -> str:
        return "TEXT"

    def evaluate(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        amenities = frame[schema.AMENITIES].fillna("")
        empty = int((amenities.str.strip() == "{}").sum())
        avg_items = float(amenities.str.count(",").add(1).mean())
        return (
            AnomalyFinding(
                code=self.code,
                title="Unstructured text pending extraction",
                affected_columns=(schema.AMENITIES, schema.DESCRIPTION, schema.NAME),
                observed=(
                    f"amenities holds {avg_items:.1f} items on average and {empty} empty "
                    "lists; description and name are free text"
                ),
                severity=Severity.MEDIUM,
                proposed_treatment=(
                    "Turn the most frequent amenities into binary indicators; postpone "
                    "description and name to a text-processing stage."
                ),
            ),
        )


class AnomalyDetector:
    """Runs a collection of rules and collects their findings.

    The detector knows nothing about the rules it executes, which is what makes
    the set extensible without modification.
    """

    def __init__(self, rules: Sequence[AnomalyRule]) -> None:
        self._rules = tuple(rules)

    @classmethod
    def with_default_rules(cls) -> "AnomalyDetector":
        """Factory method with the rule set used by the challenge."""
        return cls(
            (
                MissingValuesRule(),
                DuplicateRule(),
                PriceOutlierRule(),
                ImplausibleZeroRule(),
                InconsistentFormatRule(),
                HighCardinalityRule(),
                UnstructuredTextRule(),
            )
        )

    def detect(self, frame: pd.DataFrame) -> Sequence[AnomalyFinding]:
        """Return every finding produced by the configured rules."""
        findings: list[AnomalyFinding] = []
        for rule in self._rules:
            findings.extend(rule.evaluate(frame))
        return tuple(findings)
