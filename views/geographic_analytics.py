# ============================================================
# GEOGRAPHIC ANALYTICS
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

    country_df = load_csv(
        "country_performance.csv"
    )

except Exception as error:

    st.error(
        "Geographic analytics data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 4. DATA VALIDATION
# ============================================================

required_columns = [
    "Country",
    "Revenue"
]


missing_columns = [
    column
    for column in required_columns
    if column not in country_df.columns
]


if missing_columns:

    st.error(
        "Required geographic columns are missing: "
        + ", ".join(missing_columns)
    )

    st.stop()


country_df = country_df.copy()


# ============================================================
# 5. DETECT OPTIONAL COLUMNS
# ============================================================

order_candidates = [
    "Orders",
    "OrderCount"
]

customer_candidates = [
    "Customers",
    "UniqueCustomers",
    "CustomerCount"
]

aov_candidates = [
    "AverageOrderValue",
    "AOV"
]

revenue_customer_candidates = [
    "RevenuePerCustomer",
    "RevenuePerCustomerValue"
]


order_column = None
customer_column = None
aov_column = None
revenue_customer_column = None


for column in order_candidates:

    if column in country_df.columns:

        order_column = column
        break


for column in customer_candidates:

    if column in country_df.columns:

        customer_column = column
        break


for column in aov_candidates:

    if column in country_df.columns:

        aov_column = column
        break


for column in revenue_customer_candidates:

    if column in country_df.columns:

        revenue_customer_column = column
        break


# ============================================================
# 6. CREATE DERIVED METRICS WHEN NEEDED
# ============================================================

if (
    revenue_customer_column is None
    and
    customer_column is not None
):

    country_df[
        "RevenuePerCustomer"
    ] = np.where(

        country_df[
            customer_column
        ] > 0,

        country_df[
            "Revenue"
        ]
        /
        country_df[
            customer_column
        ],

        np.nan
    )

    revenue_customer_column = (
        "RevenuePerCustomer"
    )


if (
    aov_column is None
    and
    order_column is not None
):

    country_df[
        "AverageOrderValue"
    ] = np.where(

        country_df[
            order_column
        ] > 0,

        country_df[
            "Revenue"
        ]
        /
        country_df[
            order_column
        ],

        np.nan
    )

    aov_column = (
        "AverageOrderValue"
    )


# ============================================================
# 7. PAGE HEADER
# ============================================================

st.title(
    "🌍 Geographic Analytics"
)

st.caption(
    "Analysis of market performance across countries, "
    "including revenue, customers, orders and customer value."
)

st.divider()


# ============================================================
# 8. GEOGRAPHIC KPI CARDS
# ============================================================

number_countries = (
    country_df[
        "Country"
    ]
    .nunique()
)


total_revenue = (
    country_df[
        "Revenue"
    ]
    .sum()
)


top_country_row = (
    country_df.loc[
        country_df[
            "Revenue"
        ].idxmax()
    ]
)


top_country = (
    top_country_row[
        "Country"
    ]
)


top_country_revenue = (
    top_country_row[
        "Revenue"
    ]
)


top_country_share = (

    top_country_revenue
    /
    total_revenue
    * 100

    if total_revenue != 0

    else 0
)


kpi1, kpi2, kpi3, kpi4 = (
    st.columns(4)
)


with kpi1:

    st.metric(
        "Countries",
        f"{number_countries:,}"
    )


with kpi2:

    st.metric(
        "Total Revenue",
        f"£{total_revenue:,.0f}"
    )


with kpi3:

    st.metric(
        "Largest Market",
        str(top_country)
    )


with kpi4:

    st.metric(
        "Largest Market Share",
        f"{top_country_share:.1f}%"
    )


st.divider()


# ============================================================
# 9. TOP-N CONTROL
# ============================================================

top_n = st.slider(
    "Number of countries to compare",
    min_value=5,
    max_value=min(
        30,
        len(country_df)
    ),
    value=min(
        10,
        len(country_df)
    ),
    step=1
)


# ============================================================
# 10. REVENUE BY COUNTRY
# ============================================================

st.subheader(
    "Revenue by Country"
)


top_revenue_countries = (

    country_df

    .nlargest(
        top_n,
        "Revenue"
    )

    .sort_values(
        "Revenue",
        ascending=True
    )
)


fig, ax = plt.subplots(
    figsize=(11, 7)
)


sns.barplot(
    data=top_revenue_countries,
    x="Revenue",
    y="Country",
    ax=ax
)


ax.set_title(
    f"Top {top_n} Countries by Revenue"
)

ax.set_xlabel(
    "Revenue (£)"
)

ax.set_ylabel(
    "Country"
)


plt.tight_layout()


st.pyplot(
    fig,
    use_container_width=True
)


plt.close(fig)


st.divider()


# ============================================================
# 11. ORDERS AND CUSTOMERS
# ============================================================

if (
    order_column is not None
    or
    customer_column is not None
):

    st.subheader(
        "Market Activity"
    )


    left, right = st.columns(2)


    # --------------------------------------------------------
    # Orders
    # --------------------------------------------------------

    with left:

        if order_column is not None:

            top_orders = (

                country_df

                .nlargest(
                    top_n,
                    order_column
                )

                .sort_values(
                    order_column,
                    ascending=True
                )
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            sns.barplot(
                data=top_orders,
                x=order_column,
                y="Country",
                ax=ax
            )


            ax.set_title(
                f"Top {top_n} Countries by Orders"
            )

            ax.set_xlabel(
                "Orders"
            )

            ax.set_ylabel(
                "Country"
            )


            plt.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(fig)


        else:

            st.info(
                "Order counts are not available."
            )


    # --------------------------------------------------------
    # Customers
    # --------------------------------------------------------

    with right:

        if customer_column is not None:

            top_customers = (

                country_df

                .nlargest(
                    top_n,
                    customer_column
                )

                .sort_values(
                    customer_column,
                    ascending=True
                )
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            sns.barplot(
                data=top_customers,
                x=customer_column,
                y="Country",
                ax=ax
            )


            ax.set_title(
                f"Top {top_n} Countries by Customers"
            )

            ax.set_xlabel(
                "Customers"
            )

            ax.set_ylabel(
                "Country"
            )


            plt.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(fig)


        else:

            st.info(
                "Customer counts are not available."
            )


    st.divider()


# ============================================================
# 12. CUSTOMER VALUE BY COUNTRY
# ============================================================

if (
    revenue_customer_column is not None
    or
    aov_column is not None
):

    st.subheader(
        "Market Customer Value"
    )


    left, right = st.columns(2)


    # --------------------------------------------------------
    # Revenue per Customer
    # --------------------------------------------------------

    with left:

        if revenue_customer_column is not None:

            value_df = (

                country_df

                .dropna(
                    subset=[
                        revenue_customer_column
                    ]
                )

                .nlargest(
                    top_n,
                    revenue_customer_column
                )

                .sort_values(
                    revenue_customer_column,
                    ascending=True
                )
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            sns.barplot(
                data=value_df,
                x=revenue_customer_column,
                y="Country",
                ax=ax
            )


            ax.set_title(
                "Revenue per Customer by Country"
            )

            ax.set_xlabel(
                "Revenue per Customer (£)"
            )

            ax.set_ylabel(
                "Country"
            )


            plt.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(fig)


        else:

            st.info(
                "Revenue-per-customer data "
                "is not available."
            )


    # --------------------------------------------------------
    # Average Order Value
    # --------------------------------------------------------

    with right:

        if aov_column is not None:

            aov_df = (

                country_df

                .dropna(
                    subset=[
                        aov_column
                    ]
                )

                .nlargest(
                    top_n,
                    aov_column
                )

                .sort_values(
                    aov_column,
                    ascending=True
                )
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            sns.barplot(
                data=aov_df,
                x=aov_column,
                y="Country",
                ax=ax
            )


            ax.set_title(
                "Average Order Value by Country"
            )

            ax.set_xlabel(
                "Average Order Value (£)"
            )

            ax.set_ylabel(
                "Country"
            )


            plt.tight_layout()


            st.pyplot(
                fig,
                use_container_width=True
            )


            plt.close(fig)


        else:

            st.info(
                "Average-order-value data "
                "is not available."
            )


    st.divider()


# ============================================================
# 13. MARKET SIZE VS CUSTOMER VALUE
# ============================================================

if (
    customer_column is not None
    and
    revenue_customer_column is not None
):

    st.subheader(
        "Market Size vs Customer Value"
    )


    scatter_df = (

        country_df

        .dropna(
            subset=[
                customer_column,
                revenue_customer_column,
                "Revenue"
            ]
        )

        .copy()
    )


    fig, ax = plt.subplots(
        figsize=(11, 7)
    )


    sns.scatterplot(
        data=scatter_df,
        x=customer_column,
        y=revenue_customer_column,
        size="Revenue",
        alpha=0.7,
        ax=ax
    )


    # Annotate major revenue markets

    annotation_df = (

        scatter_df

        .nlargest(
            min(
                8,
                len(scatter_df)
            ),
            "Revenue"
        )
    )


    for _, row in annotation_df.iterrows():

        ax.annotate(
            str(
                row["Country"]
            ),
            (
                row[
                    customer_column
                ],
                row[
                    revenue_customer_column
                ]
            ),
            xytext=(5, 5),
            textcoords="offset points",
            fontsize=8
        )


    ax.set_title(
        "Customer Base vs Revenue per Customer"
    )

    ax.set_xlabel(
        "Customers"
    )

    ax.set_ylabel(
        "Revenue per Customer (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


    st.caption(
        "Bubble size represents total country revenue. "
        "This separates large customer markets from "
        "smaller markets with relatively high customer value."
    )


    st.divider()


# ============================================================
# 14. GEOGRAPHIC REVENUE DISTRIBUTION
# ============================================================

st.subheader(
    "Geographic Revenue Distribution"
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Distribution
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=country_df,
        x="Revenue",
        bins=25,
        kde=True,
        ax=ax
    )


    ax.set_title(
        "Distribution of Country Revenue"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )

    ax.set_ylabel(
        "Countries"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


# ------------------------------------------------------------
# Boxplot
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.boxplot(
        data=country_df,
        x="Revenue",
        ax=ax
    )


    ax.set_title(
        "Country Revenue Spread"
    )

    ax.set_xlabel(
        "Revenue (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 15. GEOGRAPHIC CONCENTRATION
# ============================================================

st.subheader(
    "Geographic Revenue Concentration"
)


country_sorted = (

    country_df

    .sort_values(
        "Revenue",
        ascending=False
    )

    .reset_index(
        drop=True
    )
)


country_sorted[
    "CumulativeRevenue"
] = (

    country_sorted[
        "Revenue"
    ]
    .cumsum()
)


country_sorted[
    "CumulativeRevenuePct"
] = (

    country_sorted[
        "CumulativeRevenue"
    ]

    /

    country_sorted[
        "Revenue"
    ].sum()

    * 100
)


country_sorted[
    "CumulativeCountryPct"
] = (

    (
        np.arange(
            1,
            len(
                country_sorted
            ) + 1
        )
        /
        len(
            country_sorted
        )
    )

    * 100
)


fig, ax = plt.subplots(
    figsize=(11, 6)
)


ax.plot(
    country_sorted[
        "CumulativeCountryPct"
    ],
    country_sorted[
        "CumulativeRevenuePct"
    ],
    linewidth=2
)


ax.axhline(
    80,
    linestyle="--",
    label="80% of Revenue"
)


ax.axvline(
    20,
    linestyle="--",
    label="20% of Countries"
)


ax.set_title(
    "Geographic Revenue Concentration Curve"
)

ax.set_xlabel(
    "Cumulative Countries (%)"
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


# ============================================================
# 16. TOP MARKET CONCENTRATION METRICS
# ============================================================

top_1_share = (

    country_sorted
    .head(1)[
        "Revenue"
    ]
    .sum()

    /
    total_revenue

    * 100
)


top_5_share = (

    country_sorted
    .head(
        min(
            5,
            len(
                country_sorted
            )
        )
    )[
        "Revenue"
    ]
    .sum()

    /
    total_revenue

    * 100
)


top_10_share = (

    country_sorted
    .head(
        min(
            10,
            len(
                country_sorted
            )
        )
    )[
        "Revenue"
    ]
    .sum()

    /
    total_revenue

    * 100
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "Top Market Revenue Share",
        f"{top_1_share:.1f}%"
    )


with c2:

    st.metric(
        "Top 5 Markets Revenue Share",
        f"{top_5_share:.1f}%"
    )


with c3:

    st.metric(
        "Top 10 Markets Revenue Share",
        f"{top_10_share:.1f}%"
    )


st.caption(
    "These measures quantify the degree to which "
    "revenue depends on a relatively small number "
    "of geographic markets."
)


st.divider()


# ============================================================
# 17. UK VS INTERNATIONAL
# ============================================================

st.subheader(
    "Domestic vs International Performance"
)


uk_mask = (

    country_df[
        "Country"
    ]
    .astype(str)
    .str.strip()
    .str.lower()
    .eq(
        "united kingdom"
    )
)


uk_revenue = (

    country_df.loc[
        uk_mask,
        "Revenue"
    ]
    .sum()
)


international_revenue = (

    country_df.loc[
        ~uk_mask,
        "Revenue"
    ]
    .sum()
)


comparison_df = pd.DataFrame(
    {
        "Market": [
            "United Kingdom",
            "International"
        ],

        "Revenue": [
            uk_revenue,
            international_revenue
        ]
    }
)


comparison_df[
    "RevenueShare"
] = (

    comparison_df[
        "Revenue"
    ]

    /

    comparison_df[
        "Revenue"
    ].sum()

    * 100
)


left, right = st.columns(
    [2, 1]
)


with left:

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )


    sns.barplot(
        data=comparison_df,
        x="Market",
        y="Revenue",
        ax=ax
    )


    ax.set_title(
        "UK vs International Revenue"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylabel(
        "Revenue (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


with right:

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# 18. COUNTRY EXPLORER
# ============================================================

st.subheader(
    "Country Explorer"
)


country_options = (

    country_df[
        "Country"
    ]

    .dropna()

    .sort_values()

    .unique()

    .tolist()
)


selected_country = st.selectbox(
    "Select a country",
    country_options
)


country_result = (

    country_df[
        country_df[
            "Country"
        ]
        ==
        selected_country
    ]
)


if not country_result.empty:

    selected_revenue = (
        country_result[
            "Revenue"
        ]
        .iloc[0]
    )


    country_revenue_share = (

        selected_revenue
        /
        total_revenue
        * 100
    )


    explorer1, explorer2 = (
        st.columns(2)
    )


    with explorer1:

        st.metric(
            "Country Revenue",
            f"£{selected_revenue:,.2f}"
        )


    with explorer2:

        st.metric(
            "Share of Total Revenue",
            f"{country_revenue_share:.2f}%"
        )


    st.dataframe(
        country_result,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 19. COUNTRY PERFORMANCE TABLE
# ============================================================

st.divider()


with st.expander(
    "Explore Complete Country Performance Dataset"
):

    st.dataframe(
        country_df.sort_values(
            "Revenue",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 20. FOOTER
# ============================================================

st.divider()


st.caption(
    "Geographic Analytics | "
    "UK Retail Customer Analytics"
)