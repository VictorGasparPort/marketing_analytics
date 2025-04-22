-- Particionamento: Segmentação por Categoria de Produto
CREATE TABLE main_table_partitioned PARTITION BY RANGE (MntTotal) (
    PARTITION low_spenders VALUES LESS THAN (500),
    PARTITION medium_spenders VALUES LESS THAN (1500),
    PARTITION high_spenders VALUES LESS THAN (MAXVALUE)
);
-- Motivo: Acelera relatórios específicos por faixa de gastos