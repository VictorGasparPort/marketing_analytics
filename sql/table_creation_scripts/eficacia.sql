
-- Tabela: Eficácia de Campanhas por Perfil Demográfico
CREATE TABLE campaign_performance (
    campaign_id INT,
    marital_status VARCHAR(20),
    education_level VARCHAR(20),
    acceptance_rate NUMERIC(5,2),
    cost_per_conversion NUMERIC(10,2)
);
/* Propósito: Otimizar alocação de orçamento de marketing */
INSERT INTO campaign_performance
SELECT 
    campaign,
    CASE 
        WHEN marital_Married = 1 THEN 'Casado'
        WHEN marital_Single = 1 THEN 'Solteiro'
        ELSE 'Outro'
    END AS marital_status,
    CASE 
        WHEN education_PhD = 1 THEN 'Doutorado'
        WHEN education_Master = 1 THEN 'Mestrado'
        ELSE 'Graduação ou menos'
    END AS education_level,
    AVG(AcceptedCmp) * 100 AS acceptance_rate,
    Z_CostContact / COUNT(NULLIF(AcceptedCmp,0)) AS cost_per_conversion
FROM (
    SELECT unnest(ARRAY[1,2,3,4,5]) AS campaign,
    AcceptedCmp1, AcceptedCmp2, AcceptedCmp3, AcceptedCmp4, AcceptedCmp5,
    marital_Married, marital_Single, education_PhD, education_Master, Z_CostContact
    FROM main_table
) expanded
GROUP BY 1,2,3;
