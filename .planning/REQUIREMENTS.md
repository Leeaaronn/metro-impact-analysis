# Requirements

## Non-Negotiables

- Every statistical test must report: test name, test statistic, p-value, 95% confidence interval, and effect size (Cohen's d or equivalent)
- All figures must have titles, axis labels, legends, and source annotations
- Notebook must run top-to-bottom without errors (no hidden state dependencies)
- Markdown cells must outnumber code cells or be roughly equal — this is a communication piece
- No p-hacking: state hypotheses BEFORE running tests, report all results including non-significant ones

## Treatment Design

- **Treatment event**: Gold Line Foothill Extension Phase 2A opening (March 5, 2016)
- **Treatment group**: Gold Line / A Line (the line serving the new SGV stations)
- **Control group**: Other Metro rail lines (B/D, C, E) that did NOT receive new stations in the same period
- **Pre-period**: January 2012 – February 2016 (minimum 24 months pre)
- **Post-period**: April 2016 – December 2019 (exclude COVID for primary analysis)
- **COVID sensitivity**: Run secondary analysis including 2020–2025 as a robustness check

## Data Sources

### A) LA Metro Ridership Data
- **Source**: Streets For All ridership dashboard (ridership.streetsforall.org) — CSV download of monthly ridership by line
- **Alternative**: Metro official dashboard (opa.metro.net/MetroRidership/)
- **Granularity**: Monthly average weekday boardings by line (station-level if available)
- **Time range**: 2012–2025
- **Expected schema**: `date (month)`, `line`, `avg_weekday_boardings`

### B) ACS / Census Data (optional)
- **Source**: Census API — population, income, demographics by tract
- **Use**: Control variables in regression models

### C) Metro Station Locations
- **Source**: Metro GIS data (developer.metro.net/gis-data/)
- **Use**: Geocoding, distance calculations for treatment/control assignment
- **Expected schema**: `station_name`, `line`, `lat`, `lon`, `opened_date`

## Statistical Methods Required

- Descriptive statistics (mean, median, std, IQR)
- Visual EDA (time series, distributions, scatter, heatmap)
- Paired t-test or Wilcoxon signed-rank test (pre/post within group)
- Independent samples t-test or Mann-Whitney U (between groups)
- OLS regression with DiD specification: `Y = β0 + β1(Treatment) + β2(Post) + β3(Treatment × Post) + ε`
- Cohen's d effect size for all comparisons
- Shapiro-Wilk normality test to justify parametric vs non-parametric choice

## Data Quality Requirements

- No null values in join keys (date, line/station identifiers)
- Date ranges must be continuous (flag and document any gaps)
- All cleaning steps logged in the notebook with before/after row counts

## Reproducibility Requirements

- `make setup` — create virtual environment, install dependencies
- `make test` — run pytest on data validation and statistical function tests
- `make notebook` — execute notebook top-to-bottom via nbconvert or papermill
- `make all` — setup + test + notebook
- `requirements.txt` pinned to exact versions
