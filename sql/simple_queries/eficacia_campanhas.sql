-- Query: Eficiência de Campanhas
/* Propósito: Avaliação rápida de performance de marketing */
SELECT 
    'Campanha ' || campaign AS campaign_name,
    SUM(AcceptedCmp) AS conversions,
    ROUND(SUM(Z_CostContact)/SUM(AcceptedCmp), 2) AS cost_per_conversion
FROM (
    SELECT 
        1 AS campaign, AcceptedCmp1 AS AcceptedCmp, Z_CostContact FROM main_table
    UNION ALL
    SELECT 2, AcceptedCmp2, Z_CostContact FROM main_table
    -- Repetir para demais campanhas...
) campaigns
GROUP BY 1
ORDER BY conversions DESC;