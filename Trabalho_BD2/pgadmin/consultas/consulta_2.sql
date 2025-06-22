-- CRIA UM FUNÇÃO O QUAL RECEBE OS PRODUTOS ESCOLHIDOS PELO CLIENTE PARA VERIFICAR A DISPONIBILIDADE
CREATE OR REPLACE FUNCTION verificar_disponibilidade_combo_mensagem(
    p_id_lanche INT DEFAULT NULL,
    p_id_bebida INT DEFAULT NULL,
    p_id_sobremesa INT DEFAULT NULL,
    p_id_acompanhamento INT DEFAULT NULL
)
RETURNS TABLE (
    item TEXT,
    quantidade_estoque NUMERIC,
    mensagem TEXT
) AS $$
DECLARE
    itens_faltando TEXT;
BEGIN
    RETURN QUERY
    -- Ingredientes do lanche consultando a tabela de relacionamento L_Contem_I
    WITH Ingredientes_Lanche AS (
        SELECT
            lci.Indice_prod,
            i.Nome_ingred
        FROM L_Contem_I lci
        JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
        WHERE p_id_lanche IS NOT NULL AND lci.Indice_prod = p_id_lanche
    ),
    -- Bebida é um item simples, pega direto pelo nome do produto
    Itens_Bebida AS (
        SELECT 
            b.Indice_prod,
            b.Nome AS Nome_ingred
        FROM Bebida b
        WHERE p_id_bebida IS NOT NULL AND b.Indice_prod = p_id_bebida
    ),
    -- Sobremesa é um item simples, pega direto pelo nome do produto
    Itens_Sobremesa AS (
        SELECT 
            s.Indice_prod,
            s.Nome AS Nome_ingred
        FROM Sobremesa s
        WHERE p_id_sobremesa IS NOT NULL AND s.Indice_prod = p_id_sobremesa
    ),
    -- Acompanhemento é um item simples, pega direto pelo nome do produto
    Itens_Acompanhamento AS (
        SELECT 
            a.Indice_prod,
            a.Nome AS Nome_ingred
        FROM Acompanhamento a
        WHERE p_id_acompanhamento IS NOT NULL AND a.Indice_prod = p_id_acompanhamento
    ),

    --Junta todos os itens escolhidos pelo cliente em uma tabela unica
    Itens_Combo AS (
        SELECT Indice_prod, Nome_ingred FROM Ingredientes_Lanche
        UNION ALL
        SELECT Indice_prod, Nome_ingred FROM Itens_Bebida
        UNION ALL
        SELECT Indice_prod, Nome_ingred FROM Itens_Sobremesa
        UNION ALL
        SELECT Indice_prod, Nome_ingred FROM Itens_Acompanhamento
    ),

    -- Verifica a quantidade dos itens escolhidos no estoque
    Disponibilidade_Combo AS (
        SELECT
            ic.Nome_ingred,
            e.Quantidade AS quantidade_estoque
        FROM Itens_Combo ic
        JOIN Estoque e 
            ON e.Nome_ingred = ic.Nome_ingred
    ),

    -- Verifica a quantidade dos itens escolhidos no estoque é maior que 0
    Itens_Faltando AS (
        SELECT 
            Nome_ingred
        FROM Disponibilidade_Combo
        WHERE quantidade_estoque <= 0
    ),

    Status_Combo AS (
        SELECT 
            CASE 
                WHEN EXISTS (SELECT 1 FROM Itens_Faltando) 
                THEN 'Faltam: ' || string_agg(Nome_ingred, ', ')
                ELSE 'Combo disponível'
            END AS mensagem
        FROM Itens_Combo ic
        JOIN Disponibilidade_Combo d ON d.Nome_ingred = ic.Nome_ingred
    )

    SELECT 
        d.Nome_ingred AS item,
        d.quantidade_estoque,
        s.mensagem
    FROM Disponibilidade_Combo d
    CROSS JOIN Status_Combo s
    ORDER BY d.Nome_ingred;

END;
$$ LANGUAGE plpgsql;