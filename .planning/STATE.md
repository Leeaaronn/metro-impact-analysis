# State

## What's Done

- Project scaffold created: PROJECT.md, ROADMAP.md, REQUIREMENTS.md, CLAUDE.md, STATE.md
- Plan 01-01: Acquired raw ridership data (1,323 rows, 2009–2025) and station locations (26 stations)
- Plan 01-02: Cleaned datasets produced — 944 rail ridership rows, 26 stations (6 Foothill treatment)
- Plan 02-01: EDA notebook complete — 6 publication-quality figures (trends, treatment/control, distributions, boxplots, normality tests, correlation heatmap). Shapiro-Wilk results ready for Phase 3 test selection.

## What's Next

- Phase 3: Statistical Testing (DiD analysis)

## Blockers

(none)

## Decisions Log

- **D-01 (Phase 1)**: Business proximity analysis dropped for SGV stations. Research confirmed that Arcadia, Monrovia, Duarte, Irwindale, and Azusa do not publish business license data to any open data portal. LA City data covers only City of LA boundaries. Per CLAUDE.md stop condition: "LA City business data missing geocoding → drop business proximity analysis from scope." Alternative: Census ACS/LEHD data may be used in Phase 3 as economic proxy if needed.
- **D-02 (Phase 1)**: Primary ridership source is Streets For All (line-level monthly). Station-level data unavailable via automated download; analysis will use line-level data per CLAUDE.md stop condition fallback. Gold Line vs other lines is the treatment/control design.
- **D-03 (Phase 1)**: Regional Connector (June 2023) creates a data discontinuity. Primary analysis window ends Dec 2019 (pre-COVID). Secondary robustness check may extend to 2025 but must account for June 2023 line restructuring where Gold Line (L Line) was absorbed into A Line.
- **D-04 (Phase 1)**: BRT lines (G Line/Orange, J Line/Silver) excluded from rail analysis. Raw data tagged them as "Train" but they are bus rapid transit. 944 rail-only rows retained from 1,323 total.
- **D-05 (Phase 1)**: System-wide data gap identified for April–June 2018 across all lines. Likely a Metro reporting gap, not a data error. Will be handled as missing data in analysis.
