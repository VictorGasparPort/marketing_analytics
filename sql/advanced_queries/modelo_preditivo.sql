-- Query: Modelo Preditivo de Aceitação de Campanha
/* Propósito: Prever probabilidade de aceitação usando dados históricos */
SELECT 
    Customer_ID,
    1/(1+EXP(-(
        0.5*(MntTotal/1000) + 
        0.3*(NumDealsPurchases/5) - 
        0.2*(Recency/30) + 
        0.4*(CASE WHEN education_PhD = 1 THEN 1 ELSE 0 END)
    )) AS acceptance_probability,
    NTILE(4) OVER (ORDER BY (MntTotal/1000 + NumDealsPurchases/5) DESC) AS target_group
FROM main_table
WHERE Complain = 0;
-- Fórmula inspirada em regressão logística usando variáveis-chave
