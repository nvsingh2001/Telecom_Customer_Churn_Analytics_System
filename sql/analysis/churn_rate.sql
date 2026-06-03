SELECT 
    (COUNT(CASE WHEN customer_status = 'Churned' THEN 1 END) * 100.0 / COUNT(*)) as churn_rate 
FROM customer_analytics;
