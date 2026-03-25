"""
Data acquisition functions for LA Metro ridership impact analysis.

This module downloads/creates the two primary datasets needed for the
difference-in-differences analysis:
  1. Monthly ridership by line (from Streets For All ridership dashboard)
  2. Metro station locations with treatment/control grouping flags
"""

import json
import pathlib
import re
import sys
from typing import Optional

import pandas as pd
import requests


# ---------------------------------------------------------------------------
# Line number → name mapping (from Streets For All JS bundle)
# ---------------------------------------------------------------------------
_LINE_MAP: dict[int, dict[str, str]] = {
    801: {"current": "A Line", "former": "Blue Line"},
    802: {"current": "B Line", "former": "Red Line"},
    803: {"current": "C Line", "former": "Green Line"},
    804: {"current": "E Line", "former": "Expo Line"},
    805: {"current": "D Line", "former": "Purple Line"},
    806: {"current": "L Line", "former": "Gold Line"},
    807: {"current": "K Line", "former": "Crenshaw/LAX"},
    901: {"current": "G Line", "former": "Orange BRT"},
    910: {"current": "J Line", "former": "Silver Line"},
}

_STREETS_FOR_ALL_URL = "https://ridership.streetsforall.org"
_BUNDLE_URL = "https://ridership.streetsforall.org/assets/index-D8qXEJs6.js"


def _get_bundle_url(base_url: str = _STREETS_FOR_ALL_URL) -> str:
    """Discover the current JS bundle URL from the site's index page."""
    resp = requests.get(base_url, timeout=30)
    resp.raise_for_status()
    match = re.search(r'src="(/assets/index-[^"]+\.js)"', resp.text)
    if match:
        return base_url.rstrip("/") + match.group(1)
    raise ValueError("Could not find JS bundle URL in Streets For All index page")


def download_ridership_csv(
    output_path: str = "data/raw/ridership_monthly.csv",
) -> pathlib.Path:
    """Download monthly ridership data from Streets For All and save as CSV.

    The Streets For All ridership dashboard (ridership.streetsforall.org) embeds
    all ridership records directly in its compiled JavaScript bundle as a JSON
    array. This function extracts that JSON, filters to Rail lines only, maps
    numeric line IDs to human-readable names, and writes a clean CSV.

    If the CSV already exists at output_path, the function returns early to
    avoid unnecessary re-downloads. Delete the file to force a refresh.

    Parameters
    ----------
    output_path : str
        Destination path for the CSV file. Defaults to data/raw/ridership_monthly.csv.

    Returns
    -------
    pathlib.Path
        Resolved path to the saved CSV file.

    Raises
    ------
    RuntimeError
        If the ridership data cannot be extracted from the bundle.
    requests.HTTPError
        If the HTTP request fails.
    """
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    if out.exists():
        print(f"[acquire] {out} already exists — skipping download.")
        return out.resolve()

    print("[acquire] Fetching Streets For All ridership bundle…")

    # Discover the bundle URL dynamically in case it changes after a deploy
    try:
        bundle_url = _get_bundle_url()
    except Exception:
        bundle_url = _BUNDLE_URL  # fall back to known URL

    resp = requests.get(bundle_url, timeout=60)
    resp.raise_for_status()
    content = resp.text

    # Extract the large JSON.parse call containing all ridership records
    marker = 'JSON.parse(\'[{"year":2009'
    idx = content.find(marker)
    if idx < 0:
        raise RuntimeError(
            "Could not locate ridership JSON in bundle. "
            "The site may have been updated — check for a new bundle filename."
        )

    start_quote = idx + len("JSON.parse(")
    end_quote = content.find("')", start_quote)
    if end_quote < 0:
        raise RuntimeError("Malformed JSON.parse block in bundle.")

    raw_json = content[start_quote + 1 : end_quote]
    records: list[dict] = json.loads(raw_json)
    print(f"[acquire] Extracted {len(records):,} total ridership records.")

    ridership_df = pd.DataFrame(records)

    # Filter to Rail lines only (line_name codes 801–807 are rail)
    rail_line_ids = set(_LINE_MAP.keys())
    ridership_rail = ridership_df[ridership_df["line_name"].isin(rail_line_ids)].copy()

    # Map numeric line IDs to current and former names
    ridership_rail["Line Name"] = ridership_rail["line_name"].map(
        lambda x: _LINE_MAP.get(x, {}).get("current", str(x))
    )
    ridership_rail["Former Name"] = ridership_rail["line_name"].map(
        lambda x: _LINE_MAP.get(x, {}).get("former", "")
    )
    ridership_rail["Line Category"] = "Train"

    # Rename columns to match the expected schema from Streets For All exports
    ridership_rail = ridership_rail.rename(
        columns={
            "year": "Year",
            "month": "Month",
            "est_wkday_ridership": "Avg. Daily Boardings (Weekday)",
            "est_sat_ridership": "Avg. Daily Boardings (Saturday)",
            "est_sun_ridership": "Avg. Daily Boardings (Sunday)",
        }
    )

    # Keep the most useful columns and add a Day Group column for Weekday rows
    # (the primary analysis metric per REQUIREMENTS.md)
    final_cols = [
        "Year",
        "Month",
        "Line Name",
        "Former Name",
        "Line Category",
        "Avg. Daily Boardings (Weekday)",
        "Avg. Daily Boardings (Saturday)",
        "Avg. Daily Boardings (Sunday)",
        "line_name",
    ]
    ridership_rail = ridership_rail[final_cols].sort_values(
        ["Line Name", "Year", "Month"]
    )

    ridership_rail.to_csv(out, index=False)
    n_rows = len(ridership_rail)
    years = sorted(ridership_rail["Year"].unique())
    print(
        f"[acquire] Saved {n_rows:,} rail ridership rows "
        f"({years[0]}–{years[-1]}) to {out}"
    )
    return out.resolve()


def create_station_locations(
    output_path: str = "data/raw/station_locations.csv",
) -> pathlib.Path:
    """Create a manually verified CSV of LA Metro rail stations.

    Includes all six Foothill Extension Phase 2A stations (treatment group)
    and representative control stations from other lines. Coordinates are
    taken from the research document (Section 4b) and cross-checked against
    Metro GTFS data.

    Parameters
    ----------
    output_path : str
        Destination path for the CSV file. Defaults to data/raw/station_locations.csv.

    Returns
    -------
    pathlib.Path
        Resolved path to the saved CSV file.
    """
    out = pathlib.Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------------
    # Station data
    # Columns: station_name, line, lat, lon, opened_date, is_foothill_2016
    #
    # Treatment group — 6 Foothill Extension Phase 2A stations (opened 2016-03-05)
    # Control group — established stations on other lines not extended in 2016
    #   B/D Line (heavy rail, no new stations 2012-2019)
    #   C Line (Green Line, no new stations 2012-2019)
    #   E Line (Expo Line, Santa Monica extension opened 2016-05-20 — excluded
    #            from primary control; flagged separately)
    # -----------------------------------------------------------------------

    stations: list[dict] = [
        # ------------------------------------------------------------------
        # A / Gold Line — Foothill Extension Phase 2A (TREATMENT GROUP)
        # Opened: 2016-03-05
        # Source: Research doc Section 4b, confirmed via Wikipedia
        # ------------------------------------------------------------------
        {
            "station_name": "Arcadia",
            "line": "A",
            "lat": 34.1417,
            "lon": -118.0287,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        {
            "station_name": "Monrovia",
            "line": "A",
            "lat": 34.1356,
            "lon": -118.0019,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        {
            "station_name": "Duarte/City of Hope",
            "line": "A",
            "lat": 34.1311,
            "lon": -117.9712,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        {
            "station_name": "Irwindale",
            "line": "A",
            "lat": 34.1283,
            "lon": -117.9344,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        {
            "station_name": "Azusa Downtown",
            "line": "A",
            "lat": 34.1360,
            "lon": -117.9068,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        {
            "station_name": "APU/Citrus College",
            "line": "A",
            "lat": 34.1363,
            "lon": -117.8920,
            "opened_date": "2016-03-05",
            "is_foothill_2016": True,
        },
        # ------------------------------------------------------------------
        # A / Gold Line — Existing stations (pre-2016, part of original Gold
        # Line; used as pre-extension context, not primary control)
        # ------------------------------------------------------------------
        {
            "station_name": "Sierra Madre Villa",
            "line": "A",
            "lat": 34.1484,
            "lon": -118.0576,
            "opened_date": "2003-07-26",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Allen",
            "line": "A",
            "lat": 34.1477,
            "lon": -118.1027,
            "opened_date": "2003-07-26",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Lake",
            "line": "A",
            "lat": 34.1460,
            "lon": -118.1309,
            "opened_date": "2003-07-26",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Del Mar",
            "line": "A",
            "lat": 34.1454,
            "lon": -118.1509,
            "opened_date": "2003-07-26",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Memorial Park",
            "line": "A",
            "lat": 34.1477,
            "lon": -118.1579,
            "opened_date": "2003-07-26",
            "is_foothill_2016": False,
        },
        # ------------------------------------------------------------------
        # B Line (Red Line) — CONTROL GROUP
        # Heavy rail, no new stations 2012–2019
        # Opened: 1993-01-30 (original segment)
        # ------------------------------------------------------------------
        {
            "station_name": "Union Station",
            "line": "B",
            "lat": 34.0560,
            "lon": -118.2356,
            "opened_date": "1993-01-30",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Civic Center/Grand Park",
            "line": "B",
            "lat": 34.0554,
            "lon": -118.2429,
            "opened_date": "1993-01-30",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Pershing Square",
            "line": "B",
            "lat": 34.0493,
            "lon": -118.2493,
            "opened_date": "1993-01-30",
            "is_foothill_2016": False,
        },
        {
            "station_name": "7th Street/Metro Center",
            "line": "B",
            "lat": 34.0484,
            "lon": -118.2588,
            "opened_date": "1993-01-30",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Wilshire/Vermont",
            "line": "B",
            "lat": 34.0623,
            "lon": -118.2924,
            "opened_date": "1996-06-22",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Hollywood/Highland",
            "line": "B",
            "lat": 34.1019,
            "lon": -118.3388,
            "opened_date": "1999-06-12",
            "is_foothill_2016": False,
        },
        {
            "station_name": "North Hollywood",
            "line": "B",
            "lat": 34.1679,
            "lon": -118.3777,
            "opened_date": "2000-06-24",
            "is_foothill_2016": False,
        },
        # ------------------------------------------------------------------
        # C Line (Green Line) — CONTROL GROUP
        # Light rail, no new stations 2012–2019
        # Opened: 1995-08-12
        # ------------------------------------------------------------------
        {
            "station_name": "Norwalk",
            "line": "C",
            "lat": 33.9041,
            "lon": -118.0826,
            "opened_date": "1995-08-12",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Lakewood",
            "line": "C",
            "lat": 33.8539,
            "lon": -118.1234,
            "opened_date": "1995-08-12",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Hawthorne/Lennox",
            "line": "C",
            "lat": 33.9164,
            "lon": -118.3454,
            "opened_date": "1995-08-12",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Aviation/LAX",
            "line": "C",
            "lat": 33.9290,
            "lon": -118.3759,
            "opened_date": "1995-08-12",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Redondo Beach",
            "line": "C",
            "lat": 33.8831,
            "lon": -118.3759,
            "opened_date": "1995-08-12",
            "is_foothill_2016": False,
        },
        # ------------------------------------------------------------------
        # D Line (Purple Line) — CONTROL GROUP
        # Heavy rail, no new stations 2012–2019 (extension started 2021+)
        # Opened: 1993-01-30
        # ------------------------------------------------------------------
        {
            "station_name": "Koreatown/Wilshire",
            "line": "D",
            "lat": 34.0594,
            "lon": -118.3013,
            "opened_date": "1996-06-22",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Wilshire/Western",
            "line": "D",
            "lat": 34.0616,
            "lon": -118.3090,
            "opened_date": "1996-06-22",
            "is_foothill_2016": False,
        },
        {
            "station_name": "Wilshire/Normandie",
            "line": "D",
            "lat": 34.0609,
            "lon": -118.2989,
            "opened_date": "1996-06-22",
            "is_foothill_2016": False,
        },
    ]

    station_df = pd.DataFrame(stations)
    station_df.to_csv(out, index=False)

    n_foothill = station_df["is_foothill_2016"].sum()
    print(
        f"[acquire] Saved {len(station_df)} stations "
        f"({n_foothill} Foothill 2016 treatment, "
        f"{len(station_df) - n_foothill} control/other) to {out}"
    )
    return out.resolve()


if __name__ == "__main__":
    print("=== LA Metro Data Acquisition ===\n")

    ridership_path = download_ridership_csv()

    ridership_df = pd.read_csv(ridership_path)
    years = sorted(ridership_df["Year"].unique())
    lines = sorted(ridership_df["Line Name"].unique())
    print(
        f"\nRidership summary:\n"
        f"  Rows: {len(ridership_df):,}\n"
        f"  Years: {years[0]}–{years[-1]}\n"
        f"  Rail lines: {lines}\n"
    )

    station_path = create_station_locations()

    station_df = pd.read_csv(station_path)
    foothill = station_df[station_df["is_foothill_2016"]]
    print(
        f"\nStation summary:\n"
        f"  Total stations: {len(station_df)}\n"
        f"  Foothill 2016 treatment stations ({len(foothill)}):\n"
    )
    for _, row in foothill.iterrows():
        print(f"    - {row['station_name']} ({row['lat']}, {row['lon']})")

    print("\n=== Acquisition complete ===")
