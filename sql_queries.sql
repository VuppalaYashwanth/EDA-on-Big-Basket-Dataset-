-- =============================================
-- BIGBASKET SALES & PRICING ANALYSIS
-- SQL Queries for Retail Analytics
-- =============================================

-- 1. CATEGORY-WISE SALES ANALYSIS
-- Total revenue, units sold, and average order value by category
SELECT 
    p.category,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS total_revenue,
    SUM(t.discount_amount) AS total_discount,
    ROUND(AVG(t.total_amount), 2) AS avg_order_value,
    ROUND(SUM(t.discount_amount) / SUM(t.total_amount) * 100, 2) AS avg_discount_rate
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- 2. MONTHLY SALES TREND ANALYSIS
-- Track sales performance month-over-month
SELECT 
    DATE_FORMAT(STR_TO_DATE(t.date, '%Y-%m-%d'), '%Y-%m') AS month,
    COUNT(DISTINCT t.transaction_id) AS total_transactions,
    SUM(t.quantity) AS total_units,
    SUM(t.total_amount) AS revenue,
    SUM(t.discount_amount) AS total_discount,
    ROUND(AVG(t.total_amount), 2) AS avg_transaction_value
FROM transactions t
GROUP BY month
ORDER BY month;

-- 3. TOP 10 BEST SELLING PRODUCTS
-- Products with highest revenue contribution
SELECT 
    p.product_name,
    p.category,
    p.sub_category,
    p.brand,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS total_revenue,
    ROUND(AVG(p.rating), 2) AS avg_rating,
    p.discount_percent
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category, p.sub_category, p.brand, p.rating, p.discount_percent
ORDER BY total_revenue DESC
LIMIT 10;

-- 4. DISCOUNT IMPACT ANALYSIS
-- Analyze relationship between discount and sales volume
SELECT 
    CASE 
        WHEN p.discount_percent = 0 THEN 'No Discount'
        WHEN p.discount_percent <= 10 THEN '1-10%'
        WHEN p.discount_percent <= 20 THEN '11-20%'
        ELSE '20%+'
    END AS discount_bracket,
    COUNT(DISTINCT t.transaction_id) AS transactions,
    SUM(t.quantity) AS total_units_sold,
    SUM(t.total_amount) AS revenue,
    ROUND(AVG(t.quantity), 2) AS avg_units_per_order,
    ROUND(SUM(t.total_amount) / COUNT(DISTINCT t.transaction_id), 2) AS revenue_per_order
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY discount_bracket
ORDER BY 
    CASE discount_bracket
        WHEN 'No Discount' THEN 1
        WHEN '1-10%' THEN 2
        WHEN '11-20%' THEN 3
        ELSE 4
    END;

-- 5. REGIONAL PERFORMANCE ANALYSIS
-- Sales distribution across different regions
SELECT 
    t.region,
    COUNT(DISTINCT t.transaction_id) AS total_orders,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_order_value,
    ROUND(SUM(t.total_amount) / (SELECT SUM(total_amount) FROM transactions) * 100, 2) AS revenue_share_pct
FROM transactions t
GROUP BY t.region
ORDER BY revenue DESC;

-- 6. BRAND PERFORMANCE COMPARISON
-- Top performing brands by revenue
SELECT 
    p.brand,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS total_revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_sale_price,
    ROUND(AVG(p.rating), 2) AS avg_product_rating
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY p.brand
ORDER BY total_revenue DESC;

-- 7. SUB-CATEGORY DEEP DIVE
-- Detailed performance by sub-category
SELECT 
    p.category,
    p.sub_category,
    COUNT(DISTINCT t.transaction_id) AS transactions,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS revenue,
    SUM(t.discount_amount) AS total_discount,
    ROUND(AVG(p.discount_percent), 2) AS avg_discount_pct,
    ROUND(AVG(p.rating), 2) AS avg_rating
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY p.category, p.sub_category
ORDER BY revenue DESC
LIMIT 20;

-- 8. WEEKLY PERFORMANCE COMPARISON
-- Week-over-week sales trends
SELECT 
    YEARWEEK(STR_TO_DATE(t.date, '%Y-%m-%d')) AS year_week,
    MIN(t.date) AS week_start,
    MAX(t.date) AS week_end,
    COUNT(DISTINCT t.transaction_id) AS transactions,
    SUM(t.total_amount) AS revenue,
    ROUND(AVG(t.total_amount), 2) AS avg_order_value
FROM transactions t
GROUP BY year_week
ORDER BY year_week;

-- 9. PRICE POINT ANALYSIS
-- Revenue distribution by price ranges
SELECT 
    CASE 
        WHEN p.sale_price < 50 THEN 'Under ₹50'
        WHEN p.sale_price < 100 THEN '₹50-100'
        WHEN p.sale_price < 200 THEN '₹100-200'
        WHEN p.sale_price < 500 THEN '₹200-500'
        ELSE 'Above ₹500'
    END AS price_range,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS total_revenue,
    ROUND(AVG(t.quantity), 2) AS avg_quantity_per_order
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY price_range
ORDER BY 
    CASE price_range
        WHEN 'Under ₹50' THEN 1
        WHEN '₹50-100' THEN 2
        WHEN '₹100-200' THEN 3
        WHEN '₹200-500' THEN 4
        ELSE 5
    END;

-- 10. HIGH-VALUE CUSTOMER TRANSACTIONS
-- Identify premium transactions
SELECT 
    t.transaction_id,
    t.date,
    t.customer_id,
    t.region,
    p.product_name,
    p.category,
    t.quantity,
    t.total_amount,
    t.discount_amount
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
WHERE t.total_amount > (SELECT AVG(total_amount) * 2 FROM transactions)
ORDER BY t.total_amount DESC
LIMIT 50;

-- 11. PRODUCT RATING vs SALES CORRELATION
-- Analyze if higher-rated products sell more
SELECT 
    CASE 
        WHEN p.rating < 3.5 THEN 'Low (< 3.5)'
        WHEN p.rating < 4.0 THEN 'Medium (3.5-4.0)'
        WHEN p.rating < 4.5 THEN 'High (4.0-4.5)'
        ELSE 'Very High (4.5+)'
    END AS rating_category,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(t.quantity) AS units_sold,
    SUM(t.total_amount) AS revenue,
    ROUND(AVG(t.quantity), 2) AS avg_units_per_transaction
FROM transactions t
INNER JOIN products p ON t.product_id = p.product_id
GROUP BY rating_category
ORDER BY 
    CASE rating_category
        WHEN 'Low (< 3.5)' THEN 1
        WHEN 'Medium (3.5-4.0)' THEN 2
        WHEN 'High (4.0-4.5)' THEN 3
        ELSE 4
    END;

-- 12. REVENUE CONTRIBUTION ANALYSIS (Pareto Principle)
-- Identify products contributing to 80% of revenue
WITH product_revenue AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(t.total_amount) AS revenue,
        SUM(SUM(t.total_amount)) OVER (ORDER BY SUM(t.total_amount) DESC) AS cumulative_revenue,
        (SELECT SUM(total_amount) FROM transactions) AS total_revenue
    FROM transactions t
    INNER JOIN products p ON t.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    product_id,
    product_name,
    category,
    revenue,
    ROUND(revenue / total_revenue * 100, 2) AS revenue_pct,
    ROUND(cumulative_revenue / total_revenue * 100, 2) AS cumulative_revenue_pct
FROM product_revenue
WHERE cumulative_revenue / total_revenue <= 0.8
ORDER BY revenue DESC;
