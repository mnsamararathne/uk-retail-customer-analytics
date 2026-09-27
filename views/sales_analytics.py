# ============================================================
# SALES ANALYTICS
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils.data_loader import load_dashboard_data


# ============================================================
# 3. LOAD DATA
# ============================================================

try:

    data = load_dashboard_data()

except Exception as error:

    st.error(
        "Sales analytics data could not be loaded."
    )

    st.exception(error)

    st.stop()


monthly_df = data["monthly_performance"]


# Load additional datasets directly through our loader
# if they are not already included in load_dashboard_data().

from utils.data_loader import load_csv


daily_df = load_csv(
    "daily_performance.csv"
)

weekday_df = load_csv(
    "weekday_performance.csv"
)

hourly_df = load_csv(
    "hourly_performance.csv"
)


# ============================================================
# 4. DATA PREPARATION
# ============================================================

# Convert date column

if "Date" in daily_df.columns:

    daily_df["Date"] = pd.to_datetime(
        daily_df["Date"],
        errors="coerce"
    )


# Ensure monthly data is correctly ordered

monthly_df = monthly_df.copy()


if "YearMonth" in monthly_df.columns:

    monthly_df["MonthDate"] = pd.to_datetime(
        monthly_df["YearMonth"],
        format="%Y-%m",
        errors="coerce"
    )

    monthly_df = (
        monthly_df
        .sort_values("MonthDate")
        .reset_index(drop=True)
    )


# ============================================================
# 5. PAGE HEADER
# ============================================================

st.title(
    "📈 Sales Analytics"
)

st.caption(
    "Detailed analysis of revenue, orders, average order value "
    "and temporal purchasing behaviour."
)

st.divider()


# ============================================================
# 6. SALES KPI CARDS
# ============================================================

total_revenue = (
    monthly_df["Revenue"].sum()
)

total_orders = (
    monthly_df["Orders"].sum()
)

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)

average_monthly_revenue = (
    monthly_df["Revenue"].mean()
)

best_month_row = (
    monthly_df.loc[
        monthly_df["Revenue"].idxmax()
    ]
)

best_month = (
    best_month_row["YearMonth"]
)

best_month_revenue = (
    best_month_row["Revenue"]
)


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Sales Revenue",
        f"£{total_revenue:,.0f}"
    )


with kpi2:

    st.metric(
        "Orders",
        f"{total_orders:,.0f}"
    )


with kpi3:

    st.metric(
        "Average Order Value",
        f"£{average_order_value:,.2f}"
    )


with kpi4:

    st.metric(
        "Avg. Monthly Revenue",
        f"£{average_monthly_revenue:,.0f}"
    )


st.caption(
    f"Highest-revenue month: "
    f"**{best_month}** "
    f"(£{best_month_revenue:,.0f})"
)


st.divider()


# ============================================================
# 7. MONTHLY REVENUE & ORDERS
# ============================================================

st.subheader(
    "Monthly Performance"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Monthly Revenue
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=monthly_df,
        x="YearMonth",
        y="Revenue",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Monthly Revenue Trend"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Revenue (£)"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Monthly Orders
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=monthly_df,
        x="YearMonth",
        y="Orders",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Monthly Order Trend"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Orders"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 8. AVERAGE ORDER VALUE & REVENUE GROWTH
# ============================================================

st.subheader(
    "Value & Growth Performance"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Average Order Value
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=monthly_df,
        x="YearMonth",
        y="AverageOrderValue",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Monthly Average Order Value"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Average Order Value (£)"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Revenue Growth
# ------------------------------------------------------------

with right:

    growth_df = (
        monthly_df
        .dropna(
            subset=["RevenueGrowthPct"]
        )
        .copy()
    )


    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=growth_df,
        x="YearMonth",
        y="RevenueGrowthPct",
        ax=ax
    )


    ax.axhline(
        0,
        linewidth=1
    )


    ax.set_title(
        "Month-on-Month Revenue Growth"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Growth (%)"
    )

    ax.tick_params(
        axis="x",
        rotation=45
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 9. DAILY SALES TREND
# ============================================================

st.subheader(
    "Daily Revenue Behaviour"
)


fig, ax = plt.subplots(
    figsize=(13, 5)
)


ax.plot(
    daily_df["Date"],
    daily_df["Revenue"],
    alpha=0.35,
    label="Daily Revenue"
)


if "RevenueRolling7Day" in daily_df.columns:

    ax.plot(
        daily_df["Date"],
        daily_df["RevenueRolling7Day"],
        linewidth=2,
        label="7-Day Rolling Average"
    )


ax.set_title(
    "Daily Revenue and 7-Day Rolling Average"
)

ax.set_xlabel(
    "Date"
)

ax.set_ylabel(
    "Revenue (£)"
)

ax.legend()

ax.grid(
    alpha=0.2
)


plt.xticks(
    rotation=45
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.divider()


# ============================================================
# 10. WEEKDAY PERFORMANCE
# ============================================================

st.subheader(
    "Day-of-Week Performance"
)


left, right = st.columns(2)


weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


weekday_df = weekday_df.copy()


if "DayOfWeek" in weekday_df.columns:

    weekday_df["DayOfWeek"] = pd.Categorical(
        weekday_df["DayOfWeek"],
        categories=weekday_order,
        ordered=True
    )

    weekday_df = weekday_df.sort_values(
        "DayOfWeek"
    )


# ------------------------------------------------------------
# Revenue by Weekday
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=weekday_df,
        x="DayOfWeek",
        y="Revenue",
        ax=ax
    )


    ax.set_title(
        "Revenue by Day of Week"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylabel(
        "Revenue (£)"
    )

    ax.tick_params(
        axis="x",
        rotation=30
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Orders by Weekday
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=weekday_df,
        x="DayOfWeek",
        y="Orders",
        ax=ax
    )


    ax.set_title(
        "Orders by Day of Week"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylabel(
        "Orders"
    )

    ax.tick_params(
        axis="x",
        rotation=30
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 11. HOURLY PERFORMANCE
# ============================================================

st.subheader(
    "Hourly Purchasing Behaviour"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Hourly Revenue
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=hourly_df,
        x="Hour",
        y="Revenue",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Revenue by Hour"
    )

    ax.set_xlabel(
        "Hour of Day"
    )

    ax.set_ylabel(
        "Revenue (£)"
    )

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Hourly Orders
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=hourly_df,
        x="Hour",
        y="Orders",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Orders by Hour"
    )

    ax.set_xlabel(
        "Hour of Day"
    )

    ax.set_ylabel(
        "Orders"
    )

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 12. DAY × HOUR SALES HEATMAP
# ============================================================

st.subheader(
    "Sales Activity Heatmap"
)


# We use transaction_segments because it contains
# transaction-level information required for this analysis.

transaction_df = load_csv(
    "transaction_segments.csv"
)


transaction_df["InvoiceDate"] = pd.to_datetime(
    transaction_df["InvoiceDate"],
    errors="coerce"
)


# Create required temporal features if necessary

if "DayOfWeek" not in transaction_df.columns:

    transaction_df["DayOfWeek"] = (
        transaction_df["InvoiceDate"]
        .dt.day_name()
    )


if "Hour" not in transaction_df.columns:

    transaction_df["Hour"] = (
        transaction_df["InvoiceDate"]
        .dt.hour
    )


heatmap_data = (

    transaction_df

    .pivot_table(
        values="Revenue",
        index="DayOfWeek",
        columns="Hour",
        aggfunc="sum",
        fill_value=0
    )

    .reindex(
        weekday_order
    )
)


fig, ax = plt.subplots(
    figsize=(14, 6)
)


sns.heatmap(
    heatmap_data,
    cmap="YlGnBu",
    ax=ax
)


ax.set_title(
    "Revenue Intensity by Day and Hour"
)

ax.set_xlabel(
    "Hour of Day"
)

ax.set_ylabel(
    "Day of Week"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.caption(
    "Darker areas represent periods with higher sales revenue."
)


st.divider()


# ============================================================
# 13. MONTHLY PERFORMANCE TABLE
# ============================================================

st.subheader(
    "Monthly Performance Details"
)


display_columns = [

    "YearMonth",
    "Revenue",
    "Orders",
    "Customers",
    "Units",
    "AverageOrderValue",
    "RevenueGrowthPct",
    "OrderGrowthPct"
]


display_columns = [

    column

    for column in display_columns

    if column in monthly_df.columns
]


st.dataframe(
    monthly_df[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 14. PAGE FOOTER
# ============================================================

st.divider()


st.caption(
    "Sales Analytics | "
    "UK Retail Customer Analytics"
)