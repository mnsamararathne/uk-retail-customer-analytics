# ============================================================
# CUSTOMER SEGMENTATION
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

from utils.data_loader import load_project_csv


# ============================================================
# 3. LOAD SEGMENTATION DATA
# ============================================================

try:

    customer_rfm = load_project_csv(
        "customer_rfm.csv"
    )

    customer_pca = load_project_csv(
        "customer_pca.csv"
    )

    customer_segments = load_project_csv(
        "customer_segments.csv"
    )

    cluster_evaluation = load_project_csv(
        "cluster_evaluation.csv"
    )

    cluster_profile = load_project_csv(
        "cluster_business_profile.csv"
    )

except Exception as error:

    st.error(
        "Customer segmentation data could not be loaded."
    )

    st.exception(error)

    st.stop()


# ============================================================
# 4. IDENTIFY SEGMENT / CLUSTER COLUMN
# ============================================================

segment_candidates = [
    "Segment",
    "Cluster",
    "CustomerSegment",
    "Customer_Segment"
]


segment_column = None


for column in segment_candidates:

    if column in customer_segments.columns:

        segment_column = column

        break


if segment_column is None:

    st.error(
        "A segment or cluster column could not be identified "
        "in customer_segments.csv."
    )

    st.stop()


# ============================================================
# 5. PAGE HEADER
# ============================================================

st.title(
    "🎯 Customer Segmentation"
)

st.caption(
    "Behavioural customer segmentation using RFM-style "
    "customer features, K-Means clustering and PCA."
)

st.divider()


# ============================================================
# 6. SEGMENTATION OVERVIEW KPIs
# ============================================================

total_segmented_customers = (
    customer_segments["CustomerID"].nunique()
    if "CustomerID" in customer_segments.columns
    else len(customer_segments)
)


number_segments = (
    customer_segments[
        segment_column
    ]
    .nunique()
)


largest_segment = (

    customer_segments[
        segment_column
    ]

    .value_counts()

    .idxmax()
)


largest_segment_size = (

    customer_segments[
        segment_column
    ]

    .value_counts()

    .max()
)


largest_segment_share = (

    largest_segment_size
    /
    len(customer_segments)
    * 100
)


kpi1, kpi2, kpi3, kpi4 = st.columns(4)


with kpi1:

    st.metric(
        "Segmented Customers",
        f"{total_segmented_customers:,}"
    )


with kpi2:

    st.metric(
        "Customer Segments",
        number_segments
    )


with kpi3:

    st.metric(
        "Largest Segment",
        str(largest_segment)
    )


with kpi4:

    st.metric(
        "Largest Segment Share",
        f"{largest_segment_share:.1f}%"
    )


st.divider()


# ============================================================
# 7. SEGMENTATION METHODOLOGY
# ============================================================

with st.expander(
    "How was customer segmentation developed?"
):

    st.markdown(
        """
        The customer segmentation pipeline follows a
        behavioural clustering approach:

        1. Customer-level behavioural features were generated
        from transaction data.

        2. RFM-style measures were used to represent customer
        recency, purchase frequency and monetary value.

        3. Numerical features were scaled before clustering.

        4. Multiple K-Means solutions were evaluated.

        5. Cluster quality was assessed using clustering
        evaluation metrics.

        6. Principal Component Analysis (PCA) was used to
        project the multidimensional customer space into two
        dimensions for visualisation.

        7. Final clusters were profiled using their purchasing
        characteristics.

        8. Cluster profiles were interpreted as actionable
        customer segments.
        """
    )


st.divider()


# ============================================================
# 8. CUSTOMER DISTRIBUTION BY SEGMENT
# ============================================================

st.subheader(
    "Customer Segment Distribution"
)


segment_distribution = (

    customer_segments[
        segment_column
    ]

    .value_counts()

    .rename_axis(
        segment_column
    )

    .reset_index(
        name="Customers"
    )
)


segment_distribution[
    "Percentage"
] = (

    segment_distribution[
        "Customers"
    ]

    /

    segment_distribution[
        "Customers"
    ].sum()

    * 100
)


left, right = st.columns(
    [2, 1]
)


with left:

    fig, ax = plt.subplots(
        figsize=(9, 5)
    )


    sns.barplot(
        data=segment_distribution,
        x=segment_column,
        y="Customers",
        ax=ax
    )


    ax.set_title(
        "Number of Customers by Segment"
    )

    ax.set_xlabel(
        "Customer Segment"
    )

    ax.set_ylabel(
        "Customers"
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

    st.dataframe(
        segment_distribution,
        use_container_width=True,
        hide_index=True
    )


st.divider()


# ============================================================
# 9. CLUSTER EVALUATION
# ============================================================

st.subheader(
    "Cluster Evaluation"
)


st.caption(
    "Evaluation of alternative K-Means solutions used to "
    "support selection of the final cluster configuration."
)


st.dataframe(
    cluster_evaluation,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 10. VISUALISE CLUSTER EVALUATION METRICS
# ============================================================

numeric_evaluation_columns = (

    cluster_evaluation

    .select_dtypes(
        include=np.number
    )

    .columns

    .tolist()
)


# Try to identify K column

k_candidates = [
    "k",
    "K",
    "Clusters",
    "n_clusters",
    "NumberOfClusters"
]


k_column = None


for column in k_candidates:

    if column in cluster_evaluation.columns:

        k_column = column
        break


if (
    k_column is not None
    and
    len(numeric_evaluation_columns) > 1
):

    metric_columns = [

        column

        for column
        in numeric_evaluation_columns

        if column != k_column
    ]


    selected_metric = st.selectbox(
        "Select cluster evaluation metric",
        metric_columns
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    sns.lineplot(
        data=cluster_evaluation,
        x=k_column,
        y=selected_metric,
        marker="o",
        ax=ax
    )


    ax.set_title(
        f"{selected_metric} by Number of Clusters"
    )

    ax.set_xlabel(
        "Number of Clusters"
    )

    ax.set_ylabel(
        selected_metric
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
# 11. PCA CLUSTER VISUALISATION
# ============================================================

st.subheader(
    "PCA Visualisation of Customer Segments"
)


# ------------------------------------------------------------
# Detect PCA columns
# ------------------------------------------------------------

pca_candidates_1 = [
    "PC1",
    "PCA1",
    "PrincipalComponent1",
    "Principal_Component_1"
]


pca_candidates_2 = [
    "PC2",
    "PCA2",
    "PrincipalComponent2",
    "Principal_Component_2"
]


pc1 = None
pc2 = None


for column in pca_candidates_1:

    if column in customer_pca.columns:

        pc1 = column
        break


for column in pca_candidates_2:

    if column in customer_pca.columns:

        pc2 = column
        break


# ------------------------------------------------------------
# Add segment labels if PCA file does not contain them
# ------------------------------------------------------------

pca_plot_df = customer_pca.copy()


if (
    segment_column not in pca_plot_df.columns
    and
    "CustomerID" in pca_plot_df.columns
    and
    "CustomerID" in customer_segments.columns
):

    pca_plot_df = (

        pca_plot_df

        .merge(

            customer_segments[
                [
                    "CustomerID",
                    segment_column
                ]
            ],

            on="CustomerID",

            how="left"
        )
    )


# ------------------------------------------------------------
# PCA Scatter Plot
# ------------------------------------------------------------

if (
    pc1 is not None
    and
    pc2 is not None
    and
    segment_column in pca_plot_df.columns
):

    fig, ax = plt.subplots(
        figsize=(11, 7)
    )


    sns.scatterplot(
        data=pca_plot_df,
        x=pc1,
        y=pc2,
        hue=segment_column,
        alpha=0.65,
        s=45,
        ax=ax
    )


    ax.set_title(
        "Customer Segments in PCA Space"
    )

    ax.set_xlabel(
        "Principal Component 1"
    )

    ax.set_ylabel(
        "Principal Component 2"
    )


    ax.legend(
        title="Segment",
        bbox_to_anchor=(1.02, 1),
        loc="upper left"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


    st.caption(
        "PCA reduces the multidimensional customer feature "
        "space to two components for visual interpretation. "
        "The PCA projection is used for visualisation rather "
        "than as proof that the clusters are perfectly separated."
    )


else:

    st.warning(
        "PCA columns or customer segment labels could not "
        "be identified automatically."
    )


st.divider()


# ============================================================
# 12. CLUSTER BUSINESS PROFILE
# ============================================================

st.subheader(
    "Customer Segment Profiles"
)


st.dataframe(
    cluster_profile,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 13. PROFILE HEATMAP
# ============================================================

st.subheader(
    "Behavioural Comparison Across Segments"
)


profile_numeric_columns = (

    cluster_profile

    .select_dtypes(
        include=np.number
    )

    .columns

    .tolist()
)


# Avoid IDs / cluster identifier where appropriate

identifier_candidates = [
    "Cluster",
    "Segment",
    "CustomerID"
]


heatmap_features = [

    column

    for column
    in profile_numeric_columns

    if column not in identifier_candidates
]


if heatmap_features:

    profile_heatmap_df = (

        cluster_profile[
            heatmap_features
        ]

        .copy()
    )


    # Standardise profile columns only for visual comparison.
    # This prevents high-magnitude monetary variables from
    # dominating the heatmap.

    profile_std = (
        profile_heatmap_df.std()
        .replace(0, 1)
    )


    profile_scaled = (

        profile_heatmap_df
        -
        profile_heatmap_df.mean()

    ) / profile_std


    # Determine labels

    profile_label_column = None


    for candidate in [
        "Segment",
        "Cluster"
    ]:

        if candidate in cluster_profile.columns:

            profile_label_column = candidate
            break


    if profile_label_column is not None:

        profile_scaled.index = (

            cluster_profile[
                profile_label_column
            ]
            .astype(str)
        )


    fig, ax = plt.subplots(
        figsize=(12, 6)
    )


    sns.heatmap(
        profile_scaled,
        annot=True,
        fmt=".2f",
        center=0,
        ax=ax
    )


    ax.set_title(
        "Standardised Customer Segment Profile"
    )

    ax.set_xlabel(
        "Customer Behaviour Feature"
    )

    ax.set_ylabel(
        "Customer Segment"
    )


    plt.xticks(
        rotation=45,
        ha="right"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


    st.caption(
        "Values are standardised within each feature for "
        "visual comparison. Positive values indicate that a "
        "segment is above the overall segment-profile mean for "
        "that feature; negative values indicate below-average "
        "levels."
    )


st.divider()


# ============================================================
# 14. RFM ANALYSIS
# ============================================================

st.subheader(
    "RFM Customer Behaviour"
)


st.caption(
    "Recency, Frequency and Monetary features provide a "
    "behavioural representation of customer purchasing patterns."
)


rfm_numeric = (

    customer_rfm

    .select_dtypes(
        include=np.number
    )

    .columns

    .tolist()
)


# Remove customer identifier

rfm_features = [

    column

    for column
    in rfm_numeric

    if column != "CustomerID"
]


if rfm_features:

    selected_rfm_feature = st.selectbox(
        "Explore RFM feature",
        rfm_features
    )


    fig, ax = plt.subplots(
        figsize=(10, 5)
    )


    sns.histplot(
        data=customer_rfm,
        x=selected_rfm_feature,
        bins=40,
        kde=True,
        ax=ax
    )


    ax.set_title(
        f"Distribution of {selected_rfm_feature}"
    )

    ax.set_xlabel(
        selected_rfm_feature
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
# 15. RFM RELATIONSHIP ANALYSIS
# ============================================================

st.subheader(
    "RFM Feature Relationships"
)


if len(rfm_features) >= 2:

    rfm_correlation = (

        customer_rfm[
            rfm_features
        ]

        .corr()
    )


    fig, ax = plt.subplots(
        figsize=(9, 6)
    )


    sns.heatmap(
        rfm_correlation,
        annot=True,
        fmt=".2f",
        center=0,
        ax=ax
    )


    ax.set_title(
        "RFM Feature Correlation Matrix"
    )


    plt.tight_layout()


    st.pyplot(
        fig,
        use_container_width=True
    )


    plt.close(fig)


st.divider()


# ============================================================
# 16. CUSTOMER SEGMENT EXPLORER
# ============================================================

st.subheader(
    "Customer Segment Explorer"
)


available_segments = (

    customer_segments[
        segment_column
    ]

    .dropna()

    .unique()

    .tolist()
)


selected_segment = st.selectbox(
    "Select customer segment",
    available_segments
)


selected_segment_df = (

    customer_segments[
        customer_segments[
            segment_column
        ]
        ==
        selected_segment
    ]

    .copy()
)


segment_customer_count = len(
    selected_segment_df
)


segment_share = (

    segment_customer_count
    /
    len(customer_segments)
    * 100
)


explorer1, explorer2 = st.columns(2)


with explorer1:

    st.metric(
        "Customers in Segment",
        f"{segment_customer_count:,}"
    )


with explorer2:

    st.metric(
        "Share of Customer Base",
        f"{segment_share:.1f}%"
    )


st.dataframe(
    selected_segment_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# 17. INDIVIDUAL CUSTOMER LOOKUP
# ============================================================

if "CustomerID" in customer_segments.columns:

    st.subheader(
        "Individual Customer Lookup"
    )


    customer_search = st.text_input(
        "Enter Customer ID",
        placeholder="Example: 17850"
    )


    if customer_search:

        customer_result = (

            customer_segments[
                customer_segments[
                    "CustomerID"
                ]
                .astype(str)
                ==
                customer_search.strip()
            ]
        )


        if customer_result.empty:

            st.warning(
                "Customer ID was not found."
            )


        else:

            st.dataframe(
                customer_result,
                use_container_width=True,
                hide_index=True
            )


            customer_segment_value = (

                customer_result[
                    segment_column
                ]
                .iloc[0]
            )


            st.success(
                f"This customer belongs to segment: "
                f"{customer_segment_value}"
            )


# ============================================================
# 18. DATA EXPLORERS
# ============================================================

st.divider()


with st.expander(
    "Explore Complete Customer Segment Dataset"
):

    st.dataframe(
        customer_segments,
        use_container_width=True,
        hide_index=True
    )


with st.expander(
    "Explore RFM Dataset"
):

    st.dataframe(
        customer_rfm,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# 19. FOOTER
# ============================================================

st.divider()


st.caption(
    "Customer Segmentation | "
    "UK Retail Customer Analytics"
)