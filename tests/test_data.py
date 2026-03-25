"""Data validation tests for raw and cleaned datasets."""

from pathlib import Path

import pandas as pd


class TestRawRidership:
    def test_file_exists(self):
        assert Path("data/raw/ridership_monthly.csv").exists()

    def test_row_count_positive(self):
        df = pd.read_csv("data/raw/ridership_monthly.csv")
        assert len(df) > 0, f"Raw ridership has {len(df)} rows"

    def test_expected_columns(self):
        df = pd.read_csv("data/raw/ridership_monthly.csv", nrows=1)
        expected = {"Year", "Month", "Line Name", "Line Category"}
        actual = set(df.columns)
        assert expected.issubset(actual), f"Missing columns. Got: {actual}"

    def test_no_null_year_or_line(self):
        df = pd.read_csv("data/raw/ridership_monthly.csv")
        assert df["Year"].notna().all(), "Null values in Year column"
        assert df["Line Name"].notna().all(), "Null values in Line Name column"

    def test_year_range_covers_study_period(self):
        df = pd.read_csv("data/raw/ridership_monthly.csv")
        assert df["Year"].min() <= 2013, f"Data starts too late: {df['Year'].min()}"
        assert df["Year"].max() >= 2019, f"Data ends too early: {df['Year'].max()}"


class TestRawStationLocations:
    def test_file_exists(self):
        assert Path("data/raw/station_locations.csv").exists()

    def test_row_count_minimum(self):
        df = pd.read_csv("data/raw/station_locations.csv")
        assert len(df) >= 6, f"Station locations has {len(df)} rows, need >= 6"

    def test_expected_columns(self):
        df = pd.read_csv("data/raw/station_locations.csv", nrows=1)
        expected = {"station_name", "line", "lat", "lon", "opened_date", "is_foothill_2016"}
        assert expected.issubset(set(df.columns)), f"Missing columns. Got: {set(df.columns)}"

    def test_foothill_stations_count(self):
        df = pd.read_csv("data/raw/station_locations.csv")
        foothill = df[df["is_foothill_2016"] == True]
        assert len(foothill) == 6, f"Expected 6 Foothill stations, got {len(foothill)}"

    def test_coordinates_in_la_range(self):
        df = pd.read_csv("data/raw/station_locations.csv")
        assert (df["lat"] >= 33.0).all() and (df["lat"] <= 35.0).all(), "Lat out of LA range"
        assert (df["lon"] >= -119.0).all() and (df["lon"] <= -117.0).all(), "Lon out of LA range"


class TestCleanRidership:
    def test_file_exists(self):
        assert Path("data/clean/ridership_clean.csv").exists()

    def test_no_null_join_keys(self):
        df = pd.read_csv("data/clean/ridership_clean.csv")
        assert df["date"].notna().all(), "Null dates in clean ridership"
        assert df["line_id"].notna().all(), "Null line_ids in clean ridership"
        assert df["avg_daily_boardings"].notna().all(), "Null boardings"

    def test_has_treatment_columns(self):
        df = pd.read_csv("data/clean/ridership_clean.csv", nrows=1)
        assert "is_treatment" in df.columns, "Missing is_treatment column"
        assert "period" in df.columns, "Missing period column"
        assert "line_id" in df.columns, "Missing line_id column"

    def test_date_range_spans_study_period(self):
        df = pd.read_csv("data/clean/ridership_clean.csv")
        df["date"] = pd.to_datetime(df["date"])
        assert df["date"].min().year <= 2013, f"Data starts too late: {df['date'].min()}"
        assert df["date"].max().year >= 2019, f"Data ends too early: {df['date'].max()}"

    def test_gold_line_exists(self):
        df = pd.read_csv("data/clean/ridership_clean.csv")
        assert "gold" in df["line_id"].values, "No gold line in treatment data"

    def test_no_brt_lines(self):
        df = pd.read_csv("data/clean/ridership_clean.csv")
        line_names = set(df["line_name"].unique())
        assert "G Line" not in line_names, "BRT G Line should be filtered out"
        assert "J Line" not in line_names, "BRT J Line should be filtered out"

    def test_period_values(self):
        df = pd.read_csv("data/clean/ridership_clean.csv")
        valid_periods = {"pre", "post", "transition"}
        assert set(df["period"].unique()).issubset(valid_periods), (
            f"Unexpected period values: {set(df['period'].unique()) - valid_periods}"
        )


class TestCleanStationLocations:
    def test_file_exists(self):
        assert Path("data/clean/station_locations_clean.csv").exists()

    def test_foothill_stations(self):
        df = pd.read_csv("data/clean/station_locations_clean.csv")
        foothill = df[df["is_foothill_2016"] == True]
        assert len(foothill) == 6, f"Expected 6 Foothill stations, got {len(foothill)}"

    def test_coordinates_validated(self):
        df = pd.read_csv("data/clean/station_locations_clean.csv")
        assert (df["lat"] >= 33.0).all() and (df["lat"] <= 35.0).all()
        assert (df["lon"] >= -119.0).all() and (df["lon"] <= -117.0).all()
