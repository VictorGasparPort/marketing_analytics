-- Query: Análise de Reclamações
/* Propósito: Monitoramento de satisfação do cliente */
SELECT 
    CASE 
        WHEN Kidhome + Teenhome > 2 THEN 'Família Grande'
        ELSE 'Família Pequena'
    END AS family_size,
    AVG(Recency) AS avg_recency,
    COUNT(*) FILTER (WHERE Complain = 1) * 100.0 / COUNT(*) AS complaint_rate
FROM main_table
GROUP BY 1;