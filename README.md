# UK Retail Customer Analytics

An end-to-end data analytics and customer segmentation portfolio project using the **UCI Online Retail Dataset** to investigate sales performance, customer behaviour, product performance, geographic patterns, cancellations, and customer segments.

The project demonstrates a complete analytical workflow using **Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, and Streamlit**, progressing from raw-data understanding and cleaning through feature engineering, exploratory analysis, RFM analysis, customer segmentation, business KPI analysis, and interactive dashboard development.

---

## Project Objectives

Online retailers generate large volumes of transactional data, but raw transaction records alone provide limited support for business decision-making.

This project aims to transform retail transaction data into meaningful and interpretable insights by examining:

* Sales and revenue performance
* Customer purchasing behaviour
* Product performance
* Geographic sales patterns
* Cancellation and return behaviour
* Customer value using RFM analysis
* Behavioural customer segments
* Business KPIs and opportunities

The final analytical results are presented through an interactive **Streamlit dashboard**.

---

## Dataset

The project uses the **UCI Online Retail Dataset**, which contains transactional data from a UK-based online retailer.

### Original Variables

| Feature       | Description                           |
| ------------- | ------------------------------------- |
| `InvoiceNo`   | Unique invoice/transaction identifier |
| `StockCode`   | Product identifier                    |
| `Description` | Product description                   |
| `Quantity`    | Quantity purchased                    |
| `InvoiceDate` | Transaction date and time             |
| `UnitPrice`   | Price per unit                        |
| `CustomerID`  | Customer identifier                   |
| `Country`     | Customer country                      |

Additional variables and analytical datasets are created during data cleaning and feature engineering.

---

## Project Workflow

The project follows the analytical pipeline:

```text
Raw Online Retail Data
        │
        ▼
01. Data Understanding & Profiling
        │
        ▼
02. Data Cleaning
        │
        ▼
03. Feature Engineering
        │
        ├── Transaction Features
        ├── Product Features
        └── Customer Features
        │
        ▼
04. Exploratory Data Analysis
        │
        ├── Dataset Validation
        ├── Numerical Analysis
        ├── Categorical Analysis
        ├── Transaction Analysis
        ├── Customer Analysis
        ├── Product Analysis
        ├── Geographic Analysis
        ├── Temporal Analysis
        └── Cancellation Analysis
        │
        ▼
05. Customer Segmentation
        │
        ├── RFM Analysis
        ├── Feature Scaling
        ├── K-Means Clustering
        ├── Cluster Evaluation
        ├── Cluster Profiling
        └── PCA Visualisation
        │
        ▼
06. Business Insights & KPI Analysis
        │
        ▼
Interactive Streamlit Dashboard
```

---

# Analytical Notebooks

## 01 — Data Understanding and Profiling

`01_Data_Understanding_and_Profiling.ipynb`

The first notebook examines the original dataset before transformations are applied.

Key activities include:

* Dataset structure inspection
* Data-type validation
* Descriptive statistics
* Cardinality analysis
* Missing-value analysis
* Duplicate investigation
* Business-rule validation
* Cancellation and return investigation
* Initial distribution analysis
* Data-quality assessment
* Cleaning decisions

The purpose of this stage is to understand the dataset and make evidence-based cleaning decisions.

---

## 02 — Data Cleaning

`02_Data_Cleaning.ipynb`

This notebook applies the cleaning decisions established during profiling.

The cleaning process prepares a consistent analytical dataset while avoiding indiscriminate removal of records that may represent legitimate business activity.

---

## 03 — Feature Engineering

`03_Feature_Engineering.ipynb`

The cleaned transaction data is transformed into analytical features and datasets required for subsequent analysis.

The notebook produces three primary datasets:

### Transaction-Level Dataset

Used for:

* Sales analysis
* Revenue analysis
* Temporal analysis
* Geographic analysis
* Cancellation analysis

### Product-Level Dataset

Used for:

* Product performance
* Product revenue
* Product demand
* Product ranking

### Customer-Level Dataset

Used for:

* Customer behaviour analysis
* Customer value analysis
* Purchase frequency analysis
* Customer segmentation

Engineered variables include transaction, temporal, revenue, customer, and product-level measures.

---

## 04 — Exploratory Data Analysis

`04_Exploratory_Data_Analysis.ipynb`

The EDA notebook systematically investigates patterns within the feature-engineered datasets.

### Dataset Validation

The feature-engineered datasets are validated before analysis by checking:

* Dimensions
* Column names
* Data types
* Missing values
* Duplicates
* Date ranges
* Customer coverage
* Revenue consistency

### Numerical Analysis

Numerical variables are examined using:

* Descriptive statistics
* Histograms
* Density distributions
* Boxplots
* Quantiles
* Skewness
* Outlier analysis

### Categorical Analysis

Categorical variables are analysed through:

* Frequency distributions
* Proportional analysis
* Count plots
* Comparative bar charts

### Sales Analysis

The analysis investigates:

* Revenue
* Transaction volumes
* Order behaviour
* Quantity sold
* Purchasing patterns

### Customer Analysis

Customer-level analysis examines:

* Customer spending
* Purchase frequency
* Customer activity
* Customer lifetime behaviour
* Customer concentration

### Product Analysis

Product analysis examines:

* Product demand
* Product revenue
* Best-performing products
* Product purchasing patterns

### Geographic Analysis

Sales performance is compared across customer countries.

### Temporal Analysis

Transaction timestamps are used to investigate:

* Monthly patterns
* Day-of-week patterns
* Hourly purchasing behaviour
* Revenue trends
* Transaction trends

### Cancellation Analysis

Cancellation and return behaviour is analysed separately to avoid mixing negative transactions with genuine purchasing activity.

---

# Customer Segmentation

## RFM Analysis

Customer behaviour is analysed using the **RFM framework**:

**Recency** — How recently a customer purchased.

**Frequency** — How frequently a customer purchased.

**Monetary Value** — How much revenue the customer generated.

RFM provides a compact representation of customer purchasing behaviour and supports subsequent customer segmentation.

Customers without valid positive purchasing activity are excluded from the RFM population where appropriate rather than artificially forcing them into purchasing-based segments.

---

## K-Means Customer Segmentation

`05_Customer_Segmentation.ipynb`

Behavioural customer segmentation is performed using **K-Means clustering**.

The workflow includes:

1. Customer-level analytical dataset preparation
2. RFM feature construction
3. Distribution assessment
4. Feature transformation where appropriate
5. Feature scaling
6. Cluster-number investigation
7. K-Means clustering
8. Silhouette evaluation
9. Cluster profiling
10. Business interpretation

The objective is not simply to generate clusters but to understand how groups of customers differ in terms of purchasing behaviour and business value.

---

## Principal Component Analysis

**Principal Component Analysis (PCA)** is used to visualise the multidimensional customer segmentation results in a lower-dimensional space.

PCA supports:

* Cluster visualisation
* Assessment of cluster separation
* Dimensionality interpretation
* Communication of segmentation results

PCA is used primarily as an analytical and visualisation technique rather than as evidence that the discovered clusters represent objectively existing customer categories.

---

# Business Insights and KPI Analysis

`06_Business_Insights_and_KPI_Analysis.ipynb`

The final analytical notebook translates the outputs from EDA and customer segmentation into business-oriented measures.

The analysis brings together findings relating to:

* Revenue performance
* Customer performance
* Product performance
* Geographic performance
* Temporal purchasing behaviour
* Cancellation behaviour
* Customer segments
* Customer value

The purpose is to bridge technical analysis and practical business interpretation.

---

# Interactive Streamlit Dashboard

The project includes an interactive **Streamlit analytics application**.

The application entry point is:

```text
app.py
```

The dashboard is organised into three navigation areas.

### Overview

* Executive Overview

### Business Analytics

* Sales Analytics
* Customer Analytics
* Product Analytics
* Geographic Analytics
* Cancellation Analysis

### Data Science

* Customer Segmentation

This structure separates high-level business reporting from detailed analytical and data-science outputs.

---

## Executive Overview

Provides a high-level summary of the most important KPIs and analytical findings.

It is designed to give decision-makers a concise overview before exploring individual analytical areas.

---

## Sales Analytics

Explores:

* Revenue performance
* Sales trends
* Transaction activity
* Temporal sales patterns
* Purchasing behaviour

---

## Customer Analytics

Explores:

* Customer value
* Purchase frequency
* Customer spending
* Customer activity
* Customer concentration

---

## Customer Segmentation

Presents the results of:

* RFM analysis
* K-Means clustering
* Cluster profiling
* Segment comparison
* PCA visualisation

---

## Product Analytics

Investigates:

* Product revenue
* Product demand
* Best-performing products
* Product-level contribution

---

## Geographic Analytics

Investigates:

* Revenue by country
* Customer distribution
* Geographic differences in purchasing behaviour
* International market contribution

---

## Cancellation Analysis

Examines:

* Cancellation activity
* Returned quantities
* Negative-value transactions
* Cancellation patterns
* Potential business implications

---

# Key Findings

The analysis revealed several important patterns in customer behaviour, sales performance, product demand, geographic activity, and cancellations.

### Sales Performance

* Retail performance varies considerably across transactions and time periods, demonstrating that aggregate revenue alone does not fully explain business performance.
* Revenue, order activity, quantity sold, and average order value provide complementary perspectives on sales performance.
* Temporal analysis identifies differences in purchasing activity across months, days of the week, and hours of the day, providing useful context for understanding when customer activity is strongest.

### Customer Behaviour

* Customer value is highly heterogeneous, with substantial differences in spending, purchasing frequency, average order value, product diversity, and activity levels.
* Revenue is concentrated among higher-value customers rather than being distributed uniformly across the customer base.
* This concentration highlights the importance of identifying strategically valuable customers rather than treating all customers as equally important.

### RFM and Customer Segmentation

* RFM analysis provides a meaningful behavioural representation of customers based on **Recency, Frequency, and Monetary Value**.
* Customers without valid positive purchasing activity were excluded from the purchase-based RFM population to avoid assigning misleading behavioural values to cancellation- or return-only activity.
* K-Means clustering identifies distinct behavioural customer groups with different purchasing characteristics and levels of customer value.
* The segmentation demonstrates how unsupervised machine learning can convert transaction history into interpretable customer groups that can support differentiated customer-management strategies.
* PCA provides a lower-dimensional representation of the customer feature space and supports visual interpretation of the resulting clusters.

### Product Performance

* Product performance varies substantially across the catalogue.
* Products with the highest quantity sold are not necessarily identical to products generating the highest revenue, demonstrating the importance of evaluating both demand and financial contribution.
* Product-level analysis helps identify commercially important products that may warrant closer monitoring in areas such as inventory, promotion, and product strategy.

### Geographic Performance

* The United Kingdom represents the dominant geographic market in the dataset, which is consistent with the retailer being UK-based.
* International customers nevertheless contribute additional transactions and revenue across multiple markets.
* Geographic analysis provides a clearer understanding of the retailer's core market and the contribution of international customers.

### Cancellations and Returns

* Cancellation and return activity represents a distinct component of the transaction history and should be analysed separately from completed purchasing activity.
* Negative quantities and transaction values associated with cancellations can distort sales, customer, and product metrics if they are interpreted as ordinary purchases.
* Separating positive purchases from cancellation activity therefore produces a more meaningful view of underlying commercial performance.

### Business Implications

The findings suggest several practical opportunities:

* Prioritise high-value and frequently purchasing customers for retention and relationship-management initiatives.
* Use behavioural customer segments to support differentiated engagement and marketing strategies.
* Monitor both product demand and revenue contribution when evaluating product performance.
* Track customer-value concentration to understand dependence on high-value customers.
* Analyse temporal purchasing patterns when planning campaigns and operational activity.
* Monitor geographic performance to distinguish core-market performance from international opportunities.
* Evaluate cancellation activity alongside gross sales to obtain a more complete view of commercial performance.

Overall, the project demonstrates how raw retail transaction data can be transformed into an integrated analytical framework combining **exploratory analysis, customer analytics, unsupervised machine learning, business KPIs, and interactive visualisation**.

> **Note:** The findings are descriptive and relate to the historical transactions analysed in this project. They identify patterns and potential business opportunities but should not be interpreted as causal relationships.

---

# Technology Stack

### Programming

* Python

### Data Manipulation

* Pandas
* NumPy

### Data Visualisation

* Matplotlib
* Seaborn

### Statistical Analysis

* SciPy

### Machine Learning

* Scikit-learn

### Interactive Application

* Streamlit

### Development and Version Control

* Jupyter Notebook
* Visual Studio Code
* Git
* GitHub

---

# Repository Structure

```text
uk-retail-customer-analytics/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── Data/
│   ├── retail_transaction_features.csv
│   ├── product_features.csv
│   └── customer_features.csv
│
├── Notebooks/
│   ├── 01_Data_Understanding_and_Profiling.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   ├── 04_Exploratory_Data_Analysis.ipynb
│   ├── 05_Customer_Segmentation.ipynb
│   └── 06_Business_Insights_and_KPI_Analysis.ipynb
│
├── utils/
│   ├── __init__.py
│   ├── charts.py
│   ├── data_loader.py
│   ├── formatters.py
│   └── styles.py
│
└── views/
    ├── executive_overview.py
    ├── sales_analytics.py
    ├── customer_analytics.py
    ├── customer_segmentation.py
    ├── product_analytics.py
    ├── geographic_analytics.py
    └── cancellation_analysis.py
```

---

# Streamlit Application Architecture

The dashboard follows a modular structure rather than placing the entire application inside `app.py`.

```text
app.py
   │
   ├── Navigation
   │
   ├── views/
   │      ├── Executive Overview
   │      ├── Sales Analytics
   │      ├── Customer Analytics
   │      ├── Customer Segmentation
   │      ├── Product Analytics
   │      ├── Geographic Analytics
   │      └── Cancellation Analysis
   │
   └── utils/
          ├── Data Loading
          ├── Charts
          ├── Formatting
          └── Styling
```

This improves maintainability and separates reusable functionality from individual dashboard pages.

---

# Installation

Clone the repository:

```bash
git clone <repository-url>
cd uk-retail-customer-analytics
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

The current dependency file includes:

```text
streamlit==1.45.1
pandas
numpy
matplotlib
seaborn
scipy
scikit-learn==1.9.0
openpyxl
joblib
```

---

# Running the Streamlit Dashboard

From the project root directory:

```bash
streamlit run app.py
```

If Streamlit is installed through a specific Python environment, it can also be launched using:

```bash
python -m streamlit run app.py
```

---

# Reproducing the Analysis

For complete reproduction of the analytical workflow, execute the notebooks sequentially:

```text
01_Data_Understanding_and_Profiling.ipynb
                ↓
02_Data_Cleaning.ipynb
                ↓
03_Feature_Engineering.ipynb
                ↓
04_Exploratory_Data_Analysis.ipynb
                ↓
05_Customer_Segmentation.ipynb
                ↓
06_Business_Insights_and_KPI_Analysis.ipynb
```

The output datasets generated during earlier stages are used by subsequent analytical stages and the Streamlit application.

---

# Visualisation Skills Demonstrated

The project demonstrates practical use of **Matplotlib and Seaborn** for analytical communication.

Techniques include:

* Histograms
* KDE plots
* Boxplots
* Violin plots
* Bar charts
* Count plots
* Scatterplots
* Line charts
* Heatmaps
* Distribution analysis
* Time-series visualisation
* Customer-segment comparison
* PCA cluster visualisation
* Figure formatting
* Axis formatting
* Legends
* Annotations
* Multi-variable visualisation

Visualisations are selected according to the analytical question rather than simply to demonstrate chart variety.

---

# Business Value

The project demonstrates how transactional retail data can support decisions relating to:

* Customer segmentation
* Customer prioritisation
* Revenue monitoring
* Product strategy
* Geographic performance
* Marketing targeting
* Customer retention
* Cancellation management
* Customer engagement
* Resource allocation

Analytical findings and business recommendations are distinguished so that recommendations remain grounded in observed evidence.

---

# Limitations

Several limitations should be considered when interpreting the analysis:

* The dataset represents historical transactions and may not reflect current retail behaviour.
* Transactional information provides limited demographic information about customers.
* Some customers may contain cancellation or return activity without corresponding valid positive purchasing activity.
* RFM analysis represents purchasing behaviour but does not capture every dimension of customer value.
* K-Means requires analytical assumptions about feature preparation and the number of clusters.
* Customer clusters are analytical groupings and should not be interpreted as objectively existing customer categories.
* PCA simplifies multidimensional information and therefore does not preserve all information contained in the original features.
* Observational relationships identified through EDA should not be interpreted as causal relationships.
* Findings from this dataset should not automatically be generalised to other retailers, markets, or time periods.

---

# Key Skills Demonstrated

This project demonstrates practical experience in:

* Python data analysis
* Data profiling
* Data cleaning
* Data validation
* Feature engineering
* Exploratory Data Analysis
* Statistical analysis
* Matplotlib
* Seaborn
* Customer analytics
* RFM analysis
* Unsupervised machine learning
* K-Means clustering
* Cluster evaluation
* Principal Component Analysis
* Business KPI analysis
* Data storytelling
* Streamlit application development
* Modular Python development
* Git and GitHub
* Reproducible analytical workflows

---

# Project Status

**Core analytical development complete.**

Completed components:

* Data understanding and profiling
* Data cleaning
* Feature engineering
* Exploratory Data Analysis
* RFM customer analysis
* K-Means customer segmentation
* PCA visualisation
* Business KPI analysis
* Interactive Streamlit dashboard
* Modular dashboard architecture

Final portfolio activities include application testing, documentation refinement, dashboard screenshots, and deployment.

---

# Author

**Manesh Nimsara Samararathne**

MSc Data Science & Business Analytics
University of Plymouth

Areas of interest:

**Data Science • Data Analytics • Machine Learning • Business Intelligence • Explainable AI**
