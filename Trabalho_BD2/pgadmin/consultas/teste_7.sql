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
    estoque_antigo REAL,
    estoque_atual REAL,
    mensagem TEXT
) AS $$
DECLARE
    itens_em_falta INT;
BEGIN
    --  Tabela temporária dos itens do combo
    CREATE TEMP TABLE temp_itens_combo AS
    SELECT * FROM (
        SELECT 
            lci.Indice_prod,
            i.Nome_ingred,
            i.Indice_estoq,
            p_qtd_lanche AS quantidade
        FROM L_Contem_I lci
        JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
        WHERE p_id_lanche IS NOT NULL AND p_qtd_lanche > 0 AND lci.Indice_prod = p_id_lanche

        UNION ALL

        SELECT 
            b.Indice_prod,
            b.Nome_prod AS Nome_ingred,
            NULL::NUMERIC AS Indice_estoq,
            p_qtd_bebida
        FROM Produto b
        WHERE p_id_bebida IS NOT NULL AND p_qtd_bebida > 0 AND b.Indice_prod = p_id_bebida

        UNION ALL

        SELECT 
            s.Indice_prod,
            s.Nome_prod AS Nome_ingred,
            NULL::NUMERIC AS Indice_estoq,
            p_qtd_sobremesa
        FROM Produto s
        WHERE p_id_sobremesa IS NOT NULL AND p_qtd_sobremesa > 0 AND s.Indice_prod = p_id_sobremesa

        UNION ALL

        SELECT 
            a.Indice_prod,
            a.Nome_prod AS Nome_ingred,
            NULL::NUMERIC AS Indice_estoq,
            p_qtd_acompanhamento
        FROM Produto a
        WHERE p_id_acompanhamento IS NOT NULL AND p_qtd_acompanhamento > 0 AND a.Indice_prod = p_id_acompanhamento
    ) AS itens;

    --  Consulta estoque atual dos itens antes da atualização
    CREATE TEMP TABLE temp_disponibilidade AS
    SELECT
        ic.Nome_ingred,
        e.Quantidade AS estoque_antigo,
        COALESCE(ic.Indice_estoq, e.Indice_estoq) AS Indice_estoq,
        ic.quantidade AS quantidade_solicitada
    FROM temp_itens_combo ic
    JOIN Estoque e ON 
        (ic.Indice_estoq IS NOT NULL AND e.Indice_estoq = ic.Indice_estoq)
        OR (ic.Indice_estoq IS NULL AND e.Nome_produto = ic.Nome_ingred);

    --  Verifica itens em falta
    SELECT COUNT(*) INTO itens_em_falta
    FROM temp_disponibilidade as td
    WHERE td.estoque_antigo < quantidade_solicitada;

    --  Atualiza estoque se disponível
    IF itens_em_falta = 0 THEN
        UPDATE Estoque e
        SET Quantidade = e.Quantidade - d.quantidade_solicitada
        FROM temp_disponibilidade d
        WHERE 
            (d.Indice_estoq IS NOT NULL AND e.Indice_estoq = d.Indice_estoq)
            OR (d.Indice_estoq IS NULL AND e.Nome_produto = d.Nome_ingred);
    END IF;

    --  Consulta o estoque atualizado
    RETURN QUERY
    SELECT 
        d.Nome_ingred AS item,
        d.estoque_antigo,
        e.Quantidade AS estoque_atual,
        CASE 
            WHEN itens_em_falta = 0 THEN 'Combo disponível'
            ELSE 
                'Faltam: ' || (
                    SELECT string_agg(Nome_ingred, ', ') 
                    FROM temp_disponibilidade as td
                    WHERE td.estoque_antigo < quantidade_solicitada
                )
        END AS mensagem
    FROM temp_disponibilidade d
    JOIN Estoque e ON 
        (d.Indice_estoq IS NOT NULL AND e.Indice_estoq = d.Indice_estoq)
        OR (d.Indice_estoq IS NULL AND e.Nome_produto = d.Nome_ingred)
    ORDER BY d.Nome_ingred;

    --  Limpa tabelas temporárias
    DROP TABLE temp_itens_combo;
    DROP TABLE temp_disponibilidade;

END;
$$ LANGUAGE plpgsql;


SELECT * FROM processar_pedido_com_quantidade(
    21, 3, -- lanche id 21, quantidade 3
    1, 2,  -- bebida id 1, quantidade 2
    NULL, 0, -- sem sobremesa
    NULL, 0  -- sem acompanhamento
);

SELECT * FROM verificar_disponibilidade_combo_mensagem(
    21, null, null , null
);