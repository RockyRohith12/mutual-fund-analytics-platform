"""
===========================================================
Mutual Fund Analytics Platform
Day 1 - Data Ingestion & Validation

Author      : V Rohith
Internship  : Bluestock Fintech
Description :
    Loads all mutual fund datasets, performs exploratory
    analysis, validates AMFI scheme codes, performs
    data quality checks and generates a quality report.
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
# LOAD ALL DATASETS
# ===========================================================

def load_datasets():
    """
    Load all datasets into memory.
    Displays shape, datatypes and first five rows.
    """

    datasets = {}

    print("=" * 80)
    print("LOADING DATASETS")
    print("=" * 80)

    for name, filename in DATASETS.items():

        filepath = RAW_DATA_PATH / filename

        print(f"\n{name.upper()}")
        print("-" * 80)

        try:

            df = pd.read_csv(
                filepath,
                encoding="utf-8"
            )

            datasets[name] = df

            print("Shape")
            print(df.shape)

            print("\nData Types")
            print(df.dtypes)

            print("\nFirst 5 Rows")
            print(df.head())

        except FileNotFoundError:

            print(f"File not found : {filename}")

        except pd.errors.EmptyDataError:

            print(f"Dataset is empty : {filename}")

        except Exception as e:

            print(f"Error loading {filename}")
            print(e)

    return datasets


# ===========================================================
# FUND MASTER EXPLORATION
# ===========================================================

def explore_fund_master(df):
    """
    Explore important fields inside fund_master dataset.
    """

    print("\n")
    print("=" * 80)
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
    print("Total Schemes     :", len(df))


# ===========================================================
# AMFI CODE VALIDATION
# ===========================================================

def validate_amfi_codes(
    fund_master,
    nav_history
):
    """
    Validate every AMFI scheme code
    exists inside NAV history.
    """

    print("\n")
    print("=" * 80)
    print("AMFI CODE VALIDATION")
    print("=" * 80)

    fund_codes = set(fund_master["amfi_code"])

    nav_codes = set(nav_history["amfi_code"])

    missing_codes = fund_codes - nav_codes

    if not missing_codes:

        print("\nAll AMFI codes exist in NAV History.")

    else:

        print("\nMissing AMFI Codes")

        for code in sorted(missing_codes):
            print(code)

    return missing_codes


# ===========================================================
# DATA QUALITY & ANOMALY DETECTION
# ===========================================================

def detect_anomalies(
    dataset_name,
    df
):
    """
    Perform generic data quality checks
    on every dataset.
    """

    print("\n")
    print("=" * 80)
    print(f"DATA QUALITY CHECK : {dataset_name.upper()}")
    print("=" * 80)

    report = {}

    # -------------------------------------
    # Basic Information
    # -------------------------------------

    report["rows"] = df.shape[0]

    report["columns"] = df.shape[1]

    report["missing_values"] = (
        df.isnull().sum().sum()
    )

    report["duplicate_rows"] = (
        df.duplicated().sum()
    )

    report["memory_usage_mb"] = round(
        df.memory_usage(deep=True).sum() /
        (1024 * 1024),
        2
    )

    report["empty_dataset"] = df.empty

    # -------------------------------------
    # Duplicate AMFI Codes
    # -------------------------------------

    if "amfi_code" in df.columns:

        report["duplicate_amfi_codes"] = (
            df["amfi_code"]
            .duplicated()
            .sum()
        )

    else:

        report["duplicate_amfi_codes"] = "N/A"

    # -------------------------------------
    # Numeric Validation
    # -------------------------------------

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    negative_values = {}

    for column in numeric_columns:

        negative_count = (
            df[column] < 0
        ).sum()

        if negative_count > 0:

            negative_values[column] = int(
                negative_count
            )

    report["negative_values"] = negative_values

    # -------------------------------------
    # Date Validation
    # -------------------------------------

    invalid_dates = {}

    for column in df.columns:

        if "date" in column.lower():

            converted = pd.to_datetime(
                df[column],
                errors="coerce",
                dayfirst=True
            )

            invalid_dates[column] = int(
                converted.isna().sum()
            )

    report["invalid_dates"] = invalid_dates

    # -------------------------------------
    # Data Types
    # -------------------------------------

    report["data_types"] = (
        df.dtypes
        .astype(str)
        .to_dict()
    )

    # -------------------------------------
    # Console Summary
    # -------------------------------------

    print(f"Rows                 : {report['rows']}")
    print(f"Columns              : {report['columns']}")
    print(f"Missing Values       : {report['missing_values']}")
    print(f"Duplicate Rows       : {report['duplicate_rows']}")
    print(f"Memory Usage (MB)    : {report['memory_usage_mb']}")
    print(f"Empty Dataset        : {report['empty_dataset']}")

    if report["duplicate_amfi_codes"] != "N/A":

        print(
            f"Duplicate AMFI Codes : "
            f"{report['duplicate_amfi_codes']}"
        )

    if negative_values:

        print("\nNegative Numeric Values")

        for column, count in negative_values.items():

            print(f"{column} : {count}")

    else:

        print("Negative Numeric Values : None")

    if invalid_dates:

        print("\nInvalid Date Values")

        for column, count in invalid_dates.items():

            print(f"{column} : {count}")

    print()

    return report

# ===========================================================
# GENERATE DATA QUALITY REPORT
# ===========================================================

def generate_quality_report(
    datasets,
    missing_codes,
    anomaly_reports
):
    """
    Generate a detailed data quality report and save it
    to reports/data_quality_summary.txt
    """

    report_file = REPORT_PATH / "data_quality_summary.txt"

    with open(report_file, "w", encoding="utf-8") as f:

        f.write("=" * 80 + "\n")
        f.write("DATA QUALITY SUMMARY REPORT\n")
        f.write("=" * 80 + "\n\n")

        for dataset_name in datasets.keys():

            report = anomaly_reports[dataset_name]

            f.write(f"{dataset_name.upper()}\n")
            f.write("-" * 80 + "\n")

            f.write(f"Rows                 : {report['rows']}\n")
            f.write(f"Columns              : {report['columns']}\n")
            f.write(f"Missing Values       : {report['missing_values']}\n")
            f.write(f"Duplicate Rows       : {report['duplicate_rows']}\n")
            f.write(f"Memory Usage (MB)    : {report['memory_usage_mb']}\n")
            f.write(f"Empty Dataset        : {report['empty_dataset']}\n")
            f.write(f"Duplicate AMFI Codes : {report['duplicate_amfi_codes']}\n")

            # ---------------------------------
            # Negative Values
            # ---------------------------------

            if report["negative_values"]:

                f.write("\nNegative Values\n")

                for column, count in report["negative_values"].items():

                    f.write(
                        f"   {column} : {count}\n"
                    )

            else:

                f.write("Negative Values      : None\n")

            # ---------------------------------
            # Invalid Dates
            # ---------------------------------

            if report["invalid_dates"]:

                f.write("\nInvalid Dates\n")

                for column, count in report["invalid_dates"].items():

                    f.write(
                        f"   {column} : {count}\n"
                    )

            else:

                f.write("Invalid Dates        : None\n")

            f.write("\n")

        # ==================================================
        # AMFI VALIDATION SUMMARY
        # ==================================================

        f.write("=" * 80 + "\n")
        f.write("AMFI VALIDATION\n")
        f.write("=" * 80 + "\n")

        if not missing_codes:

            f.write("Status : PASSED\n")
            f.write("All AMFI Codes are present in NAV History.\n")

        else:

            f.write("Status : FAILED\n")
            f.write(
                f"Missing AMFI Codes : {len(missing_codes)}\n\n"
            )

            for code in sorted(missing_codes):

                f.write(f"{code}\n")

        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 80 + "\n")

    print("\n")
    print("=" * 80)
    print("DATA QUALITY REPORT GENERATED SUCCESSFULLY")
    print("=" * 80)
    print(f"Report Saved At : {report_file}")


# ===========================================================
# MAIN
# ===========================================================

def main():

    print("\n")
    print("=" * 80)
    print("MUTUAL FUND ANALYTICS PLATFORM")
    print("DAY 1 - DATA INGESTION & VALIDATION")
    print("=" * 80)

    # -------------------------------------
    # Load datasets
    # -------------------------------------

    datasets = load_datasets()

    # -------------------------------------
    # Explore Fund Master
    # -------------------------------------

    if "fund_master" in datasets:

        explore_fund_master(
            datasets["fund_master"]
        )

    # -------------------------------------
    # Validate AMFI Codes
    # -------------------------------------

    if (
        "fund_master" in datasets and
        "nav_history" in datasets
    ):

        missing_codes = validate_amfi_codes(
            datasets["fund_master"],
            datasets["nav_history"]
        )

    else:

        missing_codes = []

    # -------------------------------------
    # Perform Data Quality Checks
    # -------------------------------------

    anomaly_reports = {}

    for dataset_name, dataframe in datasets.items():

        anomaly_reports[
            dataset_name
        ] = detect_anomalies(
            dataset_name,
            dataframe
        )

    # -------------------------------------
    # Generate Report
    # -------------------------------------

    generate_quality_report(
        datasets,
        missing_codes,
        anomaly_reports
    )

    print("\n")
    print("=" * 80)
    print("DAY 1 DATA INGESTION COMPLETED SUCCESSFULLY")
    print("=" * 80)


# ===========================================================
# DRIVER CODE
# ===========================================================

if __name__ == "__main__":
    main()