-- Função para retornar os produtos mais vendidos em um período específico
CREATE OR REPLACE FUNCTION produtos_mais_vendidos_periodo(
    p_data_inicio DATE,
    p_data_fim DATE
)
RETURNS TABLE (
    id_produto INT,
    nome_produto TEXT,
    tipo_produto TEXT,
    quantidade_vendida INT
) AS $$
BEGIN
    RETURN QUERY
    WITH produtos_pedidos AS (
        SELECT pe.Indice_prod, p.Id_pedido
        FROM Ped_Escolhe_Prod pe
        JOIN Pedido p ON pe.Id_pedido = p.Id_pedido  
        WHERE p.Data_pedido BETWEEN p_data_inicio AND p_data_fim
    )
    
    SELECT 
        pr.Indice_prod AS id_produto,
        pr.Nome_prod,
        CASE 
            WHEN pr.Lanche THEN 'Lanche'
            WHEN pr.Bebida THEN 'Bebida'
            WHEN pr.Sobremesa THEN 'Sobremesa'
            WHEN pr.Acompanhamento THEN 'Acompanhamento'
            ELSE 'Outro'
        END AS tipo_produto,
        COUNT(*) AS quantidade_vendida
    FROM produtos_pedidos pp
    JOIN Produto pr ON pr.Indice_prod = pp.Indice_prod
    GROUP BY pr.Indice_prod, pr.Nome_prod, pr.Lanche, pr.Bebida, pr.Sobremesa, pr.Acompanhamento
    ORDER BY quantidade_vendida DESC;
END;
$$ LANGUAGE plpgsql;

--Exemplos de uso:

SELECT * FROM produtos_mais_vendidos_periodo('2024-06-01', '2024-06-10');