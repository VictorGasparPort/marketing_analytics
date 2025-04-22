-- Índice: Filtragem por Comportamento de Compra
CREATE INDEX idx_purchase_behavior ON main_table 
    (NumWebPurchases, NumCatalogPurchases, NumStorePurchases)
INCLUDE (Recency, MntWines);
-- Motivo: Consultas combinadas de canais de compra com dados relacionados