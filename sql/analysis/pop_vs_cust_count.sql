SELECT 
    zip_code, 
    MAX(population) as population, 
    COUNT(*) as customer_count 
FROM customer_analytics 
GROUP BY zip_code 
ORDER BY customer_count DESC 
LIMIT 10;
