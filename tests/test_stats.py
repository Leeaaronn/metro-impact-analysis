"""Unit tests for statistical functions in src/stats.py."""

import numpy as np
import pandas as pd
import pytest

from src.stats import (
    DiDResult,
    TestResult,
    cohens_d,
    did_regression,
    independent_ttest,
    mann_whitney_u,
    paired_ttest,
    shapiro_wilk_test,
    summary_stats,
    summary_stats_table,
    wilcoxon_signed_rank,
)


class TestSummaryStats:
    def test_known_values(self):
        s = pd.Series([10, 20, 30, 40, 50])
        result = summary_stats(s, name="test")
        assert result["Group"] == "test"
        assert result["N"] == 5
        assert result["Mean"] == 30.0
        assert result["Median"] == 30.0
        assert result["Min"] == 10.0
        assert result["Max"] == 50.0

    def test_std_correct(self):
        s = pd.Series([10, 20, 30, 40, 50])
        result = summary_stats(s)
        expected_std = s.std()  # pandas default ddof=1
        assert abs(result["Std"] - expected_std) < 0.001

    def test_iqr_correct(self):
        s = pd.Series([10, 20, 30, 40, 50])
        result = summary_stats(s)
        expected_iqr = s.quantile(0.75) - s.quantile(0.25)
        assert abs(result["IQR"] - expected_iqr) < 0.001

    def test_single_value(self):
        s = pd.Series([42])
        result = summary_stats(s)
        assert result["N"] == 1
        assert result["Mean"] == 42.0
        assert result["Median"] == 42.0


class TestSummaryStatsTable:
    def test_two_groups(self):
        df = pd.DataFrame({
            "group": ["A", "A", "A", "B", "B", "B"],
            "value": [10, 20, 30, 100, 200, 300],
        })
        result = summary_stats_table(df, "group", "value")
        assert len(result) == 2
        assert result.loc["A", "Mean"] == 20.0
        assert result.loc["B", "Mean"] == 200.0

    def test_returns_dataframe(self):
        df = pd.DataFrame({
            "group": ["X", "X", "Y", "Y"],
            "value": [1, 2, 3, 4],
        })
        result = summary_stats_table(df, "group", "value")
        assert isinstance(result, pd.DataFrame)
        assert result.index.name == "Group"


class TestCohensD:
    def test_identical_groups_zero_effect(self):
        a = np.array([10, 20, 30, 40, 50])
        d = cohens_d(a, a)
        assert d == 0.0

    def test_large_effect(self):
        a = np.array([100, 110, 120, 130, 140])
        b = np.array([10, 20, 30, 40, 50])
        d = cohens_d(a, b)
        assert d > 0.8

    def test_positive_when_group1_larger(self):
        a = np.array([50, 60, 70, 80, 90])
        b = np.array([10, 20, 30, 40, 50])
        d = cohens_d(a, b)
        assert d > 0

    def test_negative_when_group1_smaller(self):
        a = np.array([10, 20, 30, 40, 50])
        b = np.array([50, 60, 70, 80, 90])
        d = cohens_d(a, b)
        assert d < 0


class TestShapiroWilk:
    def test_normal_data_passes(self):
        np.random.seed(42)
        s = pd.Series(np.random.normal(100, 15, 50))
        result = shapiro_wilk_test(s, name="normal")
        assert isinstance(result, TestResult)
        assert result.p_value >= 0.05
        assert "consistent with" in result.interpretation

    def test_skewed_data_fails(self):
        s = pd.Series([1, 1, 1, 1, 1, 1, 1, 1, 1, 100])
        result = shapiro_wilk_test(s, name="skewed")
        assert result.p_value < 0.05
        assert "departs from" in result.interpretation

    def test_returns_test_result(self):
        s = pd.Series([10, 20, 30, 40, 50])
        result = shapiro_wilk_test(s, name="check")
        assert isinstance(result, TestResult)
        assert "Shapiro-Wilk" in result.test_name
        assert not np.isnan(result.statistic)
        assert not np.isnan(result.p_value)


class TestIndependentTtest:
    def test_identical_groups_not_significant(self):
        a = pd.Series([10, 20, 30, 40, 50])
        result = independent_ttest(a, a, "G1", "G2")
        assert result.p_value > 0.05
        assert abs(result.effect_size) < 0.01

    def test_different_groups_significant(self):
        a = pd.Series([100, 110, 120, 130, 140])
        b = pd.Series([10, 20, 30, 40, 50])
        result = independent_ttest(a, b, "high", "low")
        assert result.p_value < 0.05
        assert abs(result.effect_size) > 0.8

    def test_ci_order(self):
        a = pd.Series([50, 60, 70, 80, 90])
        b = pd.Series([10, 20, 30, 40, 50])
        result = independent_ttest(a, b, "A", "B")
        assert result.ci_lower < result.ci_upper

    def test_returns_test_result(self):
        a = pd.Series([1, 2, 3])
        b = pd.Series([4, 5, 6])
        result = independent_ttest(a, b, "A", "B")
        assert isinstance(result, TestResult)
        assert "Independent t-test" in result.test_name


class TestMannWhitneyU:
    def test_identical_groups_not_significant(self):
        a = pd.Series([10, 20, 30, 40, 50])
        result = mann_whitney_u(a, a, "G1", "G2")
        assert result.p_value > 0.05

    def test_non_overlapping_groups_significant(self):
        a = pd.Series([100, 110, 120, 130, 140])
        b = pd.Series([10, 20, 30, 40, 50])
        result = mann_whitney_u(a, b, "high", "low")
        assert result.p_value < 0.05

    def test_returns_test_result(self):
        a = pd.Series([1, 2, 3, 4, 5])
        b = pd.Series([6, 7, 8, 9, 10])
        result = mann_whitney_u(a, b, "A", "B")
        assert isinstance(result, TestResult)
        assert "Mann-Whitney" in result.test_name


class TestPairedTtest:
    def test_constant_shift_significant(self):
        before = pd.Series([10, 20, 30, 40, 50])
        after = pd.Series([110, 120, 130, 140, 150])
        result = paired_ttest(before, after, label="shift")
        assert result.p_value < 0.05
        assert result.ci_lower > 0

    def test_no_change_not_significant(self):
        np.random.seed(42)
        before = pd.Series([100, 200, 300, 400, 500])
        after = before + np.random.normal(0, 0.01, 5)
        result = paired_ttest(before, after, label="no change")
        assert result.p_value > 0.05

    def test_ci_contains_true_difference(self):
        before = pd.Series([10, 20, 30, 40, 50])
        after = pd.Series([60, 70, 80, 90, 100])
        result = paired_ttest(before, after, label="50 shift")
        assert result.ci_lower <= 50 <= result.ci_upper

    def test_returns_test_result(self):
        before = pd.Series([1, 2, 3, 4, 5])
        after = pd.Series([2, 3, 4, 5, 6])
        result = paired_ttest(before, after, label="test")
        assert isinstance(result, TestResult)
        assert "Paired t-test" in result.test_name


class TestWilcoxonSignedRank:
    def test_consistent_increase_significant(self):
        before = pd.Series([10, 20, 30, 40, 50, 60, 70, 80])
        after = pd.Series([110, 120, 130, 140, 150, 160, 170, 180])
        result = wilcoxon_signed_rank(before, after, label="increase")
        assert result.p_value < 0.05

    def test_returns_test_result(self):
        before = pd.Series([10, 20, 30, 40, 50])
        after = pd.Series([15, 25, 35, 45, 55])
        result = wilcoxon_signed_rank(before, after, label="test")
        assert isinstance(result, TestResult)
        assert "Wilcoxon" in result.test_name


class TestDidRegression:
    @pytest.fixture
    def synthetic_panel(self):
        """Create a synthetic panel: 2 groups x 2 periods x 10 obs each.

        Treatment group post-period gets +100 added to outcome.
        """
        np.random.seed(42)
        n = 10
        rows = []
        for treatment in [0, 1]:
            for post in [0, 1]:
                for _ in range(n):
                    base = 50 + np.random.normal(0, 5)
                    effect = 100 if (treatment == 1 and post == 1) else 0
                    rows.append({
                        "outcome": base + effect,
                        "is_treatment": treatment,
                        "is_post": post,
                    })
        return pd.DataFrame(rows)

    def test_did_coefficient_approx_100(self, synthetic_panel):
        result = did_regression(
            synthetic_panel,
            outcome_col="outcome",
            treatment_col="is_treatment",
            post_col="is_post",
            label="synthetic",
        )
        assert abs(result.did_coefficient - 100) < 15

    def test_did_significant(self, synthetic_panel):
        result = did_regression(
            synthetic_panel,
            outcome_col="outcome",
            treatment_col="is_treatment",
            post_col="is_post",
            label="synthetic",
        )
        assert result.did_p_value < 0.05

    def test_ci_contains_coefficient(self, synthetic_panel):
        result = did_regression(
            synthetic_panel,
            outcome_col="outcome",
            treatment_col="is_treatment",
            post_col="is_post",
            label="synthetic",
        )
        assert result.did_ci_lower < result.did_coefficient < result.did_ci_upper

    def test_returns_did_result(self, synthetic_panel):
        result = did_regression(
            synthetic_panel,
            outcome_col="outcome",
            treatment_col="is_treatment",
            post_col="is_post",
            label="synthetic",
        )
        assert isinstance(result, DiDResult)
        assert result.n_obs == 40
        assert result.r_squared >= 0
        assert len(result.summary_text) > 0
        assert len(result.interpretation) > 0