SELECT 
    CASE 
        WHEN tenure < 12 THEN '0-1 year'
        WHEN tenure < 24 THEN '1-2 years'
        WHEN tenure < 36 THEN '2-3 years'
        WHEN tenure < 48 THEN '3-4 years'
        WHEN tenure < 60 THEN '4-5 years'
        ELSE '5+ years'
    END as tenure_group,
    COUNT(*) as churned_customers
FROM customer_analytics
WHERE customer_status = 'Churned'
GROUP BY tenure_group
ORDER BY tenure_group;
