-- Índice: Pesquisa de Clientes de Alto Valor
CREATE INDEX idx_high_value ON main_table (Income, MntTotal)
WHERE MntTotal > 1000 AND NumStorePurchases > 5;
-- Motivo: Acelera consultas frequentes para clientes Premium