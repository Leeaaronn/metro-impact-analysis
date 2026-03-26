"""
Statistical test functions for LA Metro ridership impact analysis.

All functions return structured results with test name, statistic, p-value,
confidence interval, and effect size as required by REQUIREMENTS.md.
"""

from dataclasses import dataclass
from typing import Optional

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm


@dataclass
class TestResult:
    """Container for a statistical test result."""

    test_name: str
    statistic: float
    p_value: float
    ci_lower: float
    ci_upper: float
    effect_size: float
    effect_size_type: str
    interpretation: str

    def to_dict(self) -> dict:
        return {
            "Test": self.test_name,
            "Statistic": f"{self.statistic:.4f}",
            "p-value": f"{self.p_value:.4f}",
            "95% CI": f"[{self.ci_lower:,.1f}, {self.ci_upper:,.1f}]",
            "Effect Size": f"{self.effect_size:.3f}",
            "Effect Size Type": self.effect_size_type,
            "Interpretation": self.interpretation,
        }


def summary_stats(series: pd.Series, name: str = "") -> dict:
    """Compute descriptive statistics for a numeric series.

    Parameters
    ----------
    series : pd.Series
        Numeric values.
    name : str
        Label for the group.

    Returns
    -------
    dict
        Keys: name, n, mean, median, std, iqr, min, max.
    """
    clean = series.dropna()
    q1, q3 = clean.quantile(0.25), clean.quantile(0.75)
    return {
        "Group": name,
        "N": len(clean),
        "Mean": clean.mean(),
        "Median": clean.median(),
        "Std": clean.std(),
        "IQR": q3 - q1,
        "Min": clean.min(),
        "Max": clean.max(),
    }


def summary_stats_table(
    df: pd.DataFrame,
    group_col: str,
    value_col: str,
) -> pd.DataFrame:
    """Create a summary statistics table grouped by a categorical column.

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    group_col : str
        Column to group by.
    value_col : str
        Numeric column to summarize.

    Returns
    -------
    pd.DataFrame
        One row per group with descriptive stats.
    """
    rows = []
    for group_name, group_data in df.groupby(group_col):
        rows.append(summary_stats(group_data[value_col], name=group_name))
    return pd.DataFrame(rows).set_index("Group")


def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
    """Compute Cohen's d effect size for two independent samples.

    Parameters
    ----------
    group1 : array-like
        First sample.
    group2 : array-like
        Second sample.

    Returns
    -------
    float
        Cohen's d (positive means group1 > group2).
    """
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_std = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    if pooled_std == 0:
        return 0.0
    return (np.mean(group1) - np.mean(group2)) / pooled_std


def _interpret_p(p_value: float, alpha: float = 0.05) -> str:
    if p_value < 0.001:
        return "highly significant (p < 0.001)"
    if p_value < alpha:
        return f"statistically significant (p = {p_value:.4f})"
    return f"not statistically significant (p = {p_value:.4f})"


def _interpret_d(d: float) -> str:
    abs_d = abs(d)
    if abs_d < 0.2:
        return "negligible"
    if abs_d < 0.5:
        return "small"
    if abs_d < 0.8:
        return "medium"
    return "large"


def shapiro_wilk_test(series: pd.Series, name: str = "") -> TestResult:
    """Run Shapiro-Wilk normality test.

    Parameters
    ----------
    series : pd.Series
        Numeric values to test for normality.
    name : str
        Label for reporting.

    Returns
    -------
    TestResult
    """
    clean = series.dropna().values
    stat, p = stats.shapiro(clean)
    is_normal = p >= 0.05
    interpretation = (
        f"{name}: {'consistent with' if is_normal else 'departs from'} "
        f"normality ({_interpret_p(p)})"
    )
    return TestResult(
        test_name=f"Shapiro-Wilk ({name})",
        statistic=stat,
        p_value=p,
        ci_lower=np.nan,
        ci_upper=np.nan,
        effect_size=np.nan,
        effect_size_type="N/A",
        interpretation=interpretation,
    )


def independent_ttest(
    group1: pd.Series,
    group2: pd.Series,
    label1: str = "Group 1",
    label2: str = "Group 2",
) -> TestResult:
    """Two-sample independent t-test with Cohen's d.

    Parameters
    ----------
    group1 : pd.Series
        First sample values.
    group2 : pd.Series
        Second sample values.
    label1 : str
        Name for group 1.
    label2 : str
        Name for group 2.

    Returns
    -------
    TestResult
    """
    a, b = group1.dropna().values, group2.dropna().values
    stat, p = stats.ttest_ind(a, b)
    d = cohens_d(a, b)

    # 95% CI for mean difference
    diff = np.mean(a) - np.mean(b)
    se = np.sqrt(np.var(a, ddof=1) / len(a) + np.var(b, ddof=1) / len(b))
    t_crit = stats.t.ppf(0.975, df=len(a) + len(b) - 2)
    ci_lower = diff - t_crit * se
    ci_upper = diff + t_crit * se

    interpretation = (
        f"{label1} vs {label2}: {_interpret_p(p)}; "
        f"mean diff = {diff:,.1f}; Cohen's d = {d:.3f} ({_interpret_d(d)} effect)"
    )
    return TestResult(
        test_name=f"Independent t-test ({label1} vs {label2})",
        statistic=stat,
        p_value=p,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        effect_size=d,
        effect_size_type="Cohen's d",
        interpretation=interpretation,
    )


def mann_whitney_u(
    group1: pd.Series,
    group2: pd.Series,
    label1: str = "Group 1",
    label2: str = "Group 2",
) -> TestResult:
    """Mann-Whitney U test (non-parametric alternative to independent t-test).

    Parameters
    ----------
    group1 : pd.Series
        First sample values.
    group2 : pd.Series
        Second sample values.
    label1 : str
        Name for group 1.
    label2 : str
        Name for group 2.

    Returns
    -------
    TestResult
    """
    a, b = group1.dropna().values, group2.dropna().values
    stat, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    d = cohens_d(a, b)

    # Hodges-Lehmann estimate for CI (median of pairwise differences)
    diffs = np.subtract.outer(a, b).ravel()
    ci_lower, ci_upper = np.percentile(diffs, [2.5, 97.5])

    interpretation = (
        f"{label1} vs {label2}: {_interpret_p(p)}; "
        f"Cohen's d = {d:.3f} ({_interpret_d(d)} effect)"
    )
    return TestResult(
        test_name=f"Mann-Whitney U ({label1} vs {label2})",
        statistic=stat,
        p_value=p,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        effect_size=d,
        effect_size_type="Cohen's d",
        interpretation=interpretation,
    )


def paired_ttest(
    before: pd.Series,
    after: pd.Series,
    label: str = "Pre vs Post",
) -> TestResult:
    """Paired t-test for pre/post comparison within the same group.

    Parameters
    ----------
    before : pd.Series
        Pre-period values.
    after : pd.Series
        Post-period values.
    label : str
        Label for the comparison.

    Returns
    -------
    TestResult
    """
    a, b = before.dropna().values, after.dropna().values
    # Use the shorter series length for pairing
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]

    stat, p = stats.ttest_rel(a, b)
    diff = b - a
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    d = mean_diff / std_diff if std_diff > 0 else 0.0

    se = std_diff / np.sqrt(n)
    t_crit = stats.t.ppf(0.975, df=n - 1)
    ci_lower = mean_diff - t_crit * se
    ci_upper = mean_diff + t_crit * se

    interpretation = (
        f"{label}: {_interpret_p(p)}; "
        f"mean change = {mean_diff:,.1f}; Cohen's d = {d:.3f} ({_interpret_d(d)} effect)"
    )
    return TestResult(
        test_name=f"Paired t-test ({label})",
        statistic=stat,
        p_value=p,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        effect_size=d,
        effect_size_type="Cohen's d (paired)",
        interpretation=interpretation,
    )


def wilcoxon_signed_rank(
    before: pd.Series,
    after: pd.Series,
    label: str = "Pre vs Post",
) -> TestResult:
    """Wilcoxon signed-rank test (non-parametric paired pre/post comparison).

    Parameters
    ----------
    before : pd.Series
        Pre-period values.
    after : pd.Series
        Post-period values.
    label : str
        Label for the comparison.

    Returns
    -------
    TestResult
    """
    a, b = before.dropna().values, after.dropna().values
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]

    stat, p = stats.wilcoxon(b - a, alternative="two-sided")
    diff = b - a
    mean_diff = np.mean(diff)
    std_diff = np.std(diff, ddof=1)
    d = mean_diff / std_diff if std_diff > 0 else 0.0

    # CI from percentiles of pairwise differences
    ci_lower, ci_upper = np.percentile(diff, [2.5, 97.5])

    interpretation = (
        f"{label}: {_interpret_p(p)}; "
        f"median change = {np.median(diff):,.1f}; "
        f"Cohen's d = {d:.3f} ({_interpret_d(d)} effect)"
    )
    return TestResult(
        test_name=f"Wilcoxon signed-rank ({label})",
        statistic=stat,
        p_value=p,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        effect_size=d,
        effect_size_type="Cohen's d (paired)",
        interpretation=interpretation,
    )


@dataclass
class DiDResult:
    """Container for difference-in-differences regression results."""

    did_coefficient: float
    did_se: float
    did_p_value: float
    did_ci_lower: float
    did_ci_upper: float
    treatment_coefficient: float
    post_coefficient: float
    intercept: float
    r_squared: float
    r_squared_adj: float
    n_obs: int
    summary_text: str
    interpretation: str

    def to_dict(self) -> dict:
        return {
            "DiD Coefficient (Treatment x Post)": f"{self.did_coefficient:,.1f}",
            "Std. Error": f"{self.did_se:,.1f}",
            "p-value": f"{self.did_p_value:.4f}",
            "95% CI": f"[{self.did_ci_lower:,.1f}, {self.did_ci_upper:,.1f}]",
            "Treatment Effect": f"{self.treatment_coefficient:,.1f}",
            "Post Effect": f"{self.post_coefficient:,.1f}",
            "R-squared": f"{self.r_squared:.4f}",
            "R-squared (adj)": f"{self.r_squared_adj:.4f}",
            "N": self.n_obs,
            "Interpretation": self.interpretation,
        }


def did_regression(
    df: pd.DataFrame,
    outcome_col: str = "avg_daily_boardings",
    treatment_col: str = "is_treatment",
    post_col: str = "is_post",
    label: str = "DiD",
) -> DiDResult:
    """Run OLS difference-in-differences regression.

    Model: Y = b0 + b1*Treatment + b2*Post + b3*(Treatment x Post) + e

    The coefficient b3 is the DiD estimator — the causal effect of the
    treatment on the outcome, net of group and time fixed effects.

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with outcome, treatment indicator, and post indicator.
    outcome_col : str
        Column name for the dependent variable.
    treatment_col : str
        Column name for the treatment group dummy (1 = treatment).
    post_col : str
        Column name for the post-period dummy (1 = post).
    label : str
        Label for reporting.

    Returns
    -------
    DiDResult
    """
    reg_df = df[[outcome_col, treatment_col, post_col]].dropna().copy()
    reg_df[treatment_col] = reg_df[treatment_col].astype(int)
    reg_df[post_col] = reg_df[post_col].astype(int)
    reg_df["interaction"] = reg_df[treatment_col] * reg_df[post_col]

    X = sm.add_constant(reg_df[[treatment_col, post_col, "interaction"]])
    y = reg_df[outcome_col]
    model = sm.OLS(y, X).fit(cov_type="HC1")

    did_coef = model.params["interaction"]
    did_se = model.bse["interaction"]
    did_p = model.pvalues["interaction"]
    ci = model.conf_int().loc["interaction"]

    sig = _interpret_p(did_p)
    direction = "increased" if did_coef > 0 else "decreased"

    interpretation = (
        f"{label}: The extension {direction} Gold Line ridership by "
        f"{abs(did_coef):,.0f} avg daily boardings ({sig}). "
        f"95% CI: [{ci[0]:,.0f}, {ci[1]:,.0f}]."
    )

    return DiDResult(
        did_coefficient=did_coef,
        did_se=did_se,
        did_p_value=did_p,
        did_ci_lower=ci[0],
        did_ci_upper=ci[1],
        treatment_coefficient=model.params[treatment_col],
        post_coefficient=model.params[post_col],
        intercept=model.params["const"],
        r_squared=model.rsquared,
        r_squared_adj=model.rsquared_adj,
        n_obs=int(model.nobs),
        summary_text=model.summary().as_text(),
        interpretation=interpretation,
    )
