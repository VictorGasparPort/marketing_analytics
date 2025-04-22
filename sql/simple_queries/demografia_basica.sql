-- Query: Análise Demográfica Básica
/* Propósito: Relatório rápido de perfil de clientes */
SELECT 
    CASE 
        WHEN Age BETWEEN 18 AND 35 THEN '18-35'
        WHEN Age BETWEEN 36 AND 55 THEN '36-55'
        ELSE '56+'
    END AS age_group,
    AVG(MntTotal) AS avg_spending,
    COUNT(*) FILTER (WHERE Response = 1) * 100.0 / COUNT(*) AS campaign_response_rate
FROM main_table
GROUP BY 1
ORDER BY 1;
