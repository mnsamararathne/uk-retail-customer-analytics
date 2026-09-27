
import streamlit as st

# ============================================================
# UK RETAIL CUSTOMER ANALYTICS
# APPLICATION ENTRY POINT
# ============================================================

from utils.styles import (
    apply_custom_css,
    apply_chart_style
)


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="UK Retail Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


apply_custom_css()
apply_chart_style()


# ============================================================
# DEFINE PAGES
# ============================================================

executive_page = st.Page(
    "views/executive_overview.py",
    title="Executive Overview",
    icon="🏠",
    default=True
)


sales_page = st.Page(
    "views/sales_analytics.py",
    title="Sales Analytics",
    icon="📈"
)


customer_page = st.Page(
    "views/customer_analytics.py",
    title="Customer Analytics",
    icon="👥"
)


product_page = st.Page(
    "views/product_analytics.py",
    title="Product Analytics",
    icon="📦"
)


geographic_page = st.Page(
    "views/geographic_analytics.py",
    title="Geographic Analytics",
    icon="🌍"
)


cancellation_page = st.Page(
    "views/cancellation_analysis.py",
    title="Cancellation Analysis",
    icon="↩️"
)


segmentation_page = st.Page(
    "views/customer_segmentation.py",
    title="Customer Segmentation",
    icon="🎯"
)


# ============================================================
# NAVIGATION
# ============================================================

navigation = st.navigation(
    {
        "Overview": [
            executive_page
        ],

        "Business Analytics": [
            sales_page,
            customer_page,
            product_page,
            geographic_page,
            cancellation_page
        ],

        "Data Science": [
            segmentation_page
        ]
    }
)


# ============================================================
# SIDEBAR PROJECT INFORMATION
# ============================================================

with st.sidebar:

    st.markdown(
        "### UK Retail Analytics"
    )

    st.caption(
        "Interactive customer and sales analytics "
        "portfolio project."
    )

    st.divider()

    st.caption(
        "MSc Data Science & Business Analytics"
    )


# ============================================================
# RUN SELECTED PAGE
# ============================================================

navigation.run()