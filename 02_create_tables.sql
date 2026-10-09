USE ecommerce_db;

CREATE TABLE IF NOT EXISTS ecommerce_events (
    event_id VARCHAR(100) NOT NULL,
    customer_id VARCHAR(100) NULL,
    session_id VARCHAR(100) NOT NULL,
    event_time DATETIME NULL,
    event_type VARCHAR(50) NOT NULL,
    product_id VARCHAR(100) NULL,
    product_name VARCHAR(255) NULL,
    category VARCHAR(100) NULL,
    price DECIMAL(12,2) NULL DEFAULT 0,
    quantity INT NULL DEFAULT 1,
    traffic_source VARCHAR(100) NULL,
    PRIMARY KEY (event_id)
);