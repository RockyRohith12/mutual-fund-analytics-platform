"""
===========================================================
Mutual Fund Analytics Platform
Day 1 - Data Ingestion & Validation

Author : V Rohith
Internship : Bluestock Fintech
===========================================================
"""

import pandas as pd
from pathlib import Path


# ===========================================================
# PROJECT PATHS
# ===========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "Provided_Data"

REPORT_PATH = PROJECT_ROOT / "reports"
REPORT_PATH.mkdir(exist_ok=True)


# ===========================================================
# DATASET FILES
# ===========================================================

DATASETS = {
    "fund_master": "01_fund_master.csv",
    "nav_history": "02_nav_history.csv",
    "aum_by_fund_house": "03_aum_by_fund_house.csv",
    "monthly_sip_inflows": "04_monthly_sip_inflows.csv",
    "category_inflows": "05_category_inflows.csv",
    "industry_folio_count": "06_industry_folio_count.csv",
    "scheme_performance": "07_scheme_performance.csv",
    "investor_transactions": "08_investor_transactions.csv",
    "portfolio_holdings": "09_portfolio_holdings.csv",
    "benchmark_indices": "10_benchmark_indices.csv",
}


# ===========================================================
# LOAD DATASETS
# ===========================================================

def load_datasets():

    datasets = {}

    print("=" * 80)
    print("LOADING DATASETS")
    print("=" * 80)

    for name, filename in DATASETS.items():

        filepath = RAW_DATA_PATH / filename

        df = pd.read_csv(filepath)

        datasets[name] = df

        print(f"\n{name.upper()}")
        print("-" * 80)

        print("Shape")
        print(df.shape)

        print("\nData Types")
        print(df.dtypes)

        print("\nFirst 5 Rows")
        print(df.head())

    return datasets


# ===========================================================
# EXPLORE FUND MASTER
# ===========================================================

def explore_fund_master(df):

    print("\n" + "=" * 80)
    print("FUND MASTER EXPLORATION")
    print("=" * 80)

    print("\nAvailable Columns")
    print(df.columns.tolist())

    print("\nUnique Fund Houses")
    print(sorted(df["fund_house"].dropna().unique()))

    print("\nUnique Categories")
    print(sorted(df["category"].dropna().unique()))

    print("\nUnique Sub Categories")
    print(sorted(df["sub_category"].dropna().unique()))

    print("\nUnique Risk Categories")
    print(sorted(df["risk_category"].dropna().unique()))

    print("\nTotal Fund Houses :", df["fund_house"].nunique())
    print("Total Schemes :", len(df))


# ===========================================================
# VALIDATE AMFI CODES
# ===========================================================

def validate_amfi_codes(fund_master, nav_history):

    print("\n" + "=" * 80)
    print("AMFI CODE VALIDATION")
    print("=" * 80)

    fund_codes = set(fund_master["amfi_code"])

    nav_codes = set(nav_history["amfi_code"])

    missing = fund_codes - nav_codes

    if not missing:

        print("\n✅ All AMFI codes exist in NAV history.")

    else:

        print("\n❌ Missing AMFI Codes:")

        for code in sorted(missing):
            print(code)

    return missing


# ===========================================================
# DATA QUALITY REPORT
# ===========================================================

def generate_quality_report(datasets, missing_codes):

    report = REPORT_PATH / "data_quality_summary.txt"

    with open(report, "w", encoding="utf-8") as f:

        f.write("=" * 70 + "\n")
        f.write("DATA QUALITY SUMMARY\n")
        f.write("=" * 70 + "\n\n")

        for name, df in datasets.items():

            f.write(f"{name.upper()}\n")
            f.write("-" * 70 + "\n")

            f.write(f"Rows              : {df.shape[0]}\n")
            f.write(f"Columns           : {df.shape[1]}\n")
            f.write(f"Duplicate Rows    : {df.duplicated().sum()}\n")
            f.write(f"Missing Values    : {df.isnull().sum().sum()}\n\n")

        f.write("=" * 70 + "\n")

        if not missing_codes:

            f.write("AMFI VALIDATION : PASSED\n")

        else:

            f.write("AMFI VALIDATION : FAILED\n")
            f.write(f"Missing Codes : {len(missing_codes)}\n")

        f.write("=" * 70 + "\n")

    print("\nData Quality Report Saved Successfully")
    print(report)


# ===========================================================
# MAIN
# ===========================================================

def main():

    datasets = load_datasets()

    explore_fund_master(datasets["fund_master"])

    missing_codes = validate_amfi_codes(
        datasets["fund_master"],
        datasets["nav_history"]
    )

    generate_quality_report(
        datasets,
        missing_codes
    )

    print("\n" + "=" * 80)
    print("DAY 1 DATA INGESTION COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    main()