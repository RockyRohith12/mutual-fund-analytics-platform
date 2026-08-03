# Mutual Fund Analytics Platform

## Data Dictionary

**Author:** V Rohith  
**Internship:** Bluestock Fintech

---

# 1. fund_master.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | Unique AMFI scheme code |
| fund_house | TEXT | Name of Asset Management Company (AMC) |
| scheme_name | TEXT | Mutual fund scheme name |
| category | TEXT | Mutual fund category |
| sub_category | TEXT | Mutual fund sub-category |
| plan | TEXT | Growth / IDCW plan |
| launch_date | DATE | Scheme launch date |
| benchmark | TEXT | Benchmark index |
| expense_ratio_pct | REAL | Expense ratio (%) |
| exit_load_pct | REAL | Exit load (%) |
| min_sip_amount | INTEGER | Minimum SIP investment |
| min_lumpsum_amount | INTEGER | Minimum lump sum investment |
| fund_manager | TEXT | Fund manager name |
| risk_category | TEXT | Risk classification |
| sebi_category_code | TEXT | SEBI category code |

---

# 2. nav_history.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | AMFI scheme code |
| date | DATE | NAV date |
| nav | REAL | Net Asset Value |

---

# 3. aum_by_fund_house.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| date | DATE | Reporting date |
| fund_house | TEXT | AMC name |
| aum_lakh_crore | REAL | AUM in lakh crore |
| aum_crore | REAL | AUM in crore |
| num_schemes | INTEGER | Number of schemes |

---

# 4. monthly_sip_inflows.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| month | TEXT | Month |
| sip_inflow_crore | INTEGER | SIP inflow |
| active_sip_accounts_crore | REAL | Active SIP accounts |
| new_sip_accounts_lakh | REAL | New SIP accounts |
| sip_aum_lakh_crore | REAL | SIP AUM |
| yoy_growth_pct | REAL | Year-over-year growth |

---

# 5. category_inflows.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| month | TEXT | Reporting month |
| category | TEXT | Mutual fund category |
| net_inflow_crore | REAL | Net inflow |

---

# 6. industry_folio_count.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| month | TEXT | Reporting month |
| total_folios_crore | REAL | Total folios |
| equity_folios_crore | REAL | Equity folios |
| debt_folios_crore | REAL | Debt folios |
| hybrid_folios_crore | REAL | Hybrid folios |
| others_folios_crore | REAL | Other folios |

---

# 7. scheme_performance.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | AMFI scheme code |
| scheme_name | TEXT | Scheme name |
| fund_house | TEXT | Fund house |
| category | TEXT | Category |
| plan | TEXT | Plan type |
| return_1yr_pct | REAL | 1-year return |
| return_3yr_pct | REAL | 3-year return |
| return_5yr_pct | REAL | 5-year return |
| benchmark_3yr_pct | REAL | Benchmark return |
| alpha | REAL | Alpha |
| beta | REAL | Beta |
| sharpe_ratio | REAL | Sharpe ratio |
| sortino_ratio | REAL | Sortino ratio |
| std_dev_ann_pct | REAL | Annualized standard deviation |
| max_drawdown_pct | REAL | Maximum drawdown |
| aum_crore | REAL | Assets under management |
| expense_ratio_pct | REAL | Expense ratio |
| morningstar_rating | INTEGER | Morningstar rating |
| risk_grade | TEXT | Risk grade |

---

# 8. investor_transactions.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| investor_id | TEXT | Investor ID |
| transaction_date | DATE | Transaction date |
| amfi_code | INTEGER | AMFI scheme code |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | REAL | Investment amount |
| state | TEXT | Investor state |
| city | TEXT | Investor city |
| city_tier | TEXT | Tier classification |
| age_group | TEXT | Age group |
| gender | TEXT | Gender |
| annual_income_lakh | REAL | Annual income |
| payment_mode | TEXT | Payment mode |
| kyc_status | TEXT | KYC status |

---

# 9. portfolio_holdings.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| amfi_code | INTEGER | AMFI scheme code |
| stock_symbol | TEXT | NSE/BSE symbol |
| stock_name | TEXT | Company name |
| sector | TEXT | Industry sector |
| weight_pct | REAL | Portfolio weight |
| market_value_cr | REAL | Market value |
| current_price_inr | REAL | Current stock price |
| portfolio_date | DATE | Portfolio reporting date |

---

# 10. benchmark_indices.csv

| Column | Data Type | Description |
|---------|-----------|-------------|
| date | DATE | Trading date |
| index_name | TEXT | Benchmark index |
| close_value | REAL | Closing value |

---

## Source

All datasets were provided as part of the Bluestock Mutual Fund Analytics Internship project.