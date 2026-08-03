"""
===========================================================
Mutual Fund Analytics Platform
Configuration File

Author      : V Rohith
Internship  : Bluestock Fintech
===========================================================
"""

from pathlib import Path

# ===========================================================
# PROJECT ROOT
# ===========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# ===========================================================
# DATA DIRECTORIES
# ===========================================================

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "Provided_Data"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

LIVE_NAV_DIR = PROJECT_ROOT / "data" / "raw" / "Generated_data_from_MFAPI"

# ===========================================================
# REPORTS
# ===========================================================

REPORTS_DIR = PROJECT_ROOT / "reports"

# ===========================================================
# SQL
# ===========================================================

SQL_DIR = PROJECT_ROOT / "sql"

# ===========================================================
# DATABASE
# ===========================================================

DATABASE_PATH = PROJECT_ROOT / "bluestock_mf.db"

# ===========================================================
# CREATE DIRECTORIES IF NOT PRESENT
# ===========================================================

PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

SQL_DIR.mkdir(parents=True, exist_ok=True)