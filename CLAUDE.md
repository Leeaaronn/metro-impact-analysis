# CLAUDE.md

## Coding Standards

- **Formatter**: Black (line length 88), isort (Black-compatible profile)
- **Type hints**: Required on all public functions in `src/`
- **Notebook cells**: One logical operation per cell. Markdown cell before every code cell explaining what and why.
- **Figures**: Use `sns.set_theme(style="whitegrid", palette="muted")` as default. Override only when a specific visualization requires it.
- **Variable naming**: `snake_case` everywhere, descriptive names (`ridership_monthly`, `business_near_stations` — not `df1`, `df2`)

## Directory Layout

```
data/
  raw/           # Downloaded source files (never modified)
  clean/         # Cleaned/standardized files
src/
  acquire.py     # Download functions
  clean.py       # Cleaning/standardization functions
  stats.py       # All statistical test functions (reusable, tested)
  viz.py         # Visualization helper functions
tests/
  test_data.py   # Data validation tests
  test_stats.py  # Statistical function unit tests
notebooks/
  analysis.ipynb # THE deliverable — the single polished notebook
Makefile
requirements.txt
README.md
```

## Allowed Libraries

| Library | Permitted use |
|---------|--------------|
| pandas | All DataFrame operations |
| numpy | Numerical computation |
| scipy | Statistical tests (scipy.stats) |
| statsmodels | OLS regression, DiD specification |
| seaborn | All visualization |
| matplotlib | Figure customization underlying seaborn |
| jupyter | Notebook environment |
| pytest | All testing |
| requests or httpx | Data downloads in src/acquire.py |
| geopandas | ONLY if geocoding/distance calculations needed |
| nbconvert or papermill | Notebook execution for reproducibility |

**AVOID**: scikit-learn, prophet, duckdb, streamlit, dash, plotly, heavy frameworks. This is a statistics project, not ML or pipeline.

## Commands That Must Pass Before Commit

- `make test` (pytest — zero failures)
- `make notebook` (notebook executes top-to-bottom with no errors)

## Stop Conditions

Halt and write to STATE.md under Blockers if any of these occur:

- Station-level ridership data unavailable → pivot to line-level analysis and document
- LA City business data missing geocoding → drop business proximity analysis from scope
- Any data source returns 404 or requires paid API → find alternative or reduce scope
- Statistical test assumption violated (e.g., non-normality) → use non-parametric alternative and document

## Small Patch Rule

If a change touches >3 files, propose splitting into smaller focused commits.
