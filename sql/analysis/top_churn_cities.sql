SELECT 
    city, 
    COUNT(*) as churned_customers 
FROM customer_analytics 
WHERE customer_status = 'Churned' 
GROUP BY city 
ORDER BY churned_customers DESC 
LIMIT 10;
