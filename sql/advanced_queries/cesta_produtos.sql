-- Query: Análise de Cesta de Produtos
SELECT 
    product_combination,
    COUNT(*) AS total_customers,
    AVG(Income) AS avg_income,
    CORR(MntWines, MntMeatProducts) AS wine_meat_corr
FROM (
    SELECT 
        Customer_ID,
        ARRAY_TO_STRING(ARRAY[
            CASE WHEN MntWines > 500 THEN 'Wine' END,
            CASE WHEN MntMeatProducts > 300 THEN 'Meat' END,
            CASE WHEN MntSweetProducts > 100 THEN 'Sweets' END
        ], ', ') AS product_combination
    FROM main_table
) combos
GROUP BY 1
HAVING COUNT(*) > 10;
-- Identifica combinações de produtos mais comuns para cross-selling