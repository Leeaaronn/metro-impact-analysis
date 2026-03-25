"""
Data cleaning and standardization for LA Metro ridership impact analysis.

Transforms raw CSVs (from acquire.py) into analysis-ready datasets with
standardized line names, treatment/control flags, and pre/post period labels.
"""

import pathlib

import pandas as pd


# ---------------------------------------------------------------------------
# Line name → standardized line_id mapping
# ---------------------------------------------------------------------------
_LINE_ID_MAP: dict[str, str] = {
    "L Line": "gold",
    "B Line": "red",
    "C Line": "green",
    "D Line": "purple",
    "E Line": "expo",
    "K Line": "k_line",
}

# BRT lines to exclude from rail analysis
_BRT_LINES: set[str] = {"G Line", "J Line"}


def clean_ridership(
    input_path: str = "data/raw/ridership_monthly.csv",
    output_path: str = "data/clean/ridership_clean.csv",
) -> pd.DataFrame:
    """Clean and standardize raw ridership data for analysis.

    Reads the Streets For All extract, filters out BRT lines, standardizes
    line names across the Gold->L->A Line evolution, and adds treatment/control
    and pre/post period columns.

    Parameters
    ----------
    input_path : str
        Path to raw ridership CSV from acquire.py.
    output_path : str
        Destination for cleaned CSV.

    Returns
    -------
    pd.DataFrame
        Cleaned ridership DataFrame.
    """
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    print(f"Before cleaning: {len(df)} rows")

    # Filter out BRT lines (G Line = Orange BRT, J Line = Silver BRT)
    df = df[~df["Line Name"].isin(_BRT_LINES)].copy()
    print(f"After BRT filter: {len(df)} rows")

    # Build date column from Year + Month (numeric)
    df["date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str).str.zfill(2) + "-01"
    )

    # Drop the numeric line_name column (raw code like 801) before renaming
    if "line_name" in df.columns:
        df = df.drop(columns=["line_name"])

    # Rename to snake_case
    df = df.rename(
        columns={
            "Year": "year",
            "Month": "month",
            "Line Name": "line_name",
            "Former Name": "former_name",
            "Line Category": "line_category",
            "Avg. Daily Boardings (Weekday)": "avg_daily_boardings",
            "Avg. Daily Boardings (Saturday)": "avg_daily_boardings_sat",
            "Avg. Daily Boardings (Sunday)": "avg_daily_boardings_sun",
        }
    )

    # Map line_name to standardized line_id
    # Key complexity: A Line = former Blue Line pre-June 2023,
    # but A Line absorbed Gold Line post-Regional Connector (June 2023)
    regional_connector_date = pd.Timestamp("2023-06-16")

    def _assign_line_id(row: pd.Series) -> str:
        name = row["line_name"]
        if name == "L Line":
            return "gold"
        if name == "A Line":
            if row["date"] < regional_connector_date:
                return "a_line"
            return "a_line_merged"
        return _LINE_ID_MAP.get(name, name.lower().replace(" ", "_"))

    df["line_id"] = df.apply(_assign_line_id, axis=1)

    # Treatment flag: Gold Line received the Foothill Extension
    df["is_treatment"] = df["line_id"].isin(["gold", "a_line_merged"])

    # Period labels relative to March 2016 extension opening
    pre_cutoff = pd.Timestamp("2016-03-01")
    post_cutoff = pd.Timestamp("2016-04-01")

    def _assign_period(date: pd.Timestamp) -> str:
        if date < pre_cutoff:
            return "pre"
        if date >= post_cutoff:
            return "post"
        return "transition"

    df["period"] = df["date"].apply(_assign_period)

    # Drop rows with nulls in key columns
    key_cols = ["date", "line_name", "avg_daily_boardings"]
    before_drop = len(df)
    df = df.dropna(subset=key_cols)
    if len(df) < before_drop:
        print(f"Dropped {before_drop - len(df)} rows with null key values")

    # Sort and select output columns
    df = df.sort_values(["date", "line_name"]).reset_index(drop=True)

    output_cols = [
        "date",
        "year",
        "month",
        "line_name",
        "former_name",
        "line_id",
        "avg_daily_boardings",
        "avg_daily_boardings_sat",
        "avg_daily_boardings_sun",
        "is_treatment",
        "period",
    ]
    df = df[output_cols]

    # Report
    print(f"After cleaning: {len(df)} rows")
    print(f"Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"Lines found: {sorted(df['line_id'].unique())}")

    # Check for monthly gaps per line
    for lid in df["line_id"].unique():
        line_dates = df[df["line_id"] == lid]["date"].sort_values()
        expected_months = pd.date_range(
            line_dates.min(), line_dates.max(), freq="MS"
        )
        missing = set(expected_months) - set(line_dates)
        if missing:
            missing_strs = sorted(m.strftime("%Y-%m") for m in missing)
            print(f"WARNING: {lid} has {len(missing)} missing months: {missing_strs[:5]}")

    # Save
    df.to_csv(out, index=False)
    print(f"Saved to {out}")
    return df


def clean_station_locations(
    input_path: str = "data/raw/station_locations.csv",
    output_path: str = "data/clean/station_locations_clean.csv",
) -> pd.DataFrame:
    """Clean and validate station location data.

    Parameters
    ----------
    input_path : str
        Path to raw station locations CSV.
    output_path : str
        Destination for cleaned CSV.

    Returns
    -------
    pd.DataFrame
        Cleaned station DataFrame.
    """
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)

    # Parse opened_date
    df["opened_date"] = pd.to_datetime(df["opened_date"])

    # Validate no nulls in key columns
    for col in ["station_name", "line", "lat", "lon"]:
        null_count = df[col].isna().sum()
        if null_count > 0:
            print(f"WARNING: {null_count} null values in {col}")

    # Validate coordinates are in LA County range
    lat_ok = (df["lat"] >= 33.0) & (df["lat"] <= 35.0)
    lon_ok = (df["lon"] >= -119.0) & (df["lon"] <= -117.0)
    if not lat_ok.all() or not lon_ok.all():
        bad = df[~(lat_ok & lon_ok)]
        print(f"WARNING: {len(bad)} stations with out-of-range coordinates")

    n_foothill = df["is_foothill_2016"].sum()
    print(f"Stations: {len(df)} total, {n_foothill} Foothill 2016 treatment")

    df.to_csv(out, index=False)
    print(f"Saved to {out}")
    return df


if __name__ == "__main__":
    print("=== Data Cleaning ===\n")

    ridership = clean_ridership()
    print()

    stations = clean_station_locations()

    print("\n=== Cleaning complete ===")
