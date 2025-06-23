DROP FUNCTION IF EXISTS processar_pedido_com_quantidade;

CREATE OR REPLACE FUNCTION processar_pedido_com_quantidade(
    p_id_lanche NUMERIC DEFAULT NULL,
    p_qtd_lanche INT DEFAULT 0,
    p_id_bebida NUMERIC DEFAULT NULL,
    p_qtd_bebida INT DEFAULT 0,
    p_id_sobremesa NUMERIC DEFAULT NULL,
    p_qtd_sobremesa INT DEFAULT 0,
    p_id_acompanhamento NUMERIC DEFAULT NULL,
    p_qtd_acompanhamento INT DEFAULT 0
)
RETURNS TABLE (
    item VARCHAR,
    quantidade_estoque REAL,
    mensagem VARCHAR
) AS $$
DECLARE
    itens_em_falta INT;
BEGIN
    -- Monta os itens do lanche com a quantidade de ingredientes multiplicada pela quantidade de lanches
    WITH Ingredientes_Lanche AS (
        SELECT
            lci.Indice_prod,
            i.Nome_ingred,
            i.Indice_estoq,
            p_qtd_lanche AS quantidade
        FROM L_Contem_I lci
        JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
        WHERE p_id_lanche IS NOT NULL AND lci.Indice_prod = p_id_lanche
    ),

    Itens_Bebida AS (
        SELECT 
            b.Indice_prod,
            b.Nome_prod AS Nome_ingred,
            b.Indice_estoq,
            p_qtd_bebida AS quantidade
        FROM Produto b
        WHERE p_id_bebida IS NOT NULL AND b.Indice_prod = p_id_bebida
    ),

    Itens_Sobremesa AS (
        SELECT 
            s.Indice_prod,
            s.Nome_prod AS Nome_ingred,
            s.Indice_estoq,
            p_qtd_sobremesa AS quantidade
        FROM Produto s
        WHERE p_id_sobremesa IS NOT NULL AND s.Indice_prod = p_id_sobremesa
    ),

    Itens_Acompanhamento AS (
        SELECT 
            a.Indice_prod,
            a.Nome_prod AS Nome_ingred,
            a.Indice_estoq,
            p_qtd_acompanhamento AS quantidade
        FROM Produto a
        WHERE p_id_acompanhamento IS NOT NULL AND a.Indice_prod = p_id_acompanhamento
    ),

    -- Junta todos os itens do combo
    Itens_Combo AS (
        SELECT Indice_prod, Nome_ingred, Indice_estoq, quantidade FROM Ingredientes_Lanche
        UNION ALL
        SELECT Indice_prod, Nome_ingred, Indice_estoq, quantidade FROM Itens_Bebida
        UNION ALL
        SELECT Indice_prod, Nome_ingred, Indice_estoq, quantidade FROM Itens_Sobremesa
        UNION ALL
        SELECT Indice_prod, Nome_ingred, Indice_estoq, quantidade FROM Itens_Acompanhamento
    ),

    -- Consulta o estoque atual de cada item
    Disponibilidade_Combo AS (
        SELECT
            ic.Nome_ingred,
            e.Quantidade AS quantidade_estoque,
            ic.Indice_estoq,
            ic.quantidade AS quantidade_solicitada
        FROM Itens_Combo ic
        JOIN Estoque e ON e.Indice_estoq = ic.Indice_estoq
    ),

    -- Verifica se algum item não tem quantidade suficiente
    Itens_Faltando AS (
        SELECT 
            Nome_ingred
        FROM Disponibilidade_Combo
        WHERE quantidade_estoque < quantidade_solicitada
    ),

    -- Gera o status do combo
    Status_Combo AS (
        SELECT 
            CASE 
                WHEN EXISTS (SELECT 1 FROM Itens_Faltando) THEN 
                    'Faltam: ' || (SELECT string_agg(Nome_ingred, ', ') FROM Itens_Faltando)
                ELSE 'Combo disponível'
            END AS mensagem
    )

    SELECT COUNT(*) INTO itens_em_falta FROM Itens_Faltando;

    -- Se não há itens faltando, atualiza o estoque
    IF itens_em_falta = 0 THEN
        UPDATE Estoque e
        SET Quantidade = e.Quantidade - ic.quantidade
        FROM Itens_Combo ic
        WHERE e.Indice_estoq = ic.Indice_estoq;
    END IF;

    -- Retorna os dados do estoque e status
    RETURN QUERY
    SELECT 
        d.Nome_ingred AS item,
        d.quantidade_estoque,
        s.mensagem
    FROM Disponibilidade_Combo d
    CROSS JOIN Status_Combo s
    ORDER BY d.Nome_ingred;

END;
$$ LANGUAGE plpgsql;

SELECT * FROM processar_pedido_com_quantidade(
    21, 2, -- lanche id 21, quantidade 2
    1, 3,  -- bebida id 1, quantidade 3
    NULL, 0, -- sem sobremesa
    NULL, 0  -- sem acompanhamento
);