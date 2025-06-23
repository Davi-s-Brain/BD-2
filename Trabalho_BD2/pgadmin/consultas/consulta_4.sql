--Função que serve a consulta de exibir, dentro de um período, o total de pedidos, total de vendas e o ticket médio.
CREATE OR REPLACE FUNCTION resumo_balanco_geral(
    p_data_inicio DATE,
    p_data_fim DATE
)
RETURNS TABLE (
    total_pedidos INT,
    total_vendas NUMERIC,
    ticket_medio NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(*)::INT AS total_pedidos,
        COALESCE(SUM(p.Valor_total_pedido)::NUMERIC, 0) AS total_vendas,
        CASE 
            WHEN COUNT(*) = 0 THEN 0
            ELSE ROUND((COALESCE(SUM(p.Valor_total_pedido)::NUMERIC, 0) / COUNT(*)), 2)
        END AS ticket_medio
    FROM Pedido p
    WHERE p.Data_pedido BETWEEN p_data_inicio AND p_data_fim;
END;
$$ LANGUAGE plpgsql;


--Exemplos de uso:

SELECT * FROM resumo_balanco_geral('2024-06-01', '2024-06-10');

-- --Função que serve a consulta de exibir, dentro de um período, o total de pedidos, total de vendas e o ticket médio.
-- CREATE OR REPLACE FUNCTION resumo_balanco_geral(
--     p_data_inicio DATE,
--     p_data_fim DATE
-- )
-- RETURNS TABLE (
--     total_pedidos INT,
--     total_vendas NUMERIC,
--     ticket_medio NUMERIC
-- ) AS $$
-- BEGIN
--     RETURN QUERY
--     SELECT 
--         COUNT(*) AS total_pedidos,
--         COALESCE(SUM(p.Valor_total), 0) AS total_vendas,
--         CASE 
--             WHEN COUNT(*) = 0 THEN 0
--             ELSE ROUND(COALESCE(SUM(p.Valor_total), 0) / COUNT(*), 2)
--         END AS ticket_medio
--     FROM Pedido p
--     WHERE p.Data_pedido BETWEEN p_data_inicio AND p_data_fim;
-- END;
-- $$ LANGUAGE plpgsql;

-- --Exemplos de uso:

-- SELECT * FROM resumo_balanco_geral('2024-06-01', '2024-06-10');