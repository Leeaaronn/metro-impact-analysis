# Roadmap

## Phase 1: Data Acquisition & Cleaning

- [ ] Task 1: Download Metro ridership data (CSV from Streets For All or Metro dashboard)
- [ ] Task 2: Download Metro station location data (GIS shapefiles or CSV)
- [ ] Task 4: Clean and standardize all datasets (types, nulls, date parsing, column naming)
- [ ] Task 5: Write data validation tests (Pytest: row counts > 0, no null keys, expected schemas)

**Definition of Done**: All raw data in `data/raw/`, cleaned data in `data/clean/`, pytest passes, `data_inventory.md` documents every file with row counts and date ranges.

## Phase 2: Exploratory Data Analysis

- [ ] Task 1: Ridership trends — plot monthly ridership for Gold Line vs other lines (2012–2025), annotate March 2016 extension date
- [ ] Task 2: Summary statistics table — pre vs post extension period for treatment and control groups
- [ ] Task 3: Distribution analysis — histograms, boxplots, normality checks (Shapiro-Wilk) for key variables
- [ ] Task 4: Correlation matrix — ridership and demographics (if using ACS)

**Definition of Done**: EDA notebook section complete with 5+ publication-quality figures, all with titles/labels/legends. Markdown cells explain every finding in plain English.

## Phase 3: Statistical Testing & Causal Analysis

- [ ] Task 1: Pre/post comparison — paired t-test or Wilcoxon signed-rank test on ridership before vs after extension
- [ ] Task 2: Treatment vs control — independent samples t-test or Mann-Whitney U comparing Gold Line growth to other lines
- [ ] Task 3: Difference-in-differences (DiD) — OLS regression with interaction term (treatment × post), report coefficient, SE, p-value, CI
- [ ] Task 4: Effect size — compute Cohen's d for each comparison
- [ ] Task 5: Robustness checks — vary treatment window (±6 months), exclude COVID period (2020–2021), test parallel trends assumption
**Definition of Done**: Every test has a function in `src/stats.py`, every result includes test name + statistic + p-value + 95% CI + effect size + plain English interpretation. Notebook section reads like a findings report.

## Phase 4: Narrative & Polish

- [ ] Task 1: Write executive summary (top of notebook, 5–6 sentences, no code)
- [ ] Task 2: Write methodology section (markdown cells explaining DiD, assumptions, data sources)
- [ ] Task 3: Write findings section (structured around the research questions)
- [ ] Task 4: Write limitations section (data gaps, confounders, generalizability)
- [ ] Task 5: Write conclusion (2–3 sentences answering the central question)
- [ ] Task 6: Format all figures for consistency (Seaborn theme, color palette, font sizes)
- [ ] Task 7: Create README.md with project overview, key findings, and setup instructions

**Definition of Done**: Notebook tells a complete story from question → data → analysis → findings → limitations → conclusion. A hiring manager can read it in 10 minutes and understand the analytical approach.
