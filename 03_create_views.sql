USE ecommerce_db;

DROP VIEW IF EXISTS funnel_summary;
CREATE VIEW funnel_summary AS
SELECT
    event_type,
    COUNT(DISTINCT session_id) AS total_sessions,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(*) AS total_events
FROM ecommerce_events
GROUP BY event_type;

DROP VIEW IF EXISTS product_performance;
CREATE VIEW product_performance AS
SELECT
    product_id,
    product_name,
    category,
    COUNT(*) AS total_events,
    SUM(CASE WHEN event_type = 'purchase'
             THEN COALESCE(price, 0) * COALESCE(quantity, 0)
             ELSE 0 END) AS revenue
FROM ecommerce_events
GROUP BY product_id, product_name, category;

DROP VIEW IF EXISTS traffic_source_performance;
CREATE VIEW traffic_source_performance AS
SELECT
    traffic_source,
    COUNT(DISTINCT session_id) AS sessions,
    COUNT(DISTINCT CASE WHEN event_type = 'purchase' THEN session_id END) AS purchasing_sessions,
    SUM(CASE WHEN event_type = 'purchase'
             THEN COALESCE(price, 0) * COALESCE(quantity, 0)
             ELSE 0 END) AS revenue
FROM ecommerce_events
GROUP BY traffic_source;
USE ecommerce_db;

SELECT COUNT(*) AS total_rows FROM ecommerce_events;
SELECT * FROM ecommerce_events LIMIT 20;
SELECT * FROM funnel_summary;
SELECT * FROM product_performance;
SELECT * FROM traffic_source_performance;