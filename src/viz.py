"""
Visualization helper functions for LA Metro ridership impact analysis.

All plots use seaborn with a consistent theme. Functions return matplotlib
Figure objects so callers can further customize or save them.
"""

from typing import Optional

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import seaborn as sns


def set_default_theme() -> None:
    """Apply the project-standard seaborn theme."""
    sns.set_theme(style="whitegrid", palette="muted")
    plt.rcParams.update({
        "figure.dpi": 120,
        "figure.figsize": (12, 6),
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
    })


# Line display config: line_id -> (label, color)
LINE_STYLES: dict[str, tuple[str, str]] = {
    "gold": ("Gold Line", "#D4AF37"),
    "a_line": ("A Line (Blue)", "#0072CE"),
    "a_line_merged": ("A Line (merged)", "#6A0DAD"),
    "red": ("B Line (Red)", "#E4002B"),
    "green": ("C Line (Green)", "#00A94F"),
    "purple": ("D Line (Purple)", "#A05EB5"),
    "expo": ("E Line (Expo)", "#FDB813"),
    "k_line": ("K Line", "#E56DB1"),
}


def plot_ridership_trends(
    df: pd.DataFrame,
    line_ids: Optional[list[str]] = None,
    metric: str = "avg_daily_boardings",
    title: str = "Monthly Average Weekday Boardings by Line",
    annotate_extension: bool = True,
    end_date: Optional[str] = None,
) -> plt.Figure:
    """Plot monthly ridership time series for selected lines.

    Parameters
    ----------
    df : pd.DataFrame
        Clean ridership data with 'date', 'line_id', and metric columns.
    line_ids : list[str], optional
        Lines to plot. Defaults to all except a_line_merged and k_line.
    metric : str
        Column name for the y-axis value.
    title : str
        Plot title.
    annotate_extension : bool
        Whether to draw a vertical line at March 2016.
    end_date : str, optional
        Truncate data at this date (e.g., "2019-12-31").

    Returns
    -------
    plt.Figure
    """
    set_default_theme()
    fig, ax = plt.subplots(figsize=(14, 7))

    plot_df = df.copy()
    plot_df["date"] = pd.to_datetime(plot_df["date"])

    if end_date:
        plot_df = plot_df[plot_df["date"] <= end_date]

    if line_ids is None:
        line_ids = ["gold", "a_line", "red", "green", "expo"]

    for lid in line_ids:
        line_data = plot_df[plot_df["line_id"] == lid].sort_values("date")
        if line_data.empty:
            continue
        label, color = LINE_STYLES.get(lid, (lid, None))
        lw = 2.5 if lid == "gold" else 1.5
        ax.plot(
            line_data["date"],
            line_data[metric],
            label=label,
            color=color,
            linewidth=lw,
            alpha=0.9 if lid == "gold" else 0.7,
        )

    if annotate_extension:
        ax.axvline(
            pd.Timestamp("2016-03-05"),
            color="black",
            linestyle="--",
            linewidth=1,
            alpha=0.7,
        )
        ax.text(
            pd.Timestamp("2016-05-01"),
            ax.get_ylim()[1] * 0.95,
            "Foothill Extension\nOpens Mar 2016",
            fontsize=9,
            va="top",
            ha="left",
            style="italic",
        )

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Avg. Daily Weekday Boardings")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(loc="upper left", framealpha=0.9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    fig.tight_layout()
    return fig


def plot_treatment_vs_control(
    df: pd.DataFrame,
    metric: str = "avg_daily_boardings",
    end_date: str = "2019-12-31",
    title: str = "Treatment (Gold Line) vs Control Lines - Avg. Weekday Boardings",
) -> plt.Figure:
    """Plot aggregated treatment vs control group ridership over time.

    Parameters
    ----------
    df : pd.DataFrame
        Clean ridership data.
    metric : str
        Column for the y-axis.
    end_date : str
        Truncate at this date.
    title : str
        Plot title.

    Returns
    -------
    plt.Figure
    """
    set_default_theme()
    fig, ax = plt.subplots(figsize=(14, 6))

    plot_df = df.copy()
    plot_df["date"] = pd.to_datetime(plot_df["date"])
    plot_df = plot_df[plot_df["date"] <= end_date]

    # Treatment = gold line only (pre-merger)
    treatment = (
        plot_df[plot_df["line_id"] == "gold"]
        .groupby("date")[metric]
        .mean()
        .reset_index()
    )
    # Control = non-treatment rail lines (exclude k_line: too short, a_line_merged)
    control_ids = ["a_line", "red", "green", "expo"]
    control = (
        plot_df[plot_df["line_id"].isin(control_ids)]
        .groupby("date")[metric]
        .mean()
        .reset_index()
    )

    ax.plot(
        treatment["date"],
        treatment[metric],
        label="Treatment (Gold Line)",
        color="#D4AF37",
        linewidth=2.5,
    )
    ax.plot(
        control["date"],
        control[metric],
        label="Control (avg of A, B, C, E)",
        color="#555555",
        linewidth=2,
        linestyle="-",
    )

    ax.axvline(
        pd.Timestamp("2016-03-05"),
        color="black",
        linestyle="--",
        linewidth=1,
        alpha=0.7,
    )
    ax.text(
        pd.Timestamp("2016-05-01"),
        ax.get_ylim()[1] * 0.95,
        "Extension Opens",
        fontsize=9,
        va="top",
        style="italic",
    )

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Avg. Daily Weekday Boardings")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(framealpha=0.9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{x:,.0f}"))

    fig.tight_layout()
    return fig


def plot_distributions(
    df: pd.DataFrame,
    groups: dict[str, pd.Series],
    metric_label: str = "Avg. Daily Weekday Boardings",
    title: str = "Distribution of Ridership",
) -> plt.Figure:
    """Plot histograms with KDE for multiple groups side by side.

    Parameters
    ----------
    df : pd.DataFrame
        Not used directly; kept for API consistency.
    groups : dict[str, pd.Series]
        Mapping of group label -> Series of values to plot.
    metric_label : str
        X-axis label.
    title : str
        Plot title.

    Returns
    -------
    plt.Figure
    """
    set_default_theme()
    n_groups = len(groups)
    fig, axes = plt.subplots(1, n_groups, figsize=(6 * n_groups, 5), sharey=True)
    if n_groups == 1:
        axes = [axes]

    colors = sns.color_palette("muted", n_groups)
    for ax, (label, values), color in zip(axes, groups.items(), colors):
        sns.histplot(values.dropna(), kde=True, ax=ax, color=color, bins=20)
        ax.set_title(label)
        ax.set_xlabel(metric_label)
        ax.axvline(values.mean(), color="red", linestyle="--", linewidth=1, label=f"Mean: {values.mean():,.0f}")
        ax.axvline(values.median(), color="green", linestyle=":", linewidth=1, label=f"Median: {values.median():,.0f}")
        ax.legend(fontsize=8)

    fig.suptitle(title, fontweight="bold", fontsize=14)
    fig.tight_layout()
    return fig


def plot_boxplot_comparison(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    order: Optional[list[str]] = None,
) -> plt.Figure:
    """Create a boxplot comparing groups.

    Parameters
    ----------
    df : pd.DataFrame
        Data with columns x and y.
    x : str
        Categorical column for grouping.
    y : str
        Numeric column for values.
    title : str
        Plot title.
    order : list[str], optional
        Order of categories on x-axis.

    Returns
    -------
    plt.Figure
    """
    set_default_theme()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x=x, y=y, order=order, ax=ax, hue=x, palette="muted", legend=False)
    ax.set_title(title, fontweight="bold")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    fig.tight_layout()
    return fig


def plot_correlation_heatmap(
    df: pd.DataFrame,
    line_ids: Optional[list[str]] = None,
    metric: str = "avg_daily_boardings",
    title: str = "Line-to-Line Ridership Correlation (Monthly)",
) -> plt.Figure:
    """Plot a heatmap of pairwise Pearson correlations between line ridership series.

    Parameters
    ----------
    df : pd.DataFrame
        Clean ridership data with 'date', 'line_id', and metric columns.
    line_ids : list[str], optional
        Lines to include. Defaults to gold, a_line, red, green, expo.
    metric : str
        Column name for values.
    title : str
        Plot title.

    Returns
    -------
    plt.Figure
    """
    set_default_theme()
    if line_ids is None:
        line_ids = ["gold", "a_line", "red", "green", "expo"]

    pivot = df[df["line_id"].isin(line_ids)].pivot_table(
        index="date", columns="line_id", values=metric
    )
    # Rename columns to human-readable names using LINE_STYLES
    pivot.columns = [LINE_STYLES.get(c, (c, None))[0] for c in pivot.columns]

    corr = pivot.corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        vmin=-1,
        vmax=1,
        square=True,
        ax=ax,
        linewidths=0.5,
    )
    ax.set_title(title, fontweight="bold")
    fig.tight_layout()
    return fig
