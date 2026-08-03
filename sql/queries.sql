-- ============================================================
-- Mutual Fund Analytics Platform
-- Analytical SQL Queries
--
-- Author : V Rohith
-- Internship : Bluestock Fintech
-- ============================================================


---------------------------------------------------------------
-- 1. Top 5 Funds by Assets Under Management (AUM)
---------------------------------------------------------------

SELECT
    fund_house,
    aum_crore
FROM fact_aum
ORDER BY aum_crore DESC
LIMIT 5;


---------------------------------------------------------------
-- 2. Average NAV for each Mutual Fund
---------------------------------------------------------------

SELECT
    amfi_code,
    ROUND(AVG(nav),2) AS average_nav
FROM fact_nav
GROUP BY amfi_code
ORDER BY average_nav DESC;


---------------------------------------------------------------
-- 3. Monthly Average NAV
---------------------------------------------------------------

SELECT
    strftime('%Y-%m',date) AS month,
    ROUND(AVG(nav),2) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;


---------------------------------------------------------------
-- 4. Number of Transactions by State
---------------------------------------------------------------

SELECT
    state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


---------------------------------------------------------------
-- 5. Funds having Expense Ratio less than 1%
---------------------------------------------------------------

SELECT
    scheme_name,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;


---------------------------------------------------------------
-- 6. Top Performing Funds (5 Year Return)
---------------------------------------------------------------

SELECT
    amfi_code,
    return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 10;


---------------------------------------------------------------
-- 7. Highest Sharpe Ratio Funds
---------------------------------------------------------------

SELECT
    amfi_code,
    sharpe_ratio
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 10;


---------------------------------------------------------------
-- 8. Average Investment Amount by Transaction Type
---------------------------------------------------------------

SELECT
    transaction_type,
    ROUND(AVG(amount_inr),2) AS average_amount
FROM fact_transactions
GROUP BY transaction_type;


---------------------------------------------------------------
-- 9. Gender-wise Investment Amount
---------------------------------------------------------------

SELECT
    gender,
    ROUND(SUM(amount_inr),2) AS total_amount
FROM fact_transactions
GROUP BY gender;


---------------------------------------------------------------
-- 10. Risk Grade Distribution
---------------------------------------------------------------

SELECT
    risk_grade,
    COUNT(*) AS total_funds
FROM fact_performance
GROUP BY risk_grade
ORDER BY total_funds DESC;