"""
===========================================================
Mutual Fund Analytics Platform
Day 2 - Database Loader

Author      : V Rohith
Internship  : Bluestock Fintech
===========================================================
"""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

from config import (
    PROCESSED_DATA_DIR,
    DATABASE_PATH,
    SQL_DIR
)

# ===========================================================
# DATABASE CONNECTION
# ===========================================================

engine = create_engine(f"sqlite:///{DATABASE_PATH}")

# ===========================================================
# CREATE DATABASE SCHEMA
# ===========================================================

def create_schema():

    print("=" * 80)
    print("CREATING DATABASE SCHEMA")
    print("=" * 80)

    schema_file = SQL_DIR / "schema.sql"

    with open(schema_file, "r", encoding="utf-8") as file:
        sql_script = file.read()

    with engine.begin() as connection:

        statements = sql_script.split(";")

        for statement in statements:

            statement = statement.strip()

            if statement:
                connection.execute(text(statement))

    print("✓ Database schema created.\n")


# ===========================================================
# LOAD DIMENSION TABLES
# ===========================================================

def load_dimension_tables():

    print("=" * 80)
    print("LOADING DIMENSION TABLES")
    print("=" * 80)

    # -------------------------
    # dim_fund
    # -------------------------

    fund_master = pd.read_csv(
        PROCESSED_DATA_DIR / "fund_master.csv"
    )

    fund_master.to_sql(
        "dim_fund",
        engine,
        if_exists="append",
        index=False
    )

    print("✓ dim_fund loaded")

    # -------------------------
    # dim_date
    # -------------------------

    nav = pd.read_csv(
        PROCESSED_DATA_DIR / "nav_history.csv"
    )

    nav["date"] = pd.to_datetime(nav["date"])

    dim_date = pd.DataFrame()

    dim_date["date"] = sorted(nav["date"].unique())

    dim_date["year"] = dim_date["date"].dt.year
    dim_date["quarter"] = dim_date["date"].dt.quarter
    dim_date["month"] = dim_date["date"].dt.month
    dim_date["month_name"] = dim_date["date"].dt.month_name()
    dim_date["day"] = dim_date["date"].dt.day
    dim_date["weekday"] = dim_date["date"].dt.day_name()

    dim_date.to_sql(
        "dim_date",
        engine,
        if_exists="append",
        index=False
    )

    print("✓ dim_date loaded\n")


# ===========================================================
# LOAD FACT TABLES
# ===========================================================

def load_fact_tables():

    print("=" * 80)
    print("LOADING FACT TABLES")
    print("=" * 80)

    table_mapping = {

        "nav_history.csv": "fact_nav",

        "investor_transactions.csv": "fact_transactions",

        "scheme_performance.csv": "fact_performance",

        "aum_by_fund_house.csv": "fact_aum"

    }

    for csv_file, table in table_mapping.items():

        df = pd.read_csv(
            PROCESSED_DATA_DIR / csv_file
        )

        df.to_sql(

            table,

            engine,

            if_exists="append",

            index=False

        )

        print(f"✓ {table} loaded")

    print()


# ===========================================================
# VERIFY ROW COUNTS
# ===========================================================

def verify_tables():

    print("=" * 80)
    print("VERIFYING DATABASE")
    print("=" * 80)

    tables = [

        "dim_fund",

        "dim_date",

        "fact_nav",

        "fact_transactions",

        "fact_performance",

        "fact_aum"

    ]

    with engine.connect() as connection:

        for table in tables:

            rows = connection.execute(

                text(
                    f"SELECT COUNT(*) FROM {table}"
                )

            ).scalar()

            print(f"{table:<25} {rows}")

    print()


# ===========================================================
# MAIN
# ===========================================================

def main():

    print("=" * 80)
    print("DAY 2 DATABASE LOADER")
    print("=" * 80)

    create_schema()

    load_dimension_tables()

    load_fact_tables()

    verify_tables()

    print("=" * 80)
    print("DATABASE CREATED SUCCESSFULLY")
    print("=" * 80)

    print(f"\nDatabase Location:\n{DATABASE_PATH}")


# ===========================================================
# DRIVER
# ===========================================================

if __name__ == "__main__":
    main()