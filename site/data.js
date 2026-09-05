window.DATA = {
 "profile": {
  "rows": 74080,
  "columns": 30,
  "column_profiles": [
   {
    "name": "id",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 74080,
    "sample": "6901257"
   },
   {
    "name": "log_price",
    "dtype": "float64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 767,
    "sample": "5.010635294096256"
   },
   {
    "name": "property_type",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 35,
    "sample": "Apartment"
   },
   {
    "name": "room_type",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 3,
    "sample": "Entire home/apt"
   },
   {
    "name": "amenities",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 67096,
    "sample": "{\"Wireless Internet\",\"Air conditioning\",Kitchen,Heating,\"Fa…"
   },
   {
    "name": "accommodates",
    "dtype": "int64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 16,
    "sample": "3"
   },
   {
    "name": "bathrooms",
    "dtype": "float64",
    "non_null": 73881,
    "missing": 199,
    "missing_pct": 0.27,
    "unique": 17,
    "sample": "1.0"
   },
   {
    "name": "bed_type",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 5,
    "sample": "Real Bed"
   },
   {
    "name": "cancellation_policy",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 5,
    "sample": "strict"
   },
   {
    "name": "cleaning_fee",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 2,
    "sample": "True"
   },
   {
    "name": "city",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 6,
    "sample": "NYC"
   },
   {
    "name": "description",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 73450,
    "sample": "Beautiful, sunlit brownstone 1-bedroom in the loveliest nei…"
   },
   {
    "name": "first_review",
    "dtype": "datetime64[ns]",
    "non_null": 58224,
    "missing": 15856,
    "missing_pct": 21.4,
    "unique": 2554,
    "sample": "2016-06-18 00:00:00"
   },
   {
    "name": "host_has_profile_pic",
    "dtype": "object",
    "non_null": 73892,
    "missing": 188,
    "missing_pct": 0.25,
    "unique": 2,
    "sample": "t"
   },
   {
    "name": "host_identity_verified",
    "dtype": "object",
    "non_null": 73892,
    "missing": 188,
    "missing_pct": 0.25,
    "unique": 2,
    "sample": "t"
   },
   {
    "name": "host_response_rate",
    "dtype": "object",
    "non_null": 55789,
    "missing": 18291,
    "missing_pct": 24.69,
    "unique": 80,
    "sample": "100%"
   },
   {
    "name": "host_since",
    "dtype": "datetime64[ns]",
    "non_null": 73892,
    "missing": 188,
    "missing_pct": 0.25,
    "unique": 3086,
    "sample": "2012-03-26 00:00:00"
   },
   {
    "name": "instant_bookable",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 2,
    "sample": "f"
   },
   {
    "name": "last_review",
    "dtype": "datetime64[ns]",
    "non_null": 58261,
    "missing": 15819,
    "missing_pct": 21.35,
    "unique": 1371,
    "sample": "2016-07-18 00:00:00"
   },
   {
    "name": "latitude",
    "dtype": "float64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 74080,
    "sample": "40.69652362997075"
   },
   {
    "name": "longitude",
    "dtype": "float64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 74080,
    "sample": "-73.99161684624262"
   },
   {
    "name": "name",
    "dtype": "object",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 73329,
    "sample": "Beautiful brownstone 1-bedroom"
   },
   {
    "name": "neighbourhood",
    "dtype": "object",
    "non_null": 67211,
    "missing": 6869,
    "missing_pct": 9.27,
    "unique": 619,
    "sample": "Brooklyn Heights"
   },
   {
    "name": "number_of_reviews",
    "dtype": "int64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 371,
    "sample": "2"
   },
   {
    "name": "review_scores_rating",
    "dtype": "float64",
    "non_null": 57366,
    "missing": 16714,
    "missing_pct": 22.56,
    "unique": 54,
    "sample": "100.0"
   },
   {
    "name": "thumbnail_url",
    "dtype": "object",
    "non_null": 65865,
    "missing": 8215,
    "missing_pct": 11.09,
    "unique": 65853,
    "sample": "https://a0.muscache.com/im/pictures/6d7cbbf7-c034-459c-bc82…"
   },
   {
    "name": "zipcode",
    "dtype": "object",
    "non_null": 73114,
    "missing": 966,
    "missing_pct": 1.3,
    "unique": 767,
    "sample": "11201"
   },
   {
    "name": "bedrooms",
    "dtype": "float64",
    "non_null": 73989,
    "missing": 91,
    "missing_pct": 0.12,
    "unique": 11,
    "sample": "1.0"
   },
   {
    "name": "beds",
    "dtype": "float64",
    "non_null": 73949,
    "missing": 131,
    "missing_pct": 0.18,
    "unique": 18,
    "sample": "1.0"
   },
   {
    "name": "price_usd",
    "dtype": "float64",
    "non_null": 74080,
    "missing": 0,
    "missing_pct": 0.0,
    "unique": 767,
    "sample": "150.00000000000009"
   }
  ],
  "duplicated_rows": 0,
  "duplicated_ids": 0
 },
 "numeric": [
  {
   "name": "log_price",
   "count": 74080,
   "mean": 4.782135682516876,
   "std": 0.7174059604043728,
   "minimum": 0.0,
   "q1": 4.31748811353631,
   "median": 4.709530201312334,
   "q3": 5.220355825078324,
   "maximum": 7.6004023345004
  },
  {
   "name": "accommodates",
   "count": 74080,
   "mean": 3.155440064794816,
   "std": 2.153741740830514,
   "minimum": 1.0,
   "q1": 2.0,
   "median": 2.0,
   "q3": 4.0,
   "maximum": 16.0
  },
  {
   "name": "bathrooms",
   "count": 73881,
   "mean": 1.2352905347789012,
   "std": 0.5821179915618827,
   "minimum": 0.0,
   "q1": 1.0,
   "median": 1.0,
   "q3": 1.0,
   "maximum": 8.0
  },
  {
   "name": "bedrooms",
   "count": 73989,
   "mean": 1.265836813580397,
   "std": 0.8522067601394938,
   "minimum": 0.0,
   "q1": 1.0,
   "median": 1.0,
   "q3": 1.0,
   "maximum": 10.0
  },
  {
   "name": "beds",
   "count": 73949,
   "mean": 1.7109764837928843,
   "std": 1.254298070624233,
   "minimum": 0.0,
   "q1": 1.0,
   "median": 1.0,
   "q3": 2.0,
   "maximum": 18.0
  },
  {
   "name": "number_of_reviews",
   "count": 74080,
   "mean": 20.89715172786177,
   "std": 37.82249949275012,
   "minimum": 0.0,
   "q1": 1.0,
   "median": 6.0,
   "q3": 23.0,
   "maximum": 605.0
  },
  {
   "name": "review_scores_rating",
   "count": 57366,
   "mean": 94.06730467524318,
   "std": 7.836996581132894,
   "minimum": 20.0,
   "q1": 92.0,
   "median": 96.0,
   "q3": 100.0,
   "maximum": 100.0
  },
  {
   "name": "latitude",
   "count": 74080,
   "mean": 38.446057686448604,
   "std": 3.0801643211857135,
   "minimum": 33.33890467150096,
   "q1": 34.12791254226718,
   "median": 40.66213891891258,
   "q3": 40.746096410480156,
   "maximum": 42.39043717872241
  },
  {
   "name": "longitude",
   "count": 74080,
   "mean": -92.39725390699437,
   "std": 21.70506752726615,
   "minimum": -122.51149998987214,
   "q1": -118.3423932846827,
   "median": -76.99697076923209,
   "q3": -73.95465837743028,
   "maximum": -70.98504659974512
  }
 ],
 "categorical": [
  {
   "name": "city",
   "unique": 6,
   "top_values": {
    "NYC": 32334,
    "LA": 22443,
    "SF": 6431,
    "DC": 5686,
    "Chicago": 3719,
    "Boston": 3467
   },
   "missing_pct": 0.0
  },
  {
   "name": "room_type",
   "unique": 3,
   "top_values": {
    "Entire home/apt": 41299,
    "Private room": 30621,
    "Shared room": 2160
   },
   "missing_pct": 0.0
  },
  {
   "name": "property_type",
   "unique": 35,
   "top_values": {
    "Apartment": 48981,
    "House": 16505,
    "Condominium": 2658,
    "Townhouse": 1692,
    "Loft": 1244,
    "Other": 607
   },
   "missing_pct": 0.0
  },
  {
   "name": "bed_type",
   "unique": 5,
   "top_values": {
    "Real Bed": 72000,
    "Futon": 752,
    "Pull-out Sofa": 585,
    "Airbed": 476,
    "Couch": 267
   },
   "missing_pct": 0.0
  },
  {
   "name": "cancellation_policy",
   "unique": 5,
   "top_values": {
    "strict": 32363,
    "flexible": 22537,
    "moderate": 19051,
    "super_strict_30": 112,
    "super_strict_60": 17
   },
   "missing_pct": 0.0
  },
  {
   "name": "cleaning_fee",
   "unique": 2,
   "top_values": {
    "True": 54385,
    "False": 19695
   },
   "missing_pct": 0.0
  },
  {
   "name": "instant_bookable",
   "unique": 2,
   "top_values": {
    "f": 54640,
    "t": 19440
   },
   "missing_pct": 0.0
  },
  {
   "name": "host_identity_verified",
   "unique": 2,
   "top_values": {
    "t": 49725,
    "f": 24167
   },
   "missing_pct": 0.25
  },
  {
   "name": "host_has_profile_pic",
   "unique": 2,
   "top_values": {
    "t": 73667,
    "f": 225
   },
   "missing_pct": 0.25
  },
  {
   "name": "neighbourhood",
   "unique": 619,
   "top_values": {
    "Williamsburg": 2861,
    "Bedford-Stuyvesant": 2165,
    "Bushwick": 1601,
    "Upper West Side": 1396,
    "Mid-Wilshire": 1392,
    "Harlem": 1374
   },
   "missing_pct": 9.27
  }
 ],
 "anomalies": [
  {
   "code": "MISSING-HIGH",
   "title": "Columns with a high share of missing values",
   "affected_columns": [
    "host_response_rate",
    "review_scores_rating",
    "first_review",
    "last_review"
   ],
   "observed": "host_response_rate: 24.69%; review_scores_rating: 22.56%; first_review: 21.4%; last_review: 21.35%",
   "severity": "high",
   "proposed_treatment": "Do not drop rows. Add a 'no reviews / unknown' flag and impute separately during Activity 3."
  },
  {
   "code": "MISSING-MODERATE",
   "title": "Columns with a moderate share of missing values",
   "affected_columns": [
    "thumbnail_url",
    "neighbourhood",
    "zipcode"
   ],
   "observed": "thumbnail_url: 11.09%; neighbourhood: 9.27%; zipcode: 1.3%",
   "severity": "medium",
   "proposed_treatment": "Use an 'Unknown' category for text columns and per-city medians for numeric ones."
  },
  {
   "code": "DUPLICATES",
   "title": "Duplicated records",
   "affected_columns": [
    "id"
   ],
   "observed": "0 repeated ids and 0 identical rows",
   "severity": "low",
   "proposed_treatment": "Re-check after cleaning; no action needed if both are zero."
  },
  {
   "code": "PRICE_OUTLIERS",
   "title": "Extreme prices and possible upper censoring",
   "affected_columns": [
    "log_price",
    "price_usd"
   ],
   "observed": "160 listings at USD 20 or less (minimum USD 1); 668 at USD 1000 or more; maximum USD 1999; 537 below USD 10 per guest",
   "severity": "high",
   "proposed_treatment": "Review both tails, document the apparent USD 1,999 cap and consider trimming the 1st and 99th percentiles before modelling."
  },
  {
   "code": "ZEROS",
   "title": "Zero values that may be legitimate or hidden gaps",
   "affected_columns": [
    "bedrooms",
    "bathrooms",
    "beds"
   ],
   "observed": "bedrooms = 0 in 6713 rows; bathrooms = 0 in 198 rows; beds = 0 in 4 rows",
   "severity": "medium",
   "proposed_treatment": "Treat bedrooms = 0 as a studio flag; review zeros in bathrooms and beds individually."
  },
  {
   "code": "FORMATS-ZIP",
   "title": "Inconsistent postal code format",
   "affected_columns": [
    "zipcode"
   ],
   "observed": "8875 values do not match a 5-digit pattern (e.g. '94117.0'); 767 distinct values in total",
   "severity": "medium",
   "proposed_treatment": "Normalise to five digits before using it as a location key."
  },
  {
   "code": "FORMATS-BOOL",
   "title": "Numeric and boolean values stored as text",
   "affected_columns": [
    "host_response_rate",
    "cleaning_fee",
    "instant_bookable"
   ],
   "observed": "host_response_rate keeps the '%' sign; cleaning_fee uses 'True'/'False' while the other boolean columns use 't'/'f'",
   "severity": "medium",
   "proposed_treatment": "Convert the rate to a decimal and unify booleans to 0/1."
  },
  {
   "code": "CARDINALITY",
   "title": "High-cardinality categorical variables",
   "affected_columns": [
    "neighbourhood",
    "zipcode",
    "property_type"
   ],
   "observed": "neighbourhood: 619 levels; zipcode: 767 levels; property_type: 35 levels",
   "severity": "medium",
   "proposed_treatment": "Group rare levels into 'Other' and use frequency or target encoding validated inside each city."
  },
  {
   "code": "TEXT",
   "title": "Unstructured text pending extraction",
   "affected_columns": [
    "amenities",
    "description",
    "name"
   ],
   "observed": "amenities holds 17.6 items on average and 585 empty lists; description and name are free text",
   "severity": "medium",
   "proposed_treatment": "Turn the most frequent amenities into binary indicators; postpone description and name to a text-processing stage."
  }
 ],
 "figures": [
  {
   "file": "fig1_price_distribution.png",
   "title": "Distribución del precio por noche y de log_price"
  },
  {
   "file": "fig2_price_by_room_type.png",
   "title": "Precio por noche según tipo de espacio (room_type)"
  },
  {
   "file": "fig3_price_vs_accommodates.png",
   "title": "Precio mediano según capacidad y tipo de espacio"
  },
  {
   "file": "fig4_price_by_city.png",
   "title": "Precio mediano por ciudad"
  },
  {
   "file": "fig5_missing_values.png",
   "title": "Valores faltantes por variable (% de registros)"
  }
 ],
 "extras": {
  "source": "Excel workbook 'airbnb_price_prediction.xlsx' (sheet 'in') cached at 'listings.parquet'",
  "malformed_records": 19,
  "spreadsheet_records": 74099
 },
 "generated_at": "2026-09-05 22:10 UTC",
 "price": {
  "median": 111.0,
  "mean": 160.38,
  "p10": 50.0,
  "p90": 300.0,
  "maximum": 1999.0
 },
 "by_city": [
  {
   "label": "SF",
   "listings": 6431,
   "median_price": 165.0
  },
  {
   "label": "Boston",
   "listings": 3467,
   "median_price": 136.0
  },
  {
   "label": "DC",
   "listings": 5686,
   "median_price": 125.0
  },
  {
   "label": "NYC",
   "listings": 32334,
   "median_price": 105.0
  },
  {
   "label": "LA",
   "listings": 22443,
   "median_price": 100.0
  },
  {
   "label": "Chicago",
   "listings": 3719,
   "median_price": 99.0
  }
 ],
 "by_room_type": [
  {
   "label": "Entire home/apt",
   "listings": 41299,
   "median_price": 160.0
  },
  {
   "label": "Private room",
   "listings": 30621,
   "median_price": 75.0
  },
  {
   "label": "Shared room",
   "listings": 2160,
   "median_price": 45.0
  }
 ]
};
