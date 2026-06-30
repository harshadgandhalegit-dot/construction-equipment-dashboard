-- ============================================================
-- queries.sql
-- SQL queries used to consolidate and analyze construction
-- equipment sales data for the Power BI dashboard.
-- Tools: MySQL / PostgreSQL
-- ============================================================

-- 1. Create table structure
CREATE TABLE equipment_sales (
    sale_date       DATE,
    division        VARCHAR(50),
    region          VARCHAR(50),
    product_model   VARCHAR(100),
    units_sold      INT,
    revenue_inr     NUMERIC(15,2),
    cost_inr        NUMERIC(15,2),
    dealer_name     VARCHAR(100)
);

-- 2. Division-wise revenue and profit summary
SELECT
    division,
    SUM(units_sold)                         AS total_units,
    SUM(revenue_inr)                        AS total_revenue,
    SUM(revenue_inr - cost_inr)             AS total_profit,
    ROUND(AVG((revenue_inr - cost_inr) / revenue_inr) * 100, 2) AS avg_margin_pct
FROM equipment_sales
GROUP BY division
ORDER BY total_revenue DESC;

-- 3. Region-wise performance using CTE
WITH region_perf AS (
    SELECT
        region,
        division,
        SUM(revenue_inr) AS revenue,
        SUM(units_sold)  AS units
    FROM equipment_sales
    GROUP BY region, division
)
SELECT
    region,
    division,
    revenue,
    units,
    RANK() OVER (PARTITION BY region ORDER BY revenue DESC) AS division_rank
FROM region_perf
ORDER BY region, division_rank;

-- 4. Month-over-month revenue trend using window function
SELECT
    division,
    DATE_TRUNC('month', sale_date) AS sales_month,
    SUM(revenue_inr) AS monthly_revenue,
    LAG(SUM(revenue_inr)) OVER (
        PARTITION BY division ORDER BY DATE_TRUNC('month', sale_date)
    ) AS prev_month_revenue
FROM equipment_sales
GROUP BY division, DATE_TRUNC('month', sale_date)
ORDER BY division, sales_month;

-- 5. Top-performing dealer per division
SELECT division, dealer_name, total_revenue
FROM (
    SELECT
        division,
        dealer_name,
        SUM(revenue_inr) AS total_revenue,
        ROW_NUMBER() OVER (PARTITION BY division ORDER BY SUM(revenue_inr) DESC) AS rn
    FROM equipment_sales
    GROUP BY division, dealer_name
) ranked
WHERE rn = 1;

-- 6. View for Power BI direct query (division summary)
CREATE VIEW vw_division_summary AS
SELECT
    division,
    SUM(units_sold)             AS total_units,
    SUM(revenue_inr)            AS total_revenue,
    SUM(revenue_inr - cost_inr) AS total_profit
FROM equipment_sales
GROUP BY division;
