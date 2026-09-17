# uk-retail-customer-analytics

An end-to-end data science portfolio project exploring UK online retail transaction data using Python, Pandas, NumPy, Matplotlib, Seaborn and Scikit-learn.

The project demonstrates a structured data science workflow covering data cleaning, exploratory data analysis (EDA), statistical visualisation, time-series analysis, customer behaviour analysis, RFM segmentation, clustering, PCA and machine-learning visualisation.

====Project Objective===

Online retailers generate large volumes of transactional data, but converting these records into meaningful customer and business insights requires systematic analysis and effective visualisation.

This project investigates purchasing behaviour, sales patterns, product performance and customer characteristics within an online retail dataset.

The primary objective is to demonstrate how exploratory, statistical and machine-learning visualisation techniques can transform transactional data into interpretable and actionable insights.

====Research Questions====

The analysis is guided by five questions:

What are the major distributions and data-quality characteristics of the retail dataset?
How do sales and customer behaviour vary across products, countries and time?
What relationships exist among transaction value, purchase frequency, recency and customer spending?
Can customers be meaningfully segmented using behavioural characteristics?
How can statistical and machine-learning visualisations translate analytical results into useful business insights?

====Dataset====

The project uses the UCI Online Retail Dataset, containing transactional records from a UK-based online retailer.

Key variables include:

Feature	Description
InvoiceNo	Unique invoice/transaction identifier
StockCode	Product identifier
Description	Product description
Quantity	Quantity purchased
InvoiceDate	Transaction date and time
UnitPrice	Price per unit
CustomerID	Customer identifier
Country	Customer country

Additional analytical features are engineered during the project, including:

Revenue
Month
Day of week
Hour
Order value
Customer purchase frequency
Recency
Monetary value
Customer-level behavioural features

====Technology Stack====

Programming

Python

Data Manipulation

Pandas
NumPy

Data Visualisation

Matplotlib
Seaborn

Machine Learning

Scikit-learn

Development Environment

Jupyter Notebook
Git
GitHub

====Project Methodology====

The project follows a structured analytical workflow:

Raw Transaction Data
        │
        ▼
Data Understanding & Profiling
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Feature Engineering
        │
        ▼
Exploratory Data Analysis
        │
        ├── Univariate Analysis
        ├── Bivariate Analysis
        └── Multivariate Analysis
        │
        ▼
Time-Series Analysis
        │
        ▼
RFM Customer Analysis
        │
        ▼
Customer Segmentation
        │
        ├── Feature Scaling
        ├── K-Means Clustering
        └── Cluster Evaluation
        │
        ▼
PCA Visualisation
        │
        ▼
Machine-Learning Analysis
        │
        ▼
Business Insights & Recommendations

====Exploratory Data Analysis====

The EDA stage investigates the structure, distribution and relationships within the data.

Univariate Analysis

Techniques include:

Histograms
Kernel Density Estimation (KDE)
Boxplots
Violin plots
ECDF plots
Count plots
Bar charts

The analysis examines:

Central tendency
Variability
Skewness
Distribution shape
Potential outliers
Category frequencies
Bivariate Analysis

Relationships between variables are investigated using:

Scatterplots
Regression plots
Boxplots
Violin plots
Bar plots
Joint plots
Cross-tabulation heatmaps
Multivariate Analysis

Multiple variables are investigated simultaneously using:

Pair plots
Correlation heatmaps
Faceted visualisations
Hue, size and style encoding
Multidimensional scatterplots

====Time-Series Analysis====

Transaction timestamps are used to investigate temporal purchasing behaviour.

Analysis includes:

Daily revenue trends
Monthly revenue patterns
Day-of-week behaviour
Hourly purchasing behaviour
Rolling averages
Seasonal patterns
Peak-period identification

====RFM Customer Analysis====

Customer-level behaviour is analysed using the RFM framework:

Recency — How recently did the customer purchase?

Frequency — How frequently does the customer purchase?

Monetary Value — How much revenue has the customer generated?

The transaction-level dataset is transformed into a customer-level analytical dataset for segmentation and modelling.

====Customer Segmentation====

Customer behavioural characteristics are explored using K-Means clustering.

The workflow includes:

Customer-level feature engineering
Feature scaling
Investigation of suitable cluster counts
K-Means clustering
Silhouette analysis
Cluster profiling
Business interpretation

Cluster characteristics are visualised using scatterplots, boxplots, violin plots and comparative charts.

====Principal Component Analysis====

Principal Component Analysis (PCA) is used to investigate the lower-dimensional structure of customer behaviour.

Visualisations include:

PC1 vs PC2
Cluster separation
Explained variance
Cumulative explained variance
Feature loadings

====Machine-Learning Visualisation====

The project also demonstrates visualisation techniques used when evaluating predictive models.

These include:

Confusion Matrix
ROC Curve
Precision-Recall Curve
Feature Importance
Learning Curves
Calibration Curves

The emphasis is not only on calculating performance metrics, but also on communicating model behaviour clearly.

====Visualisation Skills Demonstrated ====

Matplotlib
Figure and Axes architecture
Line charts
Scatterplots
Bar charts
Histograms
Boxplots
Subplots
Axis formatting
Tick formatting
Legends
Grid lines
Annotations
Reference lines
Logarithmic scales
Figure layouts
Publication-quality figure export
Seaborn
histplot
kdeplot
ecdfplot
countplot
barplot
boxplot
violinplot
stripplot
swarmplot
pointplot
scatterplot
lineplot
regplot
heatmap
pairplot
jointplot
relplot
displot
catplot
lmplot

====Repository Structure====
uk-retail-customer-analytics/
│
├── README.md
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_Data_Understanding.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Univariate_Analysis.ipynb
│   ├── 04_Bivariate_Analysis.ipynb
│   ├── 05_Multivariate_Analysis.ipynb
│   ├── 06_Time_Series_Analysis.ipynb
│   ├── 07_Customer_Segmentation.ipynb
│   ├── 08_ML_Visualisation.ipynb
│   └── 09_Business_Insights.ipynb
│
├── src/
│   ├── preprocessing.py
│   └── visualization.py
│
├── figures/
│   ├── distributions/
│   ├── relationships/
│   ├── timeseries/
│   └── machine_learning/
│
├── reports/
│   └── executive_summary.pdf
│
└── cheatsheets/
    ├── matplotlib_cheatsheet.pdf
    ├── seaborn_cheatsheet.pdf
    └── visualization_selection_guide.pdf

====Key Insights====

This section will be updated after completion of the analysis.

The final analysis will summarise evidence relating to:

Revenue and purchasing patterns
Customer behaviour
Product performance
Geographic differences
Temporal purchasing patterns
Customer segments
Important behavioural characteristics
Potential business opportunities

====Featured Visualisations====

Final portfolio-quality visualisations will be added here as the analysis progresses.

Planned examples include:

Revenue trend analysis
Customer purchasing distributions
Product performance rankings
Correlation heatmap
RFM customer analysis
Customer cluster visualisation
PCA cluster visualisation
Machine-learning evaluation plots

====Business Value====

The project aims to demonstrate how transaction data can support decisions relating to:

Customer segmentation
Customer retention
Marketing prioritisation
Product strategy
Revenue analysis
Customer engagement
Resource allocation

Analytical findings will be distinguished from business recommendations so that recommendations remain supported by evidence from the analysis.

====Limitations====

Potential limitations considered during the project include:

Historical data may not represent current retail behaviour.
Customer identifiers may be missing for some transactions.
Transactional data provides limited demographic information.
Observational relationships should not be interpreted as causal effects.
Customer segments produced through clustering are analytical groupings rather than objectively existing customer categories.
Predictive performance may not generalise beyond the available dataset without external validation.

====Reproducibility====

The project is designed to be reproducible using the supplied notebooks and dependency information.

Install the required packages using:

pip install -r requirements.txt

Then execute the notebooks sequentially from 01_Data_Understanding.ipynb.

====Learning Outcomes====

Through this project I aim to strengthen practical skills in:

Python data analysis
Exploratory Data Analysis
Statistical visualisation
Matplotlib
Seaborn
Data storytelling
Customer analytics
Feature engineering
Unsupervised machine learning
PCA
Model evaluation
Business interpretation
Reproducible data science workflows

====Project Status====

Status: In Development

Current workflow:

Data Understanding → Data Cleaning → EDA → Time Series → Customer Segmentation → ML Visualisation → Business Insights

====Author====

Manesh Nimsara Samararathne

MSc Data Science & Business Analytics
University of Plymouth

Areas of Interest: Data Science • Data Analytics • Machine Learning • Business Intelligence • Explainable AI
