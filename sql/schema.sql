-- ============================================================
-- Mutual Fund Analytics Platform
-- SQLite Star Schema
--
-- Author      : V Rohith
-- Internship  : Bluestock Fintech
-- ============================================================

PRAGMA foreign_keys = ON;

-- ============================================================
-- DIMENSION TABLE : FUND
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_fund (

    amfi_code INTEGER PRIMARY KEY,

    fund_house TEXT NOT NULL,

    scheme_name TEXT NOT NULL,

    category TEXT,

    sub_category TEXT,

    plan TEXT,

    launch_date DATE,

    benchmark TEXT,

    expense_ratio_pct REAL,

    exit_load_pct REAL,

    min_sip_amount INTEGER,

    min_lumpsum_amount INTEGER,

    fund_manager TEXT,

    risk_category TEXT,

    sebi_category_code TEXT

);

-- ============================================================
-- DIMENSION TABLE : DATE
-- ============================================================

CREATE TABLE IF NOT EXISTS dim_date (

    date DATE PRIMARY KEY,

    year INTEGER,

    quarter INTEGER,

    month INTEGER,

    month_name TEXT,

    day INTEGER,

    weekday TEXT

);

-- ============================================================
-- FACT TABLE : NAV HISTORY
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER NOT NULL,

    date DATE NOT NULL,

    nav REAL NOT NULL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date)
        REFERENCES dim_date(date)

);

-- ============================================================
-- FACT TABLE : INVESTOR TRANSACTIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_transactions (

    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    investor_id TEXT,

    transaction_date DATE,

    amfi_code INTEGER,

    transaction_type TEXT,

    amount_inr REAL,

    state TEXT,

    city TEXT,

    city_tier TEXT,

    age_group TEXT,

    gender TEXT,

    annual_income_lakh REAL,

    payment_mode TEXT,

    kyc_status TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (transaction_date)
        REFERENCES dim_date(date)

);

-- ============================================================
-- FACT TABLE : SCHEME PERFORMANCE
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_performance (

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER,

    return_1yr_pct REAL,

    return_3yr_pct REAL,

    return_5yr_pct REAL,

    benchmark_3yr_pct REAL,

    alpha REAL,

    beta REAL,

    sharpe_ratio REAL,

    sortino_ratio REAL,

    std_dev_ann_pct REAL,

    max_drawdown_pct REAL,

    aum_crore REAL,

    expense_ratio_pct REAL,

    morningstar_rating INTEGER,

    risk_grade TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)

);

-- ============================================================
-- FACT TABLE : AUM
-- ============================================================

CREATE TABLE IF NOT EXISTS fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date DATE,

    fund_house TEXT,

    aum_lakh_crore REAL,

    aum_crore REAL,

    num_schemes INTEGER,

    FOREIGN KEY (date)
        REFERENCES dim_date(date)

);