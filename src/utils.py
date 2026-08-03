"""
===========================================================
Mutual Fund Analytics Platform
Utility Functions

Author      : V Rohith
Internship  : Bluestock Fintech
===========================================================
"""

import pandas as pd
from pathlib import Path
from config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    REPORTS_DIR
)

# ===========================================================
# LOAD DATASET
# ===========================================================

def load_dataset(filename):
    """
    Load a CSV dataset from the raw data folder.
    """

    file_path = RAW_DATA_DIR / filename

    try:

        df = pd.read_csv(file_path)

        print(f"✓ Loaded {filename}")

        return df

    except FileNotFoundError:

        print(f"✗ File not found : {filename}")

    except Exception as e:

        print(f"Error loading {filename}")
        print(e)

    return None


# ===========================================================
# SAVE DATASET
# ===========================================================

def save_dataset(df, filename):
    """
    Save cleaned dataset into processed folder.
    """

    output_path = PROCESSED_DATA_DIR / filename

    df.to_csv(
        output_path,
        index=False
    )

    print(f"✓ Saved {filename}")


# ===========================================================
# REMOVE DUPLICATES
# ===========================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    removed = before - after

    return df, removed


# ===========================================================
# REMOVE WHITESPACES
# ===========================================================

def clean_text_columns(df):

    text_columns = df.select_dtypes(include="object").columns

    for column in text_columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )

    return df


# ===========================================================
# CONVERT DATE COLUMNS
# ===========================================================

def convert_date_columns(df):

    for column in df.columns:

        if "date" in column.lower():

            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    return df


# ===========================================================
# MISSING VALUE SUMMARY
# ===========================================================

def missing_value_summary(df):

    missing = df.isnull().sum()

    missing = missing[missing > 0]

    return missing.to_dict()


# ===========================================================
# VALIDATE POSITIVE COLUMN
# ===========================================================

def validate_positive(df, column):

    before = len(df)

    df = df[df[column] > 0]

    removed = before - len(df)

    return df, removed


# ===========================================================
# LOG REPORT
# ===========================================================

def append_report(report_lines, dataset_name,
                  before_rows,
                  after_rows,
                  duplicates_removed,
                  missing_values):

    report_lines.append("=" * 60)

    report_lines.append(dataset_name.upper())

    report_lines.append("=" * 60)

    report_lines.append(f"Rows Before           : {before_rows}")

    report_lines.append(f"Rows After            : {after_rows}")

    report_lines.append(
        f"Duplicates Removed    : {duplicates_removed}"
    )

    report_lines.append(
        f"Missing Values        : {missing_values}"
    )

    report_lines.append("")


# ===========================================================
# WRITE REPORT
# ===========================================================

def write_report(report_lines):

    report_path = REPORTS_DIR / "data_cleaning_report.txt"

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write("\n".join(report_lines))

    print()

    print("=" * 60)

    print("DATA CLEANING REPORT GENERATED")

    print(report_path)

    print("=" * 60)