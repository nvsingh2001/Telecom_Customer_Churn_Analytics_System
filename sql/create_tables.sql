CREATE TABLE IF NOT EXISTS customer_churn (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    city VARCHAR(100),
    zip_code VARCHAR(10),
    tenure INT,
    monthly_charges DECIMAL(10, 2),
    total_charges DECIMAL(10, 2),
    customer_status VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS zip_population (
    zip_code VARCHAR(10) PRIMARY KEY,
    population INT
);
