# LA Metro Ridership Impact Analysis

## Goal

Quantify the causal impact of the LA Metro Gold Line Foothill Extension (Phase 2A, opened March 2016) on ridership patterns and surrounding economic activity in the San Gabriel Valley, using a difference-in-differences framework and supporting statistical tests. The primary deliverable is a polished Jupyter notebook that demonstrates statistical reasoning, causal thinking, and clear communication to Data Analyst and Data Scientist hiring managers.

## Success Metrics

1. **Reproducible**: Notebook runs top-to-bottom with no errors and reproduces all figures and test results via `make notebook`.
2. **Statistically rigorous**: Every statistical claim includes a test name, test statistic, p-value, 95% confidence interval, and effect size.
3. **Readable**: A non-technical reader can follow the narrative without reading any code cells.

## Non-Goals

- No web application, dashboard, or API
- No real-time or streaming data
- No predictive modeling or forecasting (this is causal inference, not prediction)
- No geographic scope beyond the LA Metro rail system
- No pipeline engineering — this is a single-notebook analysis project
