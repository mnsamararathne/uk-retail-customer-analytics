# ============================================================
# CHART UTILITIES
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================

import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# FINALISE FIGURE
# ============================================================

def finalise_chart(
    ax,
    title,
    xlabel="",
    ylabel="",
    grid_axis="y"
):
    """
    Apply common formatting to a Matplotlib Axes object.
    """

    ax.set_title(
        title,
        loc="left",
        pad=15
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if grid_axis:
        ax.grid(
            axis=grid_axis,
            alpha=0.2
        )

    return ax


# ============================================================
# HORIZONTAL BAR CHART
# ============================================================

def horizontal_bar_chart(
    data,
    x,
    y,
    title,
    xlabel="",
    ylabel="",
    figsize=(10, 6)
):
    """
    Generate a standard horizontal ranking chart.
    """

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.barplot(
        data=data,
        x=x,
        y=y,
        ax=ax
    )

    finalise_chart(
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        grid_axis="x"
    )

    return fig, ax


# ============================================================
# LINE CHART
# ============================================================

def line_chart(
    data,
    x,
    y,
    title,
    xlabel="",
    ylabel="",
    figsize=(10, 5)
):
    """
    Generate a standard time-series line chart.
    """

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.lineplot(
        data=data,
        x=x,
        y=y,
        marker="o",
        ax=ax
    )

    finalise_chart(
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        grid_axis="y"
    )

    return fig, ax


# ============================================================
# DISTRIBUTION CHART
# ============================================================

def distribution_chart(
    data,
    column,
    title,
    xlabel="",
    bins=40,
    kde=True,
    figsize=(10, 5)
):
    """
    Generate a histogram / KDE distribution chart.
    """

    fig, ax = plt.subplots(
        figsize=figsize
    )

    sns.histplot(
        data=data,
        x=column,
        bins=bins,
        kde=kde,
        ax=ax
    )

    finalise_chart(
        ax=ax,
        title=title,
        xlabel=xlabel,
        ylabel="Frequency",
        grid_axis="y"
    )

    return fig, ax


# ============================================================
# CLOSE FIGURE
# ============================================================

def close_chart(fig):
    """
    Close a Matplotlib figure after Streamlit rendering.
    """

    plt.close(fig)