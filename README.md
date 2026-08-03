# 📊 Mutual Fund Analytics Platform

A complete **Data Analytics & ETL project** developed as part of the **Bluestock Fintech Internship**. This project demonstrates an end-to-end data pipeline for mutual fund analytics, including data ingestion, cleaning, database design, SQL analysis, and live NAV integration.

---

## 🚀 Project Highlights

- 📥 Data ingestion from 10 mutual fund datasets
- 🧹 Data cleaning and validation using Pandas
- 🌐 Live NAV fetching using MFAPI
- 🗄 SQLite database with Star Schema design
- 📈 Analytical SQL queries
- 📑 Data Quality & Cleaning Reports
- 📚 Comprehensive Data Dictionary
- 📊 Foundation for dashboard development

---

# 🏗 Project Architecture

```
Mutual_Fund_Analytics
│
├── data
│   ├── raw
│   └── processed
│
├── reports
│   ├── data_quality_summary.txt
│   ├── data_cleaning_report.txt
│   └── data_dictionary.md
│
├── sql
│   ├── schema.sql
│   └── queries.sql
│
├── src
│   ├── config.py
│   ├── utils.py
│   ├── data_ingestion.py
│   ├── live_nav_fetch.py
│   ├── data_cleaning.py
│   └── database_loader.py
│
├── bluestock_mf.db
├── requirements.txt
└── README.md
```

---

# 🎯 Objectives

- Build an end-to-end ETL pipeline for mutual fund data.
- Validate and clean financial datasets.
- Fetch live Net Asset Value (NAV) using MFAPI.
- Design a relational database using SQLite.
- Perform analytical SQL queries.
- Prepare clean datasets for dashboard visualization.

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3 |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Database | SQLite |
| ORM | SQLAlchemy |
| API | MFAPI |
| Notebook | Jupyter |
| Version Control | Git & GitHub |

---

# 📂 Datasets Used

| Dataset | Description |
|----------|-------------|
| Fund Master | Mutual fund master details |
| NAV History | Historical Net Asset Values |
| AUM by Fund House | Assets Under Management |
| Monthly SIP Inflows | SIP investment statistics |
| Category Inflows | Category-wise inflows |
| Industry Folio Count | Industry folio statistics |
| Scheme Performance | Return and risk metrics |
| Investor Transactions | Investor transaction records |
| Portfolio Holdings | Mutual fund holdings |
| Benchmark Indices | Historical benchmark values |

---

# ⚙ Features Implemented

## ✅ Day 1

- Project structure creation
- Data ingestion
- Dataset validation
- Data quality analysis
- MFAPI integration
- AMFI code validation

---

## ✅ Day 2

- Data cleaning pipeline
- Processed datasets generation
- SQLite database creation
- Star schema implementation
- Database loading using SQLAlchemy
- Analytical SQL queries
- Data dictionary documentation

---

# 📊 Database Schema

### Dimension Tables

- dim_fund
- dim_date

### Fact Tables

- fact_nav
- fact_transactions
- fact_performance
- fact_aum

---

# ▶️ How to Run

Clone the repository

```bash
git clone https://github.com/RockyRohith12/mutual-fund-analytics-platform.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run Day 1

```bash
python src/data_ingestion.py
```

Fetch Live NAV

```bash
python src/live_nav_fetch.py
```

Run Data Cleaning

```bash
python src/data_cleaning.py
```

Create Database

```bash
python src/database_loader.py
```

---

# 📁 Outputs

- Cleaned datasets (`data/processed/`)
- SQLite database (`bluestock_mf.db`)
- Data Quality Report
- Data Cleaning Report
- SQL Schema
- SQL Queries
- Data Dictionary

---

# 🔮 Future Enhancements

- Interactive Power BI Dashboard
- Streamlit Dashboard
- Automated ETL Scheduling
- Machine Learning-based Mutual Fund Recommendation
- Portfolio Risk Analysis
- Predictive NAV Forecasting

---

# 👨‍💻 Author

**V Rohith**

B.Tech – Computer Science & Engineering (AI & ML)

Bluestock Fintech Internship

---

## ⭐ Acknowledgement

This project was developed as part of the **Bluestock Fintech Mutual Fund Analytics Internship** to demonstrate practical skills in **Data Engineering, SQL, ETL, and Data Analytics**.