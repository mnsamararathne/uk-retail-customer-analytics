# ============================================================
# EXECUTIVE OVERVIEW
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================

# This page provides a high-level executive summary of the
# retail dataset. Detailed analysis is available through the
# dedicated analytical pages in the Streamlit application.


# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from utils.data_loader import load_csv

from utils.styles import (
    page_header,
    section_header,
    metric_row,
    dashboard_footer
)

from utils.formatters import (
    format_currency,
    format_number,
    format_percentage
)

from utils.charts import (
    horizontal_bar_chart,
    line_chart,
    close_chart
)


# ============================================================
# 2. LOAD DASHBOARD DATA
# ============================================================

try:

    monthly_df = load_csv(
        "monthly_performance.csv"
    )

    customer_df = load_csv(
        "customer_performance.csv"
    )

    product_df = load_csv(
        "product_performance.csv"
    )

    country_df = load_csv(
        "country_performance.csv"
    )

    transaction_df = load_csv(
        "transaction_segments.csv"
    )

except Exception as error:

    st.error(
        "The Executive Overview data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 3. PREPARE DATA
# ============================================================

transaction_df = transaction_df.copy()
monthly_df = monthly_df.copy()
customer_df = customer_df.copy()
product_df = product_df.copy()
country_df = country_df.copy()


# ------------------------------------------------------------
# Invoice Date
# ------------------------------------------------------------

if "InvoiceDate" in transaction_df.columns:

    transaction_df["InvoiceDate"] = pd.to_datetime(
        transaction_df["InvoiceDate"],
        errors="coerce"
    )


# ------------------------------------------------------------
# Revenue
# ------------------------------------------------------------

if "Revenue" not in transaction_df.columns:

    if (
        "Quantity" in transaction_df.columns
        and
        "UnitPrice" in transaction_df.columns
    ):

        transaction_df["Revenue"] = (
            transaction_df["Quantity"]
            *
            transaction_df["UnitPrice"]
        )


# ------------------------------------------------------------
# Identify sales transactions
# ------------------------------------------------------------

if "IsCancellation" in transaction_df.columns:

    sales_df = (
        transaction_df[
            transaction_df["IsCancellation"] == 0
        ]
        .copy()
    )

else:

    sales_df = transaction_df.copy()


# ------------------------------------------------------------
# Monthly Date
# ------------------------------------------------------------

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
# 4. PAGE HEADER
# ============================================================

page_header(
    title="🏠 Executive Overview",
    description=(
        "Executive-level view of sales performance, customer "
        "behaviour, product performance and geographic activity "
        "within the UK Online Retail dataset."
    )
)


# ============================================================
# 5. DATA SCOPE
# ============================================================

date_start = None
date_end = None


if "InvoiceDate" in transaction_df.columns:

    valid_dates = (
        transaction_df["InvoiceDate"]
        .dropna()
    )

    if not valid_dates.empty:

        date_start = valid_dates.min()
        date_end = valid_dates.max()


if (
    date_start is not None
    and
    date_end is not None
):

    st.caption(
        f"Data period: "
        f"**{date_start.strftime('%d %b %Y')}** "
        f"to "
        f"**{date_end.strftime('%d %b %Y')}**"
    )


# ============================================================
# 6. CORE BUSINESS KPIs
# ============================================================

section_header(
    "Business Performance",
    "Core indicators summarising the analysed retail activity."
)


# ------------------------------------------------------------
# Total Revenue
# ------------------------------------------------------------

if "Revenue" in sales_df.columns:

    total_revenue = (
        sales_df["Revenue"]
        .sum()
    )

elif "Revenue" in monthly_df.columns:

    total_revenue = (
        monthly_df["Revenue"]
        .sum()
    )

else:

    total_revenue = 0


# ------------------------------------------------------------
# Total Orders
# ------------------------------------------------------------

if "InvoiceNo" in sales_df.columns:

    total_orders = (
        sales_df["InvoiceNo"]
        .nunique()
    )

elif "Orders" in monthly_df.columns:

    total_orders = (
        monthly_df["Orders"]
        .sum()
    )

else:

    total_orders = 0


# ------------------------------------------------------------
# Total Customers
# ------------------------------------------------------------

if "CustomerID" in sales_df.columns:

    total_customers = (
        sales_df["CustomerID"]
        .nunique()
    )

elif "CustomerID" in customer_df.columns:

    total_customers = (
        customer_df["CustomerID"]
        .nunique()
    )

else:

    total_customers = 0


# ------------------------------------------------------------
# Average Order Value
# ------------------------------------------------------------

average_order_value = (

    total_revenue
    /
    total_orders

    if total_orders > 0

    else 0
)


# ------------------------------------------------------------
# Display KPI row
# ------------------------------------------------------------

metric_row([
    (
        "Revenue",
        format_currency(
            total_revenue
        )
    ),

    (
        "Orders",
        format_number(
            total_orders
        )
    ),

    (
        "Customers",
        format_number(
            total_customers
        )
    ),

    (
        "Average Order Value",
        format_currency(
            average_order_value
        )
    )
])


st.divider()


# ============================================================
# 7. SECONDARY KPIs
# ============================================================

# ------------------------------------------------------------
# Units Sold
# ------------------------------------------------------------

if "Quantity" in sales_df.columns:

    total_units = (
        sales_df["Quantity"]
        .sum()
    )

else:

    total_units = 0


# ------------------------------------------------------------
# Products
# ------------------------------------------------------------

if "StockCode" in sales_df.columns:

    total_products = (
        sales_df["StockCode"]
        .nunique()
    )

elif "StockCode" in product_df.columns:

    total_products = (
        product_df["StockCode"]
        .nunique()
    )

else:

    total_products = 0


# ------------------------------------------------------------
# Countries
# ------------------------------------------------------------

if "Country" in sales_df.columns:

    total_countries = (
        sales_df["Country"]
        .nunique()
    )

elif "Country" in country_df.columns:

    total_countries = (
        country_df["Country"]
        .nunique()
    )

else:

    total_countries = 0


# ------------------------------------------------------------
# Revenue per Customer
# ------------------------------------------------------------

revenue_per_customer = (

    total_revenue
    /
    total_customers

    if total_customers > 0

    else 0
)


metric_row([
    (
        "Units Sold",
        format_number(
            total_units
        )
    ),

    (
        "Products",
        format_number(
            total_products
        )
    ),

    (
        "Countries",
        format_number(
            total_countries
        )
    ),

    (
        "Revenue / Customer",
        format_currency(
            revenue_per_customer
        )
    )
])


st.divider()


# ============================================================
# 8. MONTHLY SALES PERFORMANCE
# ============================================================

section_header(
    "Sales Performance",
    (
        "Revenue and order trends across the available "
        "transaction period."
    )
)


left, right = st.columns(2)


# ------------------------------------------------------------
# Revenue Trend
# ------------------------------------------------------------

with left:

    if (
        "YearMonth" in monthly_df.columns
        and
        "Revenue" in monthly_df.columns
    ):

        fig, ax = line_chart(
            data=monthly_df,
            x="YearMonth",
            y="Revenue",
            title="Monthly Revenue",
            xlabel="Month",
            ylabel="Revenue (£)",
            figsize=(9, 5)
        )


        ax.tick_params(
            axis="x",
            rotation=45
        )


        st.pyplot(
            fig,
            use_container_width=True
        )


        close_chart(fig)


    else:

        st.info(
            "Monthly revenue data is unavailable."
        )


# ------------------------------------------------------------
# Order Trend
# ------------------------------------------------------------

with right:

    if (
        "YearMonth" in monthly_df.columns
        and
        "Orders" in monthly_df.columns
    ):

        fig, ax = line_chart(
            data=monthly_df,
            x="YearMonth",
            y="Orders",
            title="Monthly Orders",
            xlabel="Month",
            ylabel="Orders",
            figsize=(9, 5)
        )


        ax.tick_params(
            axis="x",
            rotation=45
        )


        st.pyplot(
            fig,
            use_container_width=True
        )


        close_chart(fig)


    else:

        st.info(
            "Monthly order data is unavailable."
        )


# ============================================================
# 9. SALES TREND SUMMARY
# ============================================================

if (
    "Revenue" in monthly_df.columns
    and
    not monthly_df.empty
):

    highest_month_row = (
        monthly_df.loc[
            monthly_df["Revenue"].idxmax()
        ]
    )


    highest_month = (
        highest_month_row["YearMonth"]
        if "YearMonth" in highest_month_row.index
        else "N/A"
    )


    highest_month_revenue = (
        highest_month_row["Revenue"]
    )


    avg_monthly_revenue = (
        monthly_df["Revenue"]
        .mean()
    )


    insight1, insight2 = st.columns(2)


    with insight1:

        with st.container(
            border=True
        ):

            st.markdown(
                "##### Peak Revenue Month"
            )

            st.metric(
                str(highest_month),
                format_currency(
                    highest_month_revenue
                )
            )


    with insight2:

        with st.container(
            border=True
        ):

            st.markdown(
                "##### Average Monthly Revenue"
            )

            st.metric(
                "Monthly Average",
                format_currency(
                    avg_monthly_revenue
                )
            )


st.divider()


# ============================================================
# 10. CUSTOMER INTELLIGENCE
# ============================================================

section_header(
    "Customer Intelligence",
    (
        "High-level indicators of customer value "
        "and revenue concentration."
    )
)


customer_revenue_column = None


for candidate in [
    "TotalRevenue",
    "Revenue"
]:

    if candidate in customer_df.columns:

        customer_revenue_column = candidate
        break


left, right = st.columns(2)


# ------------------------------------------------------------
# Top Customers
# ------------------------------------------------------------

with left:

    if customer_revenue_column is not None:

        top_customers = (
            customer_df
            .nlargest(
                10,
                customer_revenue_column
            )
            .copy()
        )


        if "CustomerID" in top_customers.columns:

            top_customers[
                "CustomerLabel"
            ] = (
                top_customers[
                    "CustomerID"
                ]
                .astype(str)
            )


            top_customers = (
                top_customers
                .sort_values(
                    customer_revenue_column,
                    ascending=True
                )
            )


            fig, ax = horizontal_bar_chart(
                data=top_customers,
                x=customer_revenue_column,
                y="CustomerLabel",
                title="Top 10 Customers by Revenue",
                xlabel="Revenue (£)",
                ylabel="Customer ID",
                figsize=(9, 6)
            )


            st.pyplot(
                fig,
                use_container_width=True
            )


            close_chart(fig)


        else:

            st.info(
                "Customer identifiers are unavailable."
            )


    else:

        st.info(
            "Customer revenue data is unavailable."
        )


# ------------------------------------------------------------
# Customer Revenue Concentration
# ------------------------------------------------------------

with right:

    if (
        customer_revenue_column is not None
        and
        not customer_df.empty
    ):

        customer_sorted = (
            customer_df
            .sort_values(
                customer_revenue_column,
                ascending=False
            )
            .reset_index(drop=True)
        )


        customer_total_revenue = (
            customer_sorted[
                customer_revenue_column
            ]
            .sum()
        )


        if customer_total_revenue > 0:

            customer_sorted[
                "CumulativeRevenuePct"
            ] = (
                customer_sorted[
                    customer_revenue_column
                ]
                .cumsum()
                /
                customer_total_revenue
                * 100
            )


            customer_sorted[
                "CumulativeCustomerPct"
            ] = (
                np.arange(
                    1,
                    len(customer_sorted) + 1
                )
                /
                len(customer_sorted)
                * 100
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            ax.plot(
                customer_sorted[
                    "CumulativeCustomerPct"
                ],
                customer_sorted[
                    "CumulativeRevenuePct"
                ],
                linewidth=2
            )


            ax.axvline(
                20,
                linestyle="--",
                alpha=0.7,
                label="Top 20% Customers"
            )


            ax.axhline(
                80,
                linestyle="--",
                alpha=0.7,
                label="80% Revenue"
            )


            ax.set_title(
                "Customer Revenue Concentration",
                loc="left"
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

            st.info(
                "Customer revenue is unavailable."
            )


st.divider()


# ============================================================
# 11. PRODUCT INTELLIGENCE
# ============================================================

section_header(
    "Product Intelligence",
    (
        "Products generating the highest revenue and "
        "their contribution to overall commercial performance."
    )
)


product_revenue_column = None


for candidate in [
    "TotalRevenue",
    "Revenue"
]:

    if candidate in product_df.columns:

        product_revenue_column = candidate
        break


if "Description" in product_df.columns:

    product_df[
        "ProductLabel"
    ] = (
        product_df[
            "Description"
        ]
        .fillna(
            product_df[
                "StockCode"
            ].astype(str)
        )
        .astype(str)
        .str.slice(
            0,
            40
        )
    )

elif "StockCode" in product_df.columns:

    product_df[
        "ProductLabel"
    ] = (
        product_df[
            "StockCode"
        ]
        .astype(str)
    )


left, right = st.columns(2)


# ------------------------------------------------------------
# Top Products
# ------------------------------------------------------------

with left:

    if (
        product_revenue_column is not None
        and
        "ProductLabel" in product_df.columns
    ):

        top_products = (
            product_df
            .nlargest(
                10,
                product_revenue_column
            )
            .sort_values(
                product_revenue_column,
                ascending=True
            )
        )


        fig, ax = horizontal_bar_chart(
            data=top_products,
            x=product_revenue_column,
            y="ProductLabel",
            title="Top 10 Products by Revenue",
            xlabel="Revenue (£)",
            ylabel="Product",
            figsize=(9, 6)
        )


        st.pyplot(
            fig,
            use_container_width=True
        )


        close_chart(fig)


    else:

        st.info(
            "Product revenue data is unavailable."
        )


# ------------------------------------------------------------
# Product Revenue Concentration
# ------------------------------------------------------------

with right:

    if (
        product_revenue_column is not None
        and
        not product_df.empty
    ):

        product_sorted = (
            product_df
            .sort_values(
                product_revenue_column,
                ascending=False
            )
            .reset_index(drop=True)
        )


        product_total_revenue = (
            product_sorted[
                product_revenue_column
            ]
            .sum()
        )


        if product_total_revenue > 0:

            product_sorted[
                "CumulativeRevenuePct"
            ] = (
                product_sorted[
                    product_revenue_column
                ]
                .cumsum()
                /
                product_total_revenue
                * 100
            )


            product_sorted[
                "CumulativeProductPct"
            ] = (
                np.arange(
                    1,
                    len(product_sorted) + 1
                )
                /
                len(product_sorted)
                * 100
            )


            fig, ax = plt.subplots(
                figsize=(9, 6)
            )


            ax.plot(
                product_sorted[
                    "CumulativeProductPct"
                ],
                product_sorted[
                    "CumulativeRevenuePct"
                ],
                linewidth=2
            )


            ax.axvline(
                20,
                linestyle="--",
                alpha=0.7,
                label="Top 20% Products"
            )


            ax.axhline(
                80,
                linestyle="--",
                alpha=0.7,
                label="80% Revenue"
            )


            ax.set_title(
                "Product Revenue Concentration",
                loc="left"
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

            st.info(
                "Product revenue is unavailable."
            )


st.divider()


# ============================================================
# 12. GEOGRAPHIC INTELLIGENCE
# ============================================================

section_header(
    "Geographic Intelligence",
    (
        "Comparison of the markets contributing most "
        "strongly to retail revenue."
    )
)


country_revenue_column = None


for candidate in [
    "Revenue",
    "TotalRevenue"
]:

    if candidate in country_df.columns:

        country_revenue_column = candidate
        break


if (
    country_revenue_column is not None
    and
    "Country" in country_df.columns
):

    top_countries = (
        country_df
        .nlargest(
            min(
                10,
                len(country_df)
            ),
            country_revenue_column
        )
        .sort_values(
            country_revenue_column,
            ascending=True
        )
    )


    fig, ax = horizontal_bar_chart(
        data=top_countries,
        x=country_revenue_column,
        y="Country",
        title="Top Markets by Revenue",
        xlabel="Revenue (£)",
        ylabel="Country",
        figsize=(11, 6)
    )


    st.pyplot(
        fig,
        use_container_width=True
    )


    close_chart(fig)


else:

    st.info(
        "Country revenue data is unavailable."
    )


st.divider()


# ============================================================
# 13. CANCELLATION OVERVIEW
# ============================================================

section_header(
    "Cancellation Overview",
    (
        "High-level view of cancellation activity. "
        "Detailed investigation is available on the "
        "Cancellation Analysis page."
    )
)


if "IsCancellation" in transaction_df.columns:

    cancelled_df = (
        transaction_df[
            transaction_df[
                "IsCancellation"
            ] == 1
        ]
        .copy()
    )


    total_invoice_count = (
        transaction_df[
            "InvoiceNo"
        ]
        .nunique()
    )


    cancelled_invoice_count = (
        cancelled_df[
            "InvoiceNo"
        ]
        .nunique()
    )


    cancellation_rate = (

        cancelled_invoice_count
        /
        total_invoice_count
        * 100

        if total_invoice_count > 0

        else 0
    )


    if "Revenue" in cancelled_df.columns:

        cancelled_value = (
            cancelled_df[
                "Revenue"
            ]
            .abs()
            .sum()
        )

    else:

        cancelled_value = 0


    if "Quantity" in cancelled_df.columns:

        cancelled_units = (
            cancelled_df[
                "Quantity"
            ]
            .abs()
            .sum()
        )

    else:

        cancelled_units = 0


    metric_row([
        (
            "Cancelled Invoices",
            format_number(
                cancelled_invoice_count
            )
        ),

        (
            "Cancellation Rate",
            format_percentage(
                cancellation_rate,
                2
            )
        ),

        (
            "Cancelled Value",
            format_currency(
                cancelled_value
            )
        ),

        (
            "Cancelled Units",
            format_number(
                cancelled_units
            )
        )
    ])


else:

    st.info(
        "Cancellation indicators are unavailable."
    )


st.divider()


# ============================================================
# 14. EXECUTIVE BUSINESS INSIGHTS
# ============================================================

section_header(
    "Key Business Insights",
    (
        "Automatically generated observations from the "
        "analysed dashboard datasets."
    )
)


# ------------------------------------------------------------
# Calculate insight values
# ------------------------------------------------------------

insight_peak_month = None
insight_top_country = None
insight_top_product = None


# Peak month

if (
    "Revenue" in monthly_df.columns
    and
    "YearMonth" in monthly_df.columns
    and
    not monthly_df.empty
):

    peak_row = (
        monthly_df.loc[
            monthly_df[
                "Revenue"
            ].idxmax()
        ]
    )

    insight_peak_month = (
        peak_row["YearMonth"],
        peak_row["Revenue"]
    )


# Top country

if (
    country_revenue_column is not None
    and
    "Country" in country_df.columns
    and
    not country_df.empty
):

    country_row = (
        country_df.loc[
            country_df[
                country_revenue_column
            ].idxmax()
        ]
    )

    insight_top_country = (
        country_row["Country"],
        country_row[
            country_revenue_column
        ]
    )


# Top product

if (
    product_revenue_column is not None
    and
    "ProductLabel" in product_df.columns
    and
    not product_df.empty
):

    product_row = (
        product_df.loc[
            product_df[
                product_revenue_column
            ].idxmax()
        ]
    )

    insight_top_product = (
        product_row[
            "ProductLabel"
        ],
        product_row[
            product_revenue_column
        ]
    )


# ------------------------------------------------------------
# Display insights
# ------------------------------------------------------------

insight_columns = st.columns(3)


with insight_columns[0]:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### 📈 Peak Sales Period"
        )


        if insight_peak_month is not None:

            st.write(
                f"**{insight_peak_month[0]}** "
                "recorded the highest monthly revenue."
            )

            st.metric(
                "Peak Revenue",
                format_currency(
                    insight_peak_month[1]
                )
            )

        else:

            st.write(
                "Monthly revenue information "
                "is unavailable."
            )


with insight_columns[1]:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### 🌍 Largest Market"
        )


        if insight_top_country is not None:

            country_share = (

                insight_top_country[1]
                /
                country_df[
                    country_revenue_column
                ].sum()
                * 100

                if country_df[
                    country_revenue_column
                ].sum() > 0

                else 0
            )


            st.write(
                f"**{insight_top_country[0]}** "
                "generated the highest revenue."
            )

            st.metric(
                "Revenue Share",
                format_percentage(
                    country_share,
                    1
                )
            )

        else:

            st.write(
                "Geographic revenue information "
                "is unavailable."
            )


with insight_columns[2]:

    with st.container(
        border=True
    ):

        st.markdown(
            "#### 📦 Leading Product"
        )


        if insight_top_product is not None:

            st.write(
                f"**{insight_top_product[0]}** "
                "was the highest-revenue product."
            )

            st.metric(
                "Product Revenue",
                format_currency(
                    insight_top_product[1]
                )
            )

        else:

            st.write(
                "Product revenue information "
                "is unavailable."
            )


st.divider()


# ============================================================
# 15. DASHBOARD GUIDE
# ============================================================

section_header(
    "Explore the Analysis",
    (
        "Use the navigation panel to move from the executive "
        "summary into detailed analytical views."
    )
)


guide1, guide2, guide3 = st.columns(3)


with guide1:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 📈 Sales"
        )

        st.write(
            "Explore monthly revenue, orders, "
            "growth, weekday patterns and hourly "
            "purchasing behaviour."
        )


    with st.container(
        border=True
    ):

        st.markdown(
            "### 👥 Customers"
        )

        st.write(
            "Investigate customer value, purchasing "
            "frequency, revenue concentration and "
            "high-value customers."
        )


with guide2:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🎯 Segmentation"
        )

        st.write(
            "Explore RFM customer behaviour, "
            "K-Means clustering, cluster evaluation "
            "and PCA visualisation."
        )


    with st.container(
        border=True
    ):

        st.markdown(
            "### 📦 Products"
        )

        st.write(
            "Compare product revenue, demand, "
            "customer reach and revenue concentration."
        )


with guide3:

    with st.container(
        border=True
    ):

        st.markdown(
            "### 🌍 Geography"
        )

        st.write(
            "Compare country revenue, market size, "
            "customer value and geographic concentration."
        )


    with st.container(
        border=True
    ):

        st.markdown(
            "### ↩️ Cancellations"
        )

        st.write(
            "Investigate cancellation rates, value, "
            "products, countries and temporal patterns."
        )


# ============================================================
# 16. DATASET INFORMATION
# ============================================================

st.divider()


with st.expander(
    "Dataset & analytical scope"
):

    st.markdown(
        """
        **Dataset:** UCI Online Retail dataset

        **Analytical focus:** Transaction, customer, product,
        geographic and cancellation behaviour.

        **Data science component:** Customer segmentation using
        behavioural/RFM features, K-Means clustering and PCA.

        **Visualisation:** Matplotlib and Seaborn.

        **Application:** Streamlit.

        **Purpose:** Demonstrate an end-to-end analytics workflow
        from data preparation and exploratory analysis through
        customer segmentation, business insight generation and
        interactive dashboard presentation.
        """
    )


# ============================================================
# 17. FOOTER
# ============================================================

dashboard_footer()