DROP TABLE IF EXISTS customer_analytics;

CREATE TABLE customer_analytics 
DISTKEY (zip_code)
SORTKEY (customer_id, customer_status)
AS
SELECT 
    c.customer_id,
    c.city,
    c.zip_code,
    z.population,
    c.tenure,
    c.monthly_charges,
    c.total_charges,
    c.customer_status
FROM customer_churn c
JOIN zip_population z ON c.zip_code = z.zip_code;
