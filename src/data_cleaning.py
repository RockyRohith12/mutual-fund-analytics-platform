"""
===========================================================
Mutual Fund Analytics Platform
Day 2 - Data Cleaning & ETL

Author      : V Rohith
Internship  : Bluestock Fintech
===========================================================
"""

import pandas as pd

from config import RAW_DATA_DIR

from utils import (
    load_dataset,
    save_dataset,
    remove_duplicates,
    clean_text_columns,
    convert_date_columns,
    missing_value_summary,
    validate_positive,
    append_report,
    write_report
)

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
    "benchmark_indices": "10_benchmark_indices.csv"
}


# ===========================================================
# LOAD ALL DATASETS
# ===========================================================

def load_all_datasets():

    datasets = {}

    print("=" * 80)
    print("LOADING RAW DATASETS")
    print("=" * 80)

    for dataset_name, filename in DATASETS.items():

        df = load_dataset(filename)

        if df is not None:

            datasets[dataset_name] = df

    print()

    return datasets


# ===========================================================
# CLEAN FUND MASTER
# ===========================================================

def clean_fund_master(df):

    print("=" * 80)
    print("Cleaning : FUND MASTER")
    print("=" * 80)

    rows_before = len(df)

    duplicates_removed = 0

    # Remove duplicate AMFI Codes

    before = len(df)

    df = df.drop_duplicates(
        subset="amfi_code",
        keep="first"
    )

    duplicates_removed += before - len(df)

    # Remove leading/trailing spaces

    df = clean_text_columns(df)

    # Convert launch date

    df["launch_date"] = pd.to_datetime(
        df["launch_date"],
        errors="coerce"
    )

    # Expense Ratio Validation

    if "expense_ratio_pct" in df.columns:

        df["expense_ratio_pct"] = pd.to_numeric(
            df["expense_ratio_pct"],
            errors="coerce"
        )

        df = df[
            (df["expense_ratio_pct"] >= 0.10)
            &
            (df["expense_ratio_pct"] <= 2.50)
        ]

    # Exit Load Validation

    if "exit_load_pct" in df.columns:

        df["exit_load_pct"] = pd.to_numeric(
            df["exit_load_pct"],
            errors="coerce"
        )

        df.loc[
            df["exit_load_pct"] < 0,
            "exit_load_pct"
        ] = 0

    rows_after = len(df)

    report = {

        "before": rows_before,
        "after": rows_after,
        "duplicates": duplicates_removed,
        "missing": missing_value_summary(df)

    }

    print(f"Rows Before : {rows_before}")
    print(f"Rows After  : {rows_after}")
    print(f"Duplicates Removed : {duplicates_removed}")

    print()

    return df, report


# ===========================================================
# CLEAN NAV HISTORY
# ===========================================================

def clean_nav_history(df):

    print("=" * 80)
    print("Cleaning : NAV HISTORY")
    print("=" * 80)

    rows_before = len(df)

    duplicates_removed = 0

    invalid_nav_removed = 0

    # Convert Date

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Convert NAV

    df["nav"] = pd.to_numeric(
        df["nav"],
        errors="coerce"
    )

    # Remove Invalid Dates

    df = df.dropna(
        subset=["date"]
    )

    # Sort

    df = df.sort_values(
        by=[
            "amfi_code",
            "date"
        ]
    )

    # Remove Duplicates

    before = len(df)

    df = df.drop_duplicates()

    duplicates_removed += before - len(df)

    # Forward Fill NAV

    df["nav"] = (

        df.groupby("amfi_code")["nav"]

        .transform(lambda x: x.ffill())

    )

    # Remove Invalid NAV

    before = len(df)

    df = df[df["nav"] > 0]

    invalid_nav_removed = before - len(df)

    rows_after = len(df)

    report = {

        "before": rows_before,

        "after": rows_after,

        "duplicates": duplicates_removed,

        "invalid_nav_removed": invalid_nav_removed,

        "missing": missing_value_summary(df)

    }

    print(f"Rows Before : {rows_before}")
    print(f"Rows After  : {rows_after}")
    print(f"Duplicates Removed : {duplicates_removed}")
    print(f"Invalid NAV Removed : {invalid_nav_removed}")

    print()

    return df, report

# ===========================================================
# CLEAN INVESTOR TRANSACTIONS
# ===========================================================

def clean_investor_transactions(df):

    print("=" * 80)
    print("Cleaning : INVESTOR TRANSACTIONS")
    print("=" * 80)

    rows_before = len(df)

    duplicates_removed = 0
    invalid_amount_removed = 0

    # -------------------------------------------------------
    # Convert Transaction Date
    # -------------------------------------------------------

    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"],
        errors="coerce"
    )

    # -------------------------------------------------------
    # Standardize Transaction Type
    # -------------------------------------------------------

    df["transaction_type"] = (
        df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.title()
    )

    mapping = {
        "Sip": "SIP",
        "Lumpsum": "Lumpsum",
        "Redemption": "Redemption"
    }

    df["transaction_type"] = (
        df["transaction_type"]
        .replace(mapping)
    )

    # -------------------------------------------------------
    # Remove Invalid Amounts
    # -------------------------------------------------------

    before = len(df)

    df = df[df["amount_inr"] > 0]

    invalid_amount_removed = before - len(df)

    # -------------------------------------------------------
    # KYC Validation
    # -------------------------------------------------------

    valid_status = [
        "Verified",
        "Pending",
        "Rejected"
    ]

    df = df[
        df["kyc_status"].isin(valid_status)
    ]

    # -------------------------------------------------------
    # Remove Duplicate Transactions
    # -------------------------------------------------------

    before = len(df)

    df = df.drop_duplicates()

    duplicates_removed = before - len(df)

    rows_after = len(df)

    report = {

        "before": rows_before,

        "after": rows_after,

        "duplicates": duplicates_removed,

        "invalid_amount_removed": invalid_amount_removed,

        "missing": missing_value_summary(df)

    }

    print(f"Rows Before : {rows_before}")
    print(f"Rows After  : {rows_after}")
    print(f"Duplicates Removed : {duplicates_removed}")
    print(f"Invalid Amount Removed : {invalid_amount_removed}")

    print()

    return df, report


# ===========================================================
# CLEAN SCHEME PERFORMANCE
# ===========================================================

def clean_scheme_performance(df):

    print("=" * 80)
    print("Cleaning : SCHEME PERFORMANCE")
    print("=" * 80)

    rows_before = len(df)

    duplicates_removed = 0

    numeric_columns = [

        "return_1yr_pct",

        "return_3yr_pct",

        "return_5yr_pct",

        "benchmark_3yr_pct",

        "alpha",

        "beta",

        "sharpe_ratio",

        "sortino_ratio",

        "std_dev_ann_pct",

        "max_drawdown_pct",

        "expense_ratio_pct"

    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(

                df[column],

                errors="coerce"

            )

    # -------------------------------------------------------
    # Expense Ratio Validation
    # -------------------------------------------------------

    if "expense_ratio_pct" in df.columns:

        df["expense_ratio_flag"] = (

            ~df["expense_ratio_pct"]

            .between(0.10, 2.50)

        )

    # -------------------------------------------------------
    # Remove Duplicate Rows
    # -------------------------------------------------------

    before = len(df)

    df = df.drop_duplicates()

    duplicates_removed = before - len(df)

    rows_after = len(df)

    report = {

        "before": rows_before,

        "after": rows_after,

        "duplicates": duplicates_removed,

        "missing": missing_value_summary(df)

    }

    print(f"Rows Before : {rows_before}")
    print(f"Rows After  : {rows_after}")
    print(f"Duplicates Removed : {duplicates_removed}")

    print()

    return df, report


# ===========================================================
# GENERIC CLEANING
# ===========================================================

def clean_generic_dataset(dataset_name, df):

    print("=" * 80)
    print(f"Cleaning : {dataset_name.upper()}")
    print("=" * 80)

    rows_before = len(df)

    df = clean_text_columns(df)

    df = convert_date_columns(df)

    df, duplicates_removed = remove_duplicates(df)

    rows_after = len(df)

    report = {

        "before": rows_before,

        "after": rows_after,

        "duplicates": duplicates_removed,

        "missing": missing_value_summary(df)

    }

    print(f"Rows Before : {rows_before}")
    print(f"Rows After  : {rows_after}")
    print(f"Duplicates Removed : {duplicates_removed}")

    print()

    return df, report

# ===========================================================
# MAIN ETL PIPELINE
# ===========================================================

def main():

    print("\n" + "=" * 80)
    print("DAY 2 : DATA CLEANING PIPELINE")
    print("=" * 80)

    datasets = load_all_datasets()

    report_lines = []

    # =======================================================
    # FUND MASTER
    # =======================================================

    fund_master, report = clean_fund_master(
        datasets["fund_master"]
    )

    save_dataset(
        fund_master,
        "fund_master.csv"
    )

    append_report(
        report_lines,
        "fund_master",
        report["before"],
        report["after"],
        report["duplicates"],
        report["missing"]
    )

    # =======================================================
    # NAV HISTORY
    # =======================================================

    nav_history, report = clean_nav_history(
        datasets["nav_history"]
    )

    save_dataset(
        nav_history,
        "nav_history.csv"
    )

    append_report(
        report_lines,
        "nav_history",
        report["before"],
        report["after"],
        report["duplicates"],
        report["missing"]
    )

    # =======================================================
    # INVESTOR TRANSACTIONS
    # =======================================================

    investor_transactions, report = clean_investor_transactions(
        datasets["investor_transactions"]
    )

    save_dataset(
        investor_transactions,
        "investor_transactions.csv"
    )

    append_report(
        report_lines,
        "investor_transactions",
        report["before"],
        report["after"],
        report["duplicates"],
        report["missing"]
    )

    # =======================================================
    # SCHEME PERFORMANCE
    # =======================================================

    scheme_performance, report = clean_scheme_performance(
        datasets["scheme_performance"]
    )

    save_dataset(
        scheme_performance,
        "scheme_performance.csv"
    )

    append_report(
        report_lines,
        "scheme_performance",
        report["before"],
        report["after"],
        report["duplicates"],
        report["missing"]
    )

    # =======================================================
    # REMAINING DATASETS
    # =======================================================

    generic_datasets = [

        "aum_by_fund_house",

        "monthly_sip_inflows",

        "category_inflows",

        "industry_folio_count",

        "portfolio_holdings",

        "benchmark_indices"

    ]

    for dataset_name in generic_datasets:

        cleaned_df, report = clean_generic_dataset(

            dataset_name,

            datasets[dataset_name]

        )

        save_dataset(

            cleaned_df,

            f"{dataset_name}.csv"

        )

        append_report(

            report_lines,

            dataset_name,

            report["before"],

            report["after"],

            report["duplicates"],

            report["missing"]

        )

    # =======================================================
    # WRITE REPORT
    # =======================================================

    write_report(report_lines)

    print()

    print("=" * 80)

    print("DAY 2 DATA CLEANING COMPLETED SUCCESSFULLY")

    print("=" * 80)

    print()

    print("Processed datasets saved in:")

    print("data/processed")

    print()

    print("Cleaning report saved in:")

    print("reports/data_cleaning_report.txt")

    print()


# ===========================================================
# DRIVER CODE
# ===========================================================

if __name__ == "__main__":

    main()