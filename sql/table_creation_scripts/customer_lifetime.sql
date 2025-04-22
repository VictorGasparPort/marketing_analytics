-- Tabela: Customer Lifetime Value (CLV)
CREATE TABLE clv_analysis AS
/* Propósito: Calcular valor vitalício para priorizar retenção */
SELECT 
    Customer_ID,
    MntTotal / (Customer_Days/365.25) AS annual_spending,
    (MntTotal * 0.35) / (1 - POWER(0.85, Customer_Days/365.25)) AS predicted_clv,
    CASE 
        WHEN Complain = 1 THEN RANK() OVER (ORDER BY Customer_Days DESC)
        ELSE NULL 
    END AS retention_priority
FROM main_table
WHERE Customer_Days > 365;
-- Fórmula CLV adaptada: Considera taxa de desconto de 15% anual e margem de 35%