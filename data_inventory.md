# Data Inventory

Last updated: 2026-03-25

## Raw Data (`data/raw/`)

### ridership_monthly.csv
- **Source**: Streets For All ridership dashboard (ridership.streetsforall.org), extracted from JS bundle
- **Acquired**: 2026-03-24
- **Rows**: 1,323
- **Columns**: Year, Month, Line Name, Former Name, Line Category, Avg. Daily Boardings (Weekday), Avg. Daily Boardings (Saturday), Avg. Daily Boardings (Sunday), line_name
- **Date range**: 2009 to 2025
- **Lines**: A Line, B Line, C Line, E Line, G Line, J Line, K Line, L Line (includes BRT)
- **Description**: Monthly average daily boardings by Metro rail and BRT line, segmented by day type (weekday/saturday/sunday)

### station_locations.csv
- **Source**: Manually compiled from Metro GIS data, Wikipedia, and Google Maps verification
- **Created**: 2026-03-24
- **Rows**: 26
- **Columns**: station_name, line, lat, lon, opened_date, is_foothill_2016
- **Description**: Metro rail stations with coordinates and Foothill Extension Phase 2A flags. 6 treatment stations (opened 2016-03-05), 20 control/context stations from A, B, C, D lines.

## Cleaned Data (`data/clean/`)

### ridership_clean.csv
- **Source**: Cleaned from data/raw/ridership_monthly.csv via `src/clean.py`
- **Rows**: 944
- **Columns**: date, year, month, line_name, former_name, line_id, avg_daily_boardings, avg_daily_boardings_sat, avg_daily_boardings_sun, is_treatment, period
- **Date range**: 2009-01-01 to 2025-06-01
- **Lines**: a_line, a_line_merged, expo, gold, green, k_line, red (7 line IDs)
- **Cleaning steps**: Filtered out BRT lines (G Line, J Line), standardized line names to line_id with date-aware Gold/L/A Line mapping, added is_treatment flag, added period labels (pre/post/transition relative to March 2016 extension)
- **Known gaps**: April–June 2018 missing across all lines (Metro reporting gap)

### station_locations_clean.csv
- **Source**: Cleaned from data/raw/station_locations.csv via `src/clean.py`
- **Rows**: 26
- **Columns**: station_name, line, lat, lon, opened_date, is_foothill_2016
- **Cleaning steps**: Parsed opened_date as datetime, validated coordinates within LA County range (33–35 lat, -119 to -117 lon)

## Scope Exclusions

### LA City Business Listings (NOT USED)
- **Reason**: SGV cities (Arcadia, Monrovia, Duarte, Irwindale, Azusa) do not publish business license data to open data portals. LA City data only covers City of LA boundaries, which excludes all treatment station areas.
- **Decision**: D-01 in STATE.md
- **Alternative considered**: Census ACS/LEHD data for economic proxy in Phase 3
