# ============================================================
# PRODUCT ANALYTICS
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

    product_df = load_csv(
        "product_performance.csv"
    )

    product_pareto = load_csv(
        "product_pareto.csv"
    )

except Exception as error:

    st.error(
        "Product analytics data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 4. DATA VALIDATION
# ============================================================

required_columns = [
    "StockCode",
    "TotalRevenue",
    "TotalQuantity"
]


missing_columns = [
    column
    for column in required_columns
    if column not in product_df.columns
]


if missing_columns:

    st.error(
        "Required product columns are missing: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# 5. CREATE PRODUCT LABEL
# ============================================================

product_df = product_df.copy()


if "Description" in product_df.columns:

    product_df["ProductLabel"] = (
        product_df["Description"]
        .fillna(
            product_df["StockCode"].astype(str)
        )
        .astype(str)
        .str.slice(0, 45)
    )

else:

    product_df["ProductLabel"] = (
        product_df["StockCode"]
        .astype(str)
    )


# ============================================================
# 6. PAGE HEADER
# ============================================================

st.title(
    "📦 Product Analytics"
)

st.caption(
    "Analysis of product revenue, demand, customer reach "
    "and product-level revenue concentration."
)

st.divider()


# ============================================================
# 7. PRODUCT KPI CARDS
# ============================================================

total_products = (
    product_df["StockCode"]
    .nunique()
)


total_product_revenue = (
    product_df["TotalRevenue"]
    .sum()
)


total_units = (
    product_df["TotalQuantity"]
    .sum()
)


average_revenue_product = (
    product_df["TotalRevenue"]
    .mean()
)


median_revenue_product = (
    product_df["TotalRevenue"]
    .median()
)


top_product_row = (
    product_df.loc[
        product_df[
            "TotalRevenue"
        ].idxmax()
    ]
)


top_product_name = (
    top_product_row[
        "ProductLabel"
    ]
)


top_product_revenue = (
    top_product_row[
        "TotalRevenue"
    ]
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "Products",
        f"{total_products:,}"
    )


with kpi2:

    st.metric(
        "Product Revenue",
        f"£{total_product_revenue:,.0f}"
    )


with kpi3:

    st.metric(
        "Units Sold",
        f"{total_units:,.0f}"
    )


kpi4, kpi5, kpi6 = st.columns(3)


with kpi4:

    st.metric(
        "Average Revenue / Product",
        f"£{average_revenue_product:,.2f}"
    )


with kpi5:

    st.metric(
        "Median Revenue / Product",
        f"£{median_revenue_product:,.2f}"
    )


with kpi6:

    st.metric(
        "Top Product Revenue",
        f"£{top_product_revenue:,.0f}"
    )


st.caption(
    f"Highest-revenue product: **{top_product_name}**"
)


st.divider()


# ============================================================
# 8. TOP N CONTROL
# ============================================================

st.subheader(
    "Product Rankings"
)


top_n = st.slider(
    "Number of products to display",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)


# ============================================================
# 9. TOP PRODUCTS BY REVENUE
# ============================================================

left, right = st.columns(2)


with left:

    top_revenue_products = (
        product_df
        .nlargest(
            top_n,
            "TotalRevenue"
        )
        .sort_values(
            "TotalRevenue",
            ascending=True
        )
    )


    fig, ax = plt.subplots(
        figsize=(9, 7)
    )


    sns.barplot(
        data=top_revenue_products,
        x="TotalRevenue",
        y="ProductLabel",
        ax=ax
    )


    ax.set_title(
        f"Top {top_n} Products by Revenue"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        "Product"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ============================================================
# 10. TOP PRODUCTS BY QUANTITY
# ============================================================

with right:

    top_quantity_products = (
        product_df
        .nlargest(
            top_n,
            "TotalQuantity"
        )
        .sort_values(
            "TotalQuantity",
            ascending=True
        )
    )


    fig, ax = plt.subplots(
        figsize=(9, 7)
    )


    sns.barplot(
        data=top_quantity_products,
        x="TotalQuantity",
        y="ProductLabel",
        ax=ax
    )


    ax.set_title(
        f"Top {top_n} Products by Units Sold"
    )

    ax.set_xlabel(
        "Units Sold"
    )

    ax.set_ylabel(
        "Product"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 11. CUSTOMER REACH
# ============================================================

st.subheader(
    "Product Customer Reach"
)


customer_column_candidates = [
    "UniqueCustomers",
    "Customers",
    "CustomerCount"
]


customer_count_column = None


for column in customer_column_candidates:

    if column in product_df.columns:

        customer_count_column = column
        break


if customer_count_column is not None:

    top_customer_reach = (
        product_df
        .nlargest(
            top_n,
            customer_count_column
        )
        .sort_values(
            customer_count_column,
            ascending=True
        )
    )


    fig, ax = plt.subplots(
        figsize=(11, 7)
    )


    sns.barplot(
        data=top_customer_reach,
        x=customer_count_column,
        y="ProductLabel",
        ax=ax
    )


    ax.set_title(
        f"Top {top_n} Products by Customer Reach"
    )

    ax.set_xlabel(
        "Unique Customers"
    )

    ax.set_ylabel(
        "Product"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


else:

    st.info(
        "A unique-customer count is not available in "
        "product_performance.csv."
    )


st.divider()


# ============================================================
# 12. PRODUCT REVENUE DISTRIBUTION
# ============================================================

st.subheader(
    "Product Performance Distribution"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Revenue Histogram
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=product_df,
        x="TotalRevenue",
        bins=50,
        kde=True,
        ax=ax
    )


    ax.set_title(
        "Distribution of Product Revenue"
    )

    ax.set_xlabel(
        "Product Revenue (£)"
    )

    ax.set_ylabel(
        "Products"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Revenue Boxplot
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.boxplot(
        data=product_df,
        x="TotalRevenue",
        ax=ax
    )


    ax.set_title(
        "Product Revenue Distribution and Outliers"
    )

    ax.set_xlabel(
        "Product Revenue (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.caption(
    "These charts help distinguish the typical product "
    "performance range from unusually high-revenue products."
)


st.divider()


# ============================================================
# 13. DEMAND VS REVENUE
# ============================================================

st.subheader(
    "Demand vs Revenue"
)


fig, ax = plt.subplots(
    figsize=(11, 6)
)


if customer_count_column is not None:

    sns.scatterplot(
        data=product_df,
        x="TotalQuantity",
        y="TotalRevenue",
        size=customer_count_column,
        alpha=0.6,
        ax=ax
    )

else:

    sns.scatterplot(
        data=product_df,
        x="TotalQuantity",
        y="TotalRevenue",
        alpha=0.6,
        ax=ax
    )


ax.set_title(
    "Product Demand vs Revenue"
)

ax.set_xlabel(
    "Units Sold"
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


if customer_count_column is not None:

    st.caption(
        "Bubble size represents customer reach. This view "
        "helps distinguish high-volume products from products "
        "that generate high revenue or reach a broad customer base."
    )


st.divider()


# ============================================================
# 14. QUANTITY VS CUSTOMER REACH
# ============================================================

if customer_count_column is not None:

    st.subheader(
        "Demand and Customer Reach"
    )


    fig, ax = plt.subplots(
        figsize=(11, 6)
    )


    sns.scatterplot(
        data=product_df,
        x=customer_count_column,
        y="TotalQuantity",
        size="TotalRevenue",
        alpha=0.6,
        ax=ax
    )


    ax.set_title(
        "Customer Reach vs Units Sold"
    )

    ax.set_xlabel(
        "Unique Customers"
    )

    ax.set_ylabel(
        "Units Sold"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


    st.caption(
        "Bubble size represents total product revenue."
    )


    st.divider()


# ============================================================
# 15. PRODUCT CORRELATION ANALYSIS
# ============================================================

st.subheader(
    "Product Performance Relationships"
)


correlation_columns = [
    "TotalRevenue",
    "TotalQuantity"
]


optional_correlation_columns = [
    "OrderCount",
    "Orders",
    "UniqueCustomers",
    "Customers",
    "AverageUnitPrice"
]


for column in optional_correlation_columns:

    if column in product_df.columns:

        correlation_columns.append(
            column
        )


# Remove duplicates

correlation_columns = list(
    dict.fromkeys(
        correlation_columns
    )
)


correlation_matrix = (
    product_df[
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
    "Product Performance Correlation Matrix"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.divider()


# ============================================================
# 16. PRODUCT PARETO ANALYSIS
# ============================================================

st.subheader(
    "Product Revenue Concentration"
)


pareto_x_candidates = [
    "CumulativeProductPct",
    "CumulativeProductsPct"
]


pareto_y_candidates = [
    "CumulativeRevenuePct"
]


pareto_x = None
pareto_y = None


for column in pareto_x_candidates:

    if column in product_pareto.columns:

        pareto_x = column
        break


for column in pareto_y_candidates:

    if column in product_pareto.columns:

        pareto_y = column
        break


if (
    pareto_x is not None
    and
    pareto_y is not None
):

    fig, ax = plt.subplots(
        figsize=(11, 6)
    )


    ax.plot(
        product_pareto[
            pareto_x
        ],
        product_pareto[
            pareto_y
        ],
        linewidth=2
    )


    ax.axvline(
        20,
        linestyle="--",
        label="Top 20% of Products"
    )


    ax.axhline(
        80,
        linestyle="--",
        label="80% of Revenue"
    )


    ax.set_title(
        "Product Revenue Pareto Curve"
    )

    ax.set_xlabel(
        "Cumulative Products (%)"
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


    ax.grid(
        alpha=0.2
    )

    ax.legend()


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


else:

    st.warning(
        "Required product Pareto columns could not "
        "be identified."
    )


# ============================================================
# 17. PRODUCT CONCENTRATION METRICS
# ============================================================

pareto_revenue_column = None


for candidate in [
    "TotalRevenue",
    "Revenue"
]:

    if candidate in product_pareto.columns:

        pareto_revenue_column = candidate
        break


if pareto_revenue_column is not None:

    pareto_sorted = (
        product_pareto
        .sort_values(
            pareto_revenue_column,
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    total_pareto_revenue = (
        pareto_sorted[
            pareto_revenue_column
        ]
        .sum()
    )


    product_count = len(
        pareto_sorted
    )


    top_10_count = max(
        1,
        int(
            np.ceil(
                product_count * 0.10
            )
        )
    )


    top_20_count = max(
        1,
        int(
            np.ceil(
                product_count * 0.20
            )
        )
    )


    if total_pareto_revenue != 0:

        top_10_share = (
            pareto_sorted
            .head(
                top_10_count
            )[
                pareto_revenue_column
            ]
            .sum()
            /
            total_pareto_revenue
            * 100
        )


        top_20_share = (
            pareto_sorted
            .head(
                top_20_count
            )[
                pareto_revenue_column
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
                "Revenue from Top 10% Products",
                f"{top_10_share:.1f}%"
            )


        with concentration2:

            st.metric(
                "Revenue from Top 20% Products",
                f"{top_20_share:.1f}%"
            )


st.caption(
    "The Pareto analysis measures whether product revenue "
    "is broadly distributed across the catalogue or concentrated "
    "among a relatively small number of products."
)


st.divider()


# ============================================================
# 18. PRODUCT EXPLORER
# ============================================================

st.subheader(
    "Product Explorer"
)


search_type = st.radio(
    "Search using",
    [
        "Description",
        "Stock Code"
    ],
    horizontal=True
)


search_value = st.text_input(
    "Search product",
    placeholder="Enter product description or stock code"
)


if search_value:

    if (
        search_type == "Description"
        and
        "Description" in product_df.columns
    ):

        search_results = (
            product_df[
                product_df[
                    "Description"
                ]
                .astype(str)
                .str.contains(
                    search_value,
                    case=False,
                    na=False
                )
            ]
        )

    else:

        search_results = (
            product_df[
                product_df[
                    "StockCode"
                ]
                .astype(str)
                .str.contains(
                    search_value,
                    case=False,
                    na=False
                )
            ]
        )


    if search_results.empty:

        st.warning(
            "No matching products were found."
        )

    else:

        st.dataframe(
            search_results,
            use_container_width=True,
            hide_index=True
        )


else:

    st.caption(
        "Search for an individual product to inspect "
        "its performance."
    )


st.divider()


# ============================================================
# 19. PRODUCT PERFORMANCE TABLE
# ============================================================

st.subheader(
    "Product Performance Details"
)


sort_metric = st.selectbox(
    "Sort products by",
    [
        "TotalRevenue",
        "TotalQuantity"
    ]
    +
    (
        [customer_count_column]
        if customer_count_column is not None
        else []
    )
)


sorted_products = (
    product_df
    .sort_values(
        sort_metric,
        ascending=False
    )
)


display_columns = [
    "StockCode",
    "Description",
    "TotalRevenue",
    "TotalQuantity",
    "OrderCount",
    "Orders",
    "UniqueCustomers",
    "Customers",
    "AverageUnitPrice"
]


display_columns = [
    column
    for column in display_columns
    if column in sorted_products.columns
]


st.dataframe(
    sorted_products[
        display_columns
    ],
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 20. FOOTER
# ============================================================

st.divider()


st.caption(
    "Product Analytics | "
    "UK Retail Customer Analytics"
)