# ============================================================
# CUSTOMER ANALYTICS
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.data_loader import load_csv


# ============================================================
# 3. LOAD DATA
# ============================================================

try:

    customer_df = load_csv(
        "customer_performance.csv"
    )

    customer_pareto = load_csv(
        "customer_pareto.csv"
    )

except Exception as error:

    st.error(
        "Customer analytics data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 4. DATA VALIDATION
# ============================================================

required_columns = [
    "CustomerID",
    "TotalRevenue",
    "OrderCount",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]


missing_columns = [

    column
    for column in required_columns
    if column not in customer_df.columns

]


if missing_columns:

    st.error(
        "Required customer columns are missing: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# 5. PAGE HEADER
# ============================================================

st.title(
    "👥 Customer Analytics"
)

st.caption(
    "Analysis of customer value, purchasing frequency, "
    "order behaviour and revenue concentration."
)

st.divider()


# ============================================================
# 6. CUSTOMER KPIs
# ============================================================

total_customers = (
    customer_df["CustomerID"]
    .nunique()
)


total_customer_revenue = (
    customer_df["TotalRevenue"]
    .sum()
)


average_customer_revenue = (
    customer_df["TotalRevenue"]
    .mean()
)


median_customer_revenue = (
    customer_df["TotalRevenue"]
    .median()
)


average_orders = (
    customer_df["OrderCount"]
    .mean()
)


average_customer_aov = (
    customer_df["AverageOrderValue"]
    .mean()
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "Customers",
        f"{total_customers:,.0f}"
    )


with kpi2:

    st.metric(
        "Customer Revenue",
        f"£{total_customer_revenue:,.0f}"
    )


with kpi3:

    st.metric(
        "Average Revenue / Customer",
        f"£{average_customer_revenue:,.2f}"
    )


kpi4, kpi5, kpi6 = st.columns(3)


with kpi4:

    st.metric(
        "Median Revenue / Customer",
        f"£{median_customer_revenue:,.2f}"
    )


with kpi5:

    st.metric(
        "Average Orders / Customer",
        f"{average_orders:,.2f}"
    )


with kpi6:

    st.metric(
        "Mean Customer AOV",
        f"£{average_customer_aov:,.2f}"
    )


st.divider()


# ============================================================
# 7. CUSTOMER VALUE DISTRIBUTION
# ============================================================

st.subheader(
    "Customer Value Distribution"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# 7.1 Customer Revenue Distribution
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=customer_df,
        x="TotalRevenue",
        bins=50,
        kde=True,
        ax=ax
    )


    ax.set_title(
        "Distribution of Customer Revenue"
    )

    ax.set_xlabel(
        "Total Customer Revenue (£)"
    )

    ax.set_ylabel(
        "Customers"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# 7.2 Customer Revenue Boxplot
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.boxplot(
        data=customer_df,
        x="TotalRevenue",
        ax=ax
    )


    ax.set_title(
        "Customer Revenue Distribution and Outliers"
    )

    ax.set_xlabel(
        "Total Customer Revenue (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.info(
    "The histogram shows the overall shape of customer value, "
    "while the boxplot helps identify unusually high-value customers."
)


st.divider()


# ============================================================
# 8. PURCHASE FREQUENCY & ORDER VALUE
# ============================================================

st.subheader(
    "Purchasing Behaviour"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# 8.1 Order Frequency Distribution
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=customer_df,
        x="OrderCount",
        bins=30,
        kde=False,
        ax=ax
    )


    ax.set_title(
        "Distribution of Orders per Customer"
    )

    ax.set_xlabel(
        "Number of Orders"
    )

    ax.set_ylabel(
        "Customers"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# 8.2 Customer Average Order Value
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=customer_df,
        x="AverageOrderValue",
        bins=40,
        kde=True,
        ax=ax
    )


    ax.set_title(
        "Distribution of Customer Average Order Value"
    )

    ax.set_xlabel(
        "Average Order Value (£)"
    )

    ax.set_ylabel(
        "Customers"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 9. CUSTOMER VALUE VS PURCHASE FREQUENCY
# ============================================================

st.subheader(
    "Customer Value vs Purchase Frequency"
)


fig, ax = plt.subplots(
    figsize=(11, 6)
)


sns.scatterplot(
    data=customer_df,
    x="OrderCount",
    y="TotalRevenue",
    size="UniqueProducts",
    alpha=0.6,
    ax=ax
)


ax.set_title(
    "Customer Revenue vs Number of Orders"
)

ax.set_xlabel(
    "Number of Orders"
)

ax.set_ylabel(
    "Total Revenue (£)"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.caption(
    "Bubble size represents the number of unique products "
    "purchased by each customer."
)


st.divider()


# ============================================================
# 10. CUSTOMER RELATIONSHIPS
# ============================================================

st.subheader(
    "Customer Behaviour Relationships"
)


correlation_columns = [
    "TotalRevenue",
    "OrderCount",
    "TotalQuantity",
    "UniqueProducts",
    "AverageOrderValue"
]


if "ActiveDays" in customer_df.columns:

    correlation_columns.append(
        "ActiveDays"
    )


correlation_matrix = (

    customer_df[
        correlation_columns
    ]

    .corr()
)


fig, ax = plt.subplots(
    figsize=(9, 6)
)


sns.heatmap(
    correlation_matrix,
    annot=True,
    fmt=".2f",
    center=0,
    ax=ax
)


ax.set_title(
    "Customer Behaviour Correlation Matrix"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.divider()


# ============================================================
# 11. TOP CUSTOMERS
# ============================================================

st.subheader(
    "Highest-Value Customers"
)


top_n = st.slider(
    "Number of customers to display",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)


top_customers = (

    customer_df

    .nlargest(
        top_n,
        "TotalRevenue"
    )

    .copy()
)


top_customers["CustomerLabel"] = (

    top_customers[
        "CustomerID"
    ]
    .astype(str)
)


chart_data = (

    top_customers

    .sort_values(
        "TotalRevenue",
        ascending=True
    )
)


fig, ax = plt.subplots(
    figsize=(10, 7)
)


sns.barplot(
    data=chart_data,
    x="TotalRevenue",
    y="CustomerLabel",
    ax=ax
)


ax.set_title(
    f"Top {top_n} Customers by Revenue"
)

ax.set_xlabel(
    "Total Revenue (£)"
)

ax.set_ylabel(
    "Customer ID"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


# Detailed top-customer table

top_customer_columns = [
    "CustomerID",
    "TotalRevenue",
    "OrderCount",
    "AverageOrderValue",
    "TotalQuantity",
    "UniqueProducts"
]


st.dataframe(
    top_customers[
        top_customer_columns
    ],
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# 12. CUSTOMER PARETO ANALYSIS
# ============================================================

st.subheader(
    "Customer Revenue Concentration"
)


required_pareto_columns = [
    "CumulativeCustomerPct",
    "CumulativeRevenuePct"
]


pareto_available = all(

    column in customer_pareto.columns

    for column in required_pareto_columns
)


if pareto_available:

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )


    ax.plot(
        customer_pareto[
            "CumulativeCustomerPct"
        ],
        customer_pareto[
            "CumulativeRevenuePct"
        ],
        linewidth=2
    )


    ax.axvline(
        x=20,
        linestyle="--",
        label="Top 20% of Customers"
    )


    ax.axhline(
        y=80,
        linestyle="--",
        label="80% of Revenue"
    )


    ax.set_title(
        "Customer Revenue Pareto Curve"
    )

    ax.set_xlabel(
        "Cumulative Customers (%)"
    )

    ax.set_ylabel(
        "Cumulative Revenue (%)"
    )


    ax.set_xlim(
        0,
        100
    )

    ax.set_ylim(
        0,
        100
    )


    ax.legend()

    ax.grid(
        alpha=0.2
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


else:

    st.warning(
        "Pareto columns are not available."
    )


# ============================================================
# 13. CUSTOMER CONCENTRATION METRICS
# ============================================================

if (
    "TotalRevenue"
    in customer_pareto.columns
):

    customer_sorted = (

        customer_pareto

        .sort_values(
            "TotalRevenue",
            ascending=False
        )

        .reset_index(
            drop=True
        )
    )


    total_pareto_revenue = (

        customer_sorted[
            "TotalRevenue"
        ]
        .sum()
    )


    number_customers = len(
        customer_sorted
    )


    top_10_count = max(
        1,
        int(
            np.ceil(
                number_customers * 0.10
            )
        )
    )


    top_20_count = max(
        1,
        int(
            np.ceil(
                number_customers * 0.20
            )
        )
    )


    top_10_share = (

        customer_sorted

        .head(
            top_10_count
        )[
            "TotalRevenue"
        ]

        .sum()

        /

        total_pareto_revenue

        * 100
    )


    top_20_share = (

        customer_sorted

        .head(
            top_20_count
        )[
            "TotalRevenue"
        ]

        .sum()

        /

        total_pareto_revenue

        * 100
    )


    concentration1, concentration2 = (
        st.columns(2)
    )


    with concentration1:

        st.metric(
            "Revenue from Top 10% Customers",
            f"{top_10_share:.1f}%"
        )


    with concentration2:

        st.metric(
            "Revenue from Top 20% Customers",
            f"{top_20_share:.1f}%"
        )


    st.caption(
        "These measures quantify how strongly business revenue "
        "is concentrated among the highest-value customers."
    )


st.divider()


# ============================================================
# 14. CUSTOMER EXPLORER
# ============================================================

st.subheader(
    "Customer Explorer"
)


search_customer = st.text_input(
    "Search Customer ID",
    placeholder="Enter a Customer ID"
)


if search_customer:

    customer_search_df = (

        customer_df[
            customer_df[
                "CustomerID"
            ]
            .astype(str)
            .str.contains(
                search_customer,
                case=False,
                na=False
            )
        ]
    )


    if customer_search_df.empty:

        st.warning(
            "No matching customer was found."
        )


    else:

        st.dataframe(
            customer_search_df,
            use_container_width=True,
            hide_index=True
        )


else:

    st.caption(
        "Enter a Customer ID to inspect an individual "
        "customer's purchasing behaviour."
    )


# ============================================================
# 15. FULL CUSTOMER DATA
# ============================================================

with st.expander(
    "Explore Customer Performance Dataset"
):

    st.dataframe(
        customer_df.sort_values(
            "TotalRevenue",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 16. FOOTER
# ============================================================

st.divider()


st.caption(
    "Customer Analytics | UK Retail Customer Analytics"
)