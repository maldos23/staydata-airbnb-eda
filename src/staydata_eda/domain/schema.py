"""Single source of truth for the column names of the challenge dataset.

Every layer imports the names from here instead of repeating string literals,
which keeps the project DRY: renaming a column is a one-line change.
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Mapping, Sequence

from .entities import VariableGroup

# --- Target -----------------------------------------------------------------
TARGET = "log_price"

# --- Individual columns used explicitly across the code base ----------------
ID = "id"
CITY = "city"
NEIGHBOURHOOD = "neighbourhood"
ZIPCODE = "zipcode"
LATITUDE = "latitude"
LONGITUDE = "longitude"
PROPERTY_TYPE = "property_type"
ROOM_TYPE = "room_type"
ACCOMMODATES = "accommodates"
BATHROOMS = "bathrooms"
BEDROOMS = "bedrooms"
BEDS = "beds"
BED_TYPE = "bed_type"
AMENITIES = "amenities"
CANCELLATION_POLICY = "cancellation_policy"
CLEANING_FEE = "cleaning_fee"
INSTANT_BOOKABLE = "instant_bookable"
HOST_SINCE = "host_since"
HOST_RESPONSE_RATE = "host_response_rate"
HOST_HAS_PROFILE_PIC = "host_has_profile_pic"
HOST_IDENTITY_VERIFIED = "host_identity_verified"
NUMBER_OF_REVIEWS = "number_of_reviews"
REVIEW_SCORES_RATING = "review_scores_rating"
FIRST_REVIEW = "first_review"
LAST_REVIEW = "last_review"
NAME = "name"
DESCRIPTION = "description"
THUMBNAIL_URL = "thumbnail_url"

# Derived column added at load time; the raw file only stores the logarithm.
PRICE_USD = "price_usd"

# --- Type groups ------------------------------------------------------------
NUMERIC_COLUMNS: Sequence[str] = (
    TARGET,
    ACCOMMODATES,
    BATHROOMS,
    BEDROOMS,
    BEDS,
    NUMBER_OF_REVIEWS,
    REVIEW_SCORES_RATING,
    LATITUDE,
    LONGITUDE,
)

CATEGORICAL_COLUMNS: Sequence[str] = (
    CITY,
    ROOM_TYPE,
    PROPERTY_TYPE,
    BED_TYPE,
    CANCELLATION_POLICY,
    CLEANING_FEE,
    INSTANT_BOOKABLE,
    HOST_IDENTITY_VERIFIED,
    HOST_HAS_PROFILE_PIC,
    NEIGHBOURHOOD,
)

DATE_COLUMNS: Sequence[str] = (FIRST_REVIEW, LAST_REVIEW, HOST_SINCE)

TEXT_COLUMNS: Sequence[str] = (NAME, DESCRIPTION, AMENITIES, THUMBNAIL_URL)

# --- Analytical groups defined in Activity 1 --------------------------------
VARIABLE_GROUPS: Mapping[VariableGroup, Sequence[str]] = MappingProxyType(
    {
        VariableGroup.TARGET: (TARGET,),
        VariableGroup.LOCATION: (CITY, NEIGHBOURHOOD, ZIPCODE, LATITUDE, LONGITUDE),
        VariableGroup.PROPERTY: (
            PROPERTY_TYPE,
            ROOM_TYPE,
            ACCOMMODATES,
            BEDROOMS,
            BEDS,
            BATHROOMS,
            BED_TYPE,
            AMENITIES,
        ),
        VariableGroup.HOST: (
            HOST_SINCE,
            HOST_HAS_PROFILE_PIC,
            HOST_IDENTITY_VERIFIED,
            HOST_RESPONSE_RATE,
        ),
        VariableGroup.REVIEWS: (
            NUMBER_OF_REVIEWS,
            REVIEW_SCORES_RATING,
            FIRST_REVIEW,
            LAST_REVIEW,
        ),
        VariableGroup.POLICY: (CANCELLATION_POLICY, CLEANING_FEE, INSTANT_BOOKABLE),
        VariableGroup.DESCRIPTIVE: (ID, NAME, DESCRIPTION, THUMBNAIL_URL),
    }
)

# Expected header of the raw file, used to validate the reconstruction step.
EXPECTED_COLUMNS: Sequence[str] = (
    ID, TARGET, PROPERTY_TYPE, ROOM_TYPE, AMENITIES, ACCOMMODATES, BATHROOMS,
    BED_TYPE, CANCELLATION_POLICY, CLEANING_FEE, CITY, DESCRIPTION, FIRST_REVIEW,
    HOST_HAS_PROFILE_PIC, HOST_IDENTITY_VERIFIED, HOST_RESPONSE_RATE, HOST_SINCE,
    INSTANT_BOOKABLE, LAST_REVIEW, LATITUDE, LONGITUDE, NAME, NEIGHBOURHOOD,
    NUMBER_OF_REVIEWS, REVIEW_SCORES_RATING, THUMBNAIL_URL, ZIPCODE, BEDROOMS, BEDS,
)
