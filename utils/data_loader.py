from pathlib import Path

import pandas as pd
import streamlit as st


# ============================================================
# DATA DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DASHBOARD_DATA_DIR = (
    BASE_DIR
    / "Data"
    / "dashboard"
)


# ============================================================
# GENERIC CSV LOADER
# ============================================================

@st.cache_data
def load_csv(filename):

    file_path = (
        DASHBOARD_DATA_DIR
        / filename
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Dashboard dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


# ============================================================
# DASHBOARD DATASETS
# ============================================================

@st.cache_data
def load_dashboard_data():

    data = {

        "executive_kpis":
            load_csv(
                "executive_kpis.csv"
            ),

        "dashboard_summary":
            load_csv(
                "dashboard_summary.csv"
            ),

        "monthly_performance":
            load_csv(
                "monthly_performance.csv"
            ),

        "segment_performance":
            load_csv(
                "segment_performance.csv"
            ),

        "country_performance":
            load_csv(
                "country_performance.csv"
            ),

        "product_performance":
            load_csv(
                "product_performance.csv"
            ),

        "business_findings":
            load_csv(
                "business_findings.csv"
            )
    }

    return data

# ============================================================
# PROJECT DATA LOADER
# ============================================================

@st.cache_data
def load_project_csv(filename):

    file_path = (
        BASE_DIR
        / "Data"
        / filename
    )

    if not file_path.exists():

        raise FileNotFoundError(
            f"Project dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)