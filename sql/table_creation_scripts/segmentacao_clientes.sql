-- Tabela: Segmentação de Clientes por Valor e Engajamento
CREATE TABLE customer_segments AS
/* Propósito: Classificar clientes para estratégias de marketing personalizadas */
SELECT 
    Customer_ID,
    CASE 
        WHEN MntTotal > 1500 AND NumStorePurchases > 8 THEN 'Premium'
        WHEN MntTotal BETWEEN 500 AND 1500 AND AcceptedCmpOverall >= 2 THEN 'Loyal'
        WHEN Recency < 30 AND NumWebVisitsMonth > 5 THEN 'Ativo'
        ELSE 'Oportunidade'
    END AS segment,
    NTILE(5) OVER (ORDER BY MntTotal DESC) AS spending_tier,
    (MntWines * 0.4 + MntMeatProducts * 0.3 + MntSweetProducts * 0.3) AS food_score
FROM main_table;
-- Explicação: Cria grupos estratégicos baseados em gastos, canais de compra e engajamento
