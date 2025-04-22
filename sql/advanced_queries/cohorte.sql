-- Query: Análise de Cohorte por Canal de Compra
WITH CohortAnalysis AS (
    /* Propósito: Entender padrões de compra ao longo do tempo */
    SELECT 
        EXTRACT(YEAR FROM Customer_Enrollment_Date) AS cohort_year,
        CASE 
            WHEN NumWebPurchases > NumStorePurchases THEN 'Digital'
            WHEN NumCatalogPurchases > 3 THEN 'Catálogo'
            ELSE 'Loja Física'
        END AS primary_channel,
        AVG(MntTotal) OVER (PARTITION BY cohort_year 
            ORDER BY Customer_Days ROWS BETWEEN 30 PRECEDING AND CURRENT ROW) AS rolling_spend,
        CORR(NumWebVisitsMonth, NumWebPurchases) AS web_engagement_corr
    FROM main_table
)
SELECT 
    cohort_year,
    primary_channel,
    AVG(rolling_spend) AS avg_3month_spend,
    web_engagement_corr
FROM CohortAnalysis
GROUP BY 1,2,web_engagement_corr
HAVING COUNT(*) > 30;
