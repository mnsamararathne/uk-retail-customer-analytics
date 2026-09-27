# ============================================================
# CANCELLATION ANALYSIS
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

    transaction_df = load_csv(
        "transaction_segments.csv"
    )

except Exception as error:

    st.error(
        "Cancellation analysis data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 4. DATA VALIDATION
# ============================================================

required_columns = [
    "InvoiceNo",
    "InvoiceDate",
    "StockCode",
    "Quantity",
    "Country",
    "IsCancellation"
]


missing_columns = [
    column
    for column in required_columns
    if column not in transaction_df.columns
]


if missing_columns:

    st.error(
        "Required cancellation-analysis columns are missing: "
        + ", ".join(missing_columns)
    )

    st.stop()


# ============================================================
# 5. PREPARE DATA
# ============================================================

transaction_df = transaction_df.copy()


transaction_df["InvoiceDate"] = pd.to_datetime(
    transaction_df["InvoiceDate"],
    errors="coerce"
)


# ------------------------------------------------------------
# Create Revenue if necessary
# ------------------------------------------------------------

if "Revenue" not in transaction_df.columns:

    if "UnitPrice" in transaction_df.columns:

        transaction_df["Revenue"] = (
            transaction_df["Quantity"]
            *
            transaction_df["UnitPrice"]
        )

    else:

        transaction_df["Revenue"] = np.nan


# ------------------------------------------------------------
# Create temporal variables if necessary
# ------------------------------------------------------------

if "YearMonth" not in transaction_df.columns:

    transaction_df["YearMonth"] = (
        transaction_df["InvoiceDate"]
        .dt.to_period("M")
        .astype(str)
    )


if "DayOfWeek" not in transaction_df.columns:

    transaction_df["DayOfWeek"] = (
        transaction_df["InvoiceDate"]
        .dt.day_name()
    )


# ------------------------------------------------------------
# Split normal and cancelled transactions
# ------------------------------------------------------------

cancelled_df = (
    transaction_df[
        transaction_df["IsCancellation"] == 1
    ]
    .copy()
)


sales_df = (
    transaction_df[
        transaction_df["IsCancellation"] == 0
    ]
    .copy()
)


# Absolute value is useful when describing cancelled value
# because cancellation transaction revenue may be negative.

cancelled_df["CancellationValue"] = (
    cancelled_df["Revenue"].abs()
)


cancelled_df["CancelledUnits"] = (
    cancelled_df["Quantity"].abs()
)


# ============================================================
# 6. PAGE HEADER
# ============================================================

st.title(
    "↩️ Cancellation Analysis"
)

st.caption(
    "Analysis of cancelled transactions, cancelled value, "
    "affected products and geographic patterns."
)

st.divider()


# ============================================================
# 7. CANCELLATION KPIs
# ============================================================

total_invoices = (
    transaction_df["InvoiceNo"]
    .nunique()
)


cancelled_invoices = (
    cancelled_df["InvoiceNo"]
    .nunique()
)


sales_invoices = (
    sales_df["InvoiceNo"]
    .nunique()
)


invoice_cancellation_rate = (
    cancelled_invoices
    /
    total_invoices
    * 100

    if total_invoices > 0
    else 0
)


cancelled_value = (
    cancelled_df["CancellationValue"]
    .sum()
)


cancelled_units = (
    cancelled_df["CancelledUnits"]
    .sum()
)


affected_products = (
    cancelled_df["StockCode"]
    .nunique()
)


kpi1, kpi2, kpi3 = st.columns(3)


with kpi1:

    st.metric(
        "Cancelled Invoices",
        f"{cancelled_invoices:,.0f}"
    )


with kpi2:

    st.metric(
        "Invoice Cancellation Rate",
        f"{invoice_cancellation_rate:.2f}%"
    )


with kpi3:

    st.metric(
        "Cancelled Value",
        f"£{cancelled_value:,.0f}"
    )


kpi4, kpi5, kpi6 = st.columns(3)


with kpi4:

    st.metric(
        "Cancelled Units",
        f"{cancelled_units:,.0f}"
    )


with kpi5:

    st.metric(
        "Affected Products",
        f"{affected_products:,.0f}"
    )


with kpi6:

    st.metric(
        "Completed / Non-Cancelled Invoices",
        f"{sales_invoices:,.0f}"
    )


st.caption(
    "Cancellation value is shown as an absolute magnitude "
    "to make the commercial impact easier to interpret."
)


st.divider()


# ============================================================
# 8. MONTHLY CANCELLATION TREND
# ============================================================

st.subheader(
    "Cancellation Trend"
)


monthly_cancellations = (

    cancelled_df

    .groupby(
        "YearMonth",
        as_index=False
    )

    .agg(
        CancelledInvoices=(
            "InvoiceNo",
            "nunique"
        ),

        CancelledValue=(
            "CancellationValue",
            "sum"
        ),

        CancelledUnits=(
            "CancelledUnits",
            "sum"
        )
    )

    .sort_values(
        "YearMonth"
    )
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Cancelled invoices
# ------------------------------------------------------------

with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=monthly_cancellations,
        x="YearMonth",
        y="CancelledInvoices",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Monthly Cancelled Invoices"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Cancelled Invoices"
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
# Cancelled value
# ------------------------------------------------------------

with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.lineplot(
        data=monthly_cancellations,
        x="YearMonth",
        y="CancelledValue",
        marker="o",
        ax=ax
    )


    ax.set_title(
        "Monthly Cancelled Value"
    )

    ax.set_xlabel(
        "Month"
    )

    ax.set_ylabel(
        "Cancelled Value (£)"
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
# 9. CANCELLATION RATE BY MONTH
# ============================================================

st.subheader(
    "Monthly Cancellation Rate"
)


monthly_all_invoices = (

    transaction_df

    .groupby(
        "YearMonth"
    )["InvoiceNo"]

    .nunique()

    .rename(
        "TotalInvoices"
    )
)


monthly_cancelled_invoices = (

    cancelled_df

    .groupby(
        "YearMonth"
    )["InvoiceNo"]

    .nunique()

    .rename(
        "CancelledInvoices"
    )
)


monthly_rate = (

    pd.concat(
        [
            monthly_all_invoices,
            monthly_cancelled_invoices
        ],
        axis=1
    )

    .fillna(0)

    .reset_index()
)


monthly_rate[
    "CancellationRate"
] = np.where(

    monthly_rate[
        "TotalInvoices"
    ] > 0,

    monthly_rate[
        "CancelledInvoices"
    ]
    /
    monthly_rate[
        "TotalInvoices"
    ]
    * 100,

    0
)


fig, ax = plt.subplots(
    figsize=(12, 5)
)


sns.barplot(
    data=monthly_rate,
    x="YearMonth",
    y="CancellationRate",
    ax=ax
)


ax.set_title(
    "Invoice Cancellation Rate by Month"
)

ax.set_xlabel(
    "Month"
)

ax.set_ylabel(
    "Cancellation Rate (%)"
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
# 10. CANCELLATIONS BY DAY OF WEEK
# ============================================================

st.subheader(
    "Weekly Cancellation Pattern"
)


weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]


weekday_cancellations = (

    cancelled_df

    .groupby(
        "DayOfWeek",
        as_index=False
    )

    .agg(
        CancelledInvoices=(
            "InvoiceNo",
            "nunique"
        ),

        CancelledValue=(
            "CancellationValue",
            "sum"
        )
    )
)


weekday_cancellations[
    "DayOfWeek"
] = pd.Categorical(

    weekday_cancellations[
        "DayOfWeek"
    ],

    categories=weekday_order,

    ordered=True
)


weekday_cancellations = (
    weekday_cancellations
    .sort_values(
        "DayOfWeek"
    )
)


left, right = st.columns(2)


with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=weekday_cancellations,
        x="DayOfWeek",
        y="CancelledInvoices",
        ax=ax
    )


    ax.set_title(
        "Cancelled Invoices by Day"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylabel(
        "Cancelled Invoices"
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


with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=weekday_cancellations,
        x="DayOfWeek",
        y="CancelledValue",
        ax=ax
    )


    ax.set_title(
        "Cancelled Value by Day"
    )

    ax.set_xlabel(
        ""
    )

    ax.set_ylabel(
        "Cancelled Value (£)"
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
# 11. PRODUCTS MOST AFFECTED
# ============================================================

st.subheader(
    "Products Most Affected by Cancellations"
)


product_group_columns = [
    "StockCode"
]


if "Description" in cancelled_df.columns:

    product_group_columns.append(
        "Description"
    )


cancelled_products = (

    cancelled_df

    .groupby(
        product_group_columns,
        as_index=False,
        dropna=False
    )

    .agg(
        CancelledInvoices=(
            "InvoiceNo",
            "nunique"
        ),

        CancelledUnits=(
            "CancelledUnits",
            "sum"
        ),

        CancelledValue=(
            "CancellationValue",
            "sum"
        )
    )
)


if "Description" in cancelled_products.columns:

    cancelled_products[
        "ProductLabel"
    ] = (

        cancelled_products[
            "Description"
        ]

        .fillna(
            cancelled_products[
                "StockCode"
            ].astype(str)
        )

        .astype(str)

        .str.slice(
            0,
            45
        )
    )

else:

    cancelled_products[
        "ProductLabel"
    ] = (

        cancelled_products[
            "StockCode"
        ]
        .astype(str)
    )


top_n_products = st.slider(
    "Number of affected products to display",
    min_value=5,
    max_value=30,
    value=10,
    step=5
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Products by cancelled value
# ------------------------------------------------------------

with left:

    top_cancel_value_products = (

        cancelled_products

        .nlargest(
            top_n_products,
            "CancelledValue"
        )

        .sort_values(
            "CancelledValue",
            ascending=True
        )
    )


    fig, ax = plt.subplots(
        figsize=(9, 7)
    )


    sns.barplot(
        data=top_cancel_value_products,
        x="CancelledValue",
        y="ProductLabel",
        ax=ax
    )


    ax.set_title(
        "Products by Cancelled Value"
    )

    ax.set_xlabel(
        "Cancelled Value (£)"
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


# ------------------------------------------------------------
# Products by cancelled units
# ------------------------------------------------------------

with right:

    top_cancel_unit_products = (

        cancelled_products

        .nlargest(
            top_n_products,
            "CancelledUnits"
        )

        .sort_values(
            "CancelledUnits",
            ascending=True
        )
    )


    fig, ax = plt.subplots(
        figsize=(9, 7)
    )


    sns.barplot(
        data=top_cancel_unit_products,
        x="CancelledUnits",
        y="ProductLabel",
        ax=ax
    )


    ax.set_title(
        "Products by Cancelled Units"
    )

    ax.set_xlabel(
        "Cancelled Units"
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
# 12. COUNTRIES MOST AFFECTED
# ============================================================

st.subheader(
    "Geographic Cancellation Patterns"
)


cancelled_countries = (

    cancelled_df

    .groupby(
        "Country",
        as_index=False
    )

    .agg(
        CancelledInvoices=(
            "InvoiceNo",
            "nunique"
        ),

        CancelledUnits=(
            "CancelledUnits",
            "sum"
        ),

        CancelledValue=(
            "CancellationValue",
            "sum"
        )
    )
)


top_cancelled_countries = (

    cancelled_countries

    .nlargest(
        min(
            10,
            len(
                cancelled_countries
            )
        ),
        "CancelledValue"
    )

    .sort_values(
        "CancelledValue",
        ascending=True
    )
)


fig, ax = plt.subplots(
    figsize=(11, 6)
)


sns.barplot(
    data=top_cancelled_countries,
    x="CancelledValue",
    y="Country",
    ax=ax
)


ax.set_title(
    "Countries with Highest Cancelled Value"
)

ax.set_xlabel(
    "Cancelled Value (£)"
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


st.caption(
    "Absolute cancellation volume should be interpreted "
    "alongside market size. A large market may naturally "
    "generate more cancellations simply because it processes "
    "more transactions."
)


st.divider()


# ============================================================
# 13. COUNTRY CANCELLATION RATES
# ============================================================

st.subheader(
    "Cancellation Rate by Country"
)


country_total_invoices = (

    transaction_df

    .groupby(
        "Country"
    )["InvoiceNo"]

    .nunique()

    .rename(
        "TotalInvoices"
    )
)


country_cancelled_invoices = (

    cancelled_df

    .groupby(
        "Country"
    )["InvoiceNo"]

    .nunique()

    .rename(
        "CancelledInvoices"
    )
)


country_rates = (

    pd.concat(
        [
            country_total_invoices,
            country_cancelled_invoices
        ],
        axis=1
    )

    .fillna(0)

    .reset_index()
)


country_rates[
    "CancellationRate"
] = np.where(

    country_rates[
        "TotalInvoices"
    ] > 0,

    country_rates[
        "CancelledInvoices"
    ]
    /
    country_rates[
        "TotalInvoices"
    ]
    * 100,

    0
)


# Avoid overinterpreting countries with tiny samples.

minimum_invoices = st.slider(
    "Minimum invoices required for country-rate comparison",
    min_value=1,
    max_value=100,
    value=20,
    step=5
)


eligible_country_rates = (

    country_rates[
        country_rates[
            "TotalInvoices"
        ]
        >=
        minimum_invoices
    ]

    .nlargest(
        min(
            15,
            len(
                country_rates
            )
        ),
        "CancellationRate"
    )

    .sort_values(
        "CancellationRate",
        ascending=True
    )
)


if not eligible_country_rates.empty:

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )


    sns.barplot(
        data=eligible_country_rates,
        x="CancellationRate",
        y="Country",
        ax=ax
    )


    ax.set_title(
        "Highest Invoice Cancellation Rates by Country"
    )

    ax.set_xlabel(
        "Cancellation Rate (%)"
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
        "No countries meet the selected minimum "
        "invoice threshold."
    )


st.caption(
    "The minimum-invoice threshold reduces misleading "
    "comparisons caused by very small country samples."
)


st.divider()


# ============================================================
# 14. CANCELLATION VALUE DISTRIBUTION
# ============================================================

st.subheader(
    "Cancellation Value Distribution"
)


invoice_cancellation_values = (

    cancelled_df

    .groupby(
        "InvoiceNo",
        as_index=False
    )

    .agg(
        CancellationValue=(
            "CancellationValue",
            "sum"
        ),

        CancelledUnits=(
            "CancelledUnits",
            "sum"
        )
    )
)


left, right = st.columns(2)


with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.histplot(
        data=invoice_cancellation_values,
        x="CancellationValue",
        bins=40,
        kde=True,
        ax=ax
    )


    ax.set_title(
        "Distribution of Cancellation Value per Invoice"
    )

    ax.set_xlabel(
        "Cancellation Value (£)"
    )

    ax.set_ylabel(
        "Cancelled Invoices"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


with right:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.boxplot(
        data=invoice_cancellation_values,
        x="CancellationValue",
        ax=ax
    )


    ax.set_title(
        "Cancellation Value and Outliers"
    )

    ax.set_xlabel(
        "Cancellation Value (£)"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 15. CANCELLATION CONCENTRATION
# ============================================================

st.subheader(
    "Cancellation Value Concentration"
)


cancellation_sorted = (

    invoice_cancellation_values

    .sort_values(
        "CancellationValue",
        ascending=False
    )

    .reset_index(
        drop=True
    )
)


if (
    not cancellation_sorted.empty
    and
    cancellation_sorted[
        "CancellationValue"
    ].sum() > 0
):

    cancellation_sorted[
        "CumulativeValue"
    ] = (

        cancellation_sorted[
            "CancellationValue"
        ]
        .cumsum()
    )


    cancellation_sorted[
        "CumulativeValuePct"
    ] = (

        cancellation_sorted[
            "CumulativeValue"
        ]

        /

        cancellation_sorted[
            "CancellationValue"
        ].sum()

        * 100
    )


    cancellation_sorted[
        "CumulativeInvoicePct"
    ] = (

        np.arange(
            1,
            len(
                cancellation_sorted
            ) + 1
        )

        /

        len(
            cancellation_sorted
        )

        * 100
    )


    fig, ax = plt.subplots(
        figsize=(11, 6)
    )


    ax.plot(
        cancellation_sorted[
            "CumulativeInvoicePct"
        ],
        cancellation_sorted[
            "CumulativeValuePct"
        ],
        linewidth=2
    )


    ax.axvline(
        20,
        linestyle="--",
        label="Top 20% of Cancelled Invoices"
    )


    ax.axhline(
        80,
        linestyle="--",
        label="80% of Cancelled Value"
    )


    ax.set_title(
        "Cancellation Value Concentration Curve"
    )

    ax.set_xlabel(
        "Cumulative Cancelled Invoices (%)"
    )

    ax.set_ylabel(
        "Cumulative Cancelled Value (%)"
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


st.divider()


# ============================================================
# 16. KEY CANCELLATION FINDINGS
# ============================================================

st.subheader(
    "Cancellation Summary"
)


if not cancelled_df.empty:

    peak_month_row = (

        monthly_cancellations

        .loc[
            monthly_cancellations[
                "CancelledValue"
            ].idxmax()
        ]
    )


    most_affected_product = (

        cancelled_products

        .loc[
            cancelled_products[
                "CancelledValue"
            ].idxmax()
        ]
    )


    most_affected_country = (

        cancelled_countries

        .loc[
            cancelled_countries[
                "CancelledValue"
            ].idxmax()
        ]
    )


    insight1, insight2, insight3 = (
        st.columns(3)
    )


    with insight1:

        with st.container(
            border=True
        ):

            st.markdown(
                "**Peak Cancellation Month**"
            )

            st.write(
                peak_month_row[
                    "YearMonth"
                ]
            )

            st.caption(
                f"£{peak_month_row['CancelledValue']:,.0f} "
                "in cancelled value."
            )


    with insight2:

        with st.container(
            border=True
        ):

            st.markdown(
                "**Most Affected Product**"
            )

            st.write(
                most_affected_product[
                    "ProductLabel"
                ]
            )

            st.caption(
                f"£{most_affected_product['CancelledValue']:,.0f} "
                "in cancelled value."
            )


    with insight3:

        with st.container(
            border=True
        ):

            st.markdown(
                "**Highest Cancelled-Value Market**"
            )

            st.write(
                most_affected_country[
                    "Country"
                ]
            )

            st.caption(
                f"£{most_affected_country['CancelledValue']:,.0f} "
                "in cancelled value."
            )


st.info(
    "These patterns identify where cancellations are concentrated, "
    "but transaction data alone does not establish why customers "
    "cancelled. Operational or customer-service data would be "
    "needed to investigate underlying causes."
)


st.divider()


# ============================================================
# 17. CANCELLATION DATA EXPLORER
# ============================================================

with st.expander(
    "Explore Cancellation Data"
):

    display_columns = [
        "InvoiceNo",
        "InvoiceDate",
        "CustomerID",
        "StockCode",
        "Description",
        "Quantity",
        "UnitPrice",
        "Revenue",
        "CancellationValue",
        "Country"
    ]


    display_columns = [
        column
        for column in display_columns
        if column in cancelled_df.columns
    ]


    st.dataframe(
        cancelled_df[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 18. FOOTER
# ============================================================

st.divider()


st.caption(
    "Cancellation Analysis | "
    "UK Retail Customer Analytics"
)