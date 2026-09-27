# ============================================================
# SHARED DASHBOARD STYLING
# UK RETAIL CUSTOMER ANALYTICS
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# GLOBAL CSS
# ============================================================

def apply_custom_css():
    """
    Apply shared visual styling across the dashboard.
    """

    st.markdown(
        """
        <style>

        /* Main page spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1450px;
        }

        /* Main heading */
        h1 {
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        /* Section headings */
        h2, h3 {
            font-weight: 600;
        }

        /* Metric cards */
        [data-testid="stMetric"] {
            background-color: rgba(128, 128, 128, 0.08);
            border: 1px solid rgba(128, 128, 128, 0.18);
            padding: 18px;
            border-radius: 12px;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.90rem;
        }

        [data-testid="stMetricValue"] {
            font-weight: 700;
        }

        /* Dataframes */
        [data-testid="stDataFrame"] {
            border-radius: 10px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.15);
        }

        /* Horizontal rules */
        hr {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# MATPLOTLIB / SEABORN STYLE
# ============================================================

def apply_chart_style():
    """
    Configure a consistent plotting style for Matplotlib
    and Seaborn visualisations.
    """

    sns.set_theme(
        style="whitegrid",
        context="notebook"
    )

    plt.rcParams.update({
        "figure.figsize": (10, 5),
        "figure.dpi": 100,
        "axes.titleweight": "bold",
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "figure.autolayout": True
    })


# ============================================================
# PAGE HEADER
# ============================================================

def page_header(
    title,
    description=None
):
    """
    Display a consistent dashboard page header.
    """

    st.title(title)

    if description:
        st.caption(description)

    st.divider()


# ============================================================
# SECTION HEADER
# ============================================================

def section_header(
    title,
    description=None
):
    """
    Create consistent analytical section headings.
    """

    st.subheader(title)

    if description:
        st.caption(description)


# ============================================================
# FOOTER
# ============================================================

def dashboard_footer():
    """
    Shared footer for dashboard pages.
    """

    st.divider()

    st.caption(
        "UK Retail Customer Analytics • "
        "Python • Pandas • Matplotlib • Seaborn • "
        "Scikit-learn • Streamlit"
    )

# ============================================================
# KPI ROW
# ============================================================

def metric_row(metrics):
    """
    Display a responsive row of Streamlit metric cards.

    metrics example:

    [
        ("Revenue", "£8.9M"),
        ("Orders", "18.5K"),
        ("Customers", "4.3K"),
        ("AOV", "£480")
    ]
    """

    columns = st.columns(
        len(metrics)
    )

    for column, metric in zip(
        columns,
        metrics
    ):

        label = metric[0]
        value = metric[1]

        delta = (
            metric[2]
            if len(metric) > 2
            else None
        )

        with column:

            st.metric(
                label=label,
                value=value,
                delta=delta
            )