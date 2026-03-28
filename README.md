# Impact of the Gold Line Foothill Extension on LA Metro Ridership

Did the March 2016 opening of the Gold Line Foothill Extension (Phase 2A) cause a
statistically significant change in LA Metro ridership? This project answers that
question using a difference-in-differences (DiD) quasi-experimental design, comparing
Gold Line ridership (treatment) against four other Metro rail lines (control) over
January 2012 to December 2019. The analysis spans data acquisition, cleaning,
exploratory analysis, statistical testing, and robustness checks — all in a single
reproducible Jupyter notebook.

## Key Finding

The Foothill Extension increased Gold Line average weekday boardings by approximately
**38,745 riders per day** relative to control lines (p < 0.001, 95% CI: [29,364, 48,126]),
a large and statistically significant effect that is robust to alternative specifications.

## Setup

```bash
pip install -r requirements.txt
make all
```

## Project Structure

```
data/
  raw/             # Downloaded source files (never modified)
  clean/           # Cleaned and standardized files
src/
  acquire.py       # Data download functions
  clean.py         # Cleaning and standardization
  stats.py         # Statistical tests (t-tests, DiD, effect sizes)
  viz.py           # Visualization helpers (seaborn + matplotlib)
tests/
  test_data.py     # Data validation tests
  test_stats.py    # Statistical function unit tests
notebooks/
  analysis.ipynb   # The deliverable — single polished notebook
Makefile           # setup, test, notebook, all, clean
requirements.txt
```

## Tech Stack

Python, Pandas, SciPy, Statsmodels, Seaborn, Matplotlib, Pytest, Jupyter

## Contact

**Aaron Lee** — [github.com/Leeaaronn](https://github.com/Leeaaronn) — alee190@csu.fullerton.edu
