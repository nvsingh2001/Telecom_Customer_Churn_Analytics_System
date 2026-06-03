SELECT 
    SUM(total_charges) as total_revenue_lost 
FROM customer_analytics 
WHERE customer_status = 'Churned';
