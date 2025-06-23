-- CRIA UM FUNÇÃO O QUAL RECEBE OS PRODUTOS ESCOLHIDOS PELO CLIENTE PARA VERIFICAR A DISPONIBILIDADE
CREATE OR REPLACE FUNCTION verificar_disponibilidade_combo_mensagem(
    p_id_lanche numeric DEFAULT NULL,
    p_id_bebida numeric DEFAULT NULL,
    p_id_sobremesa numeric DEFAULT NULL,
    p_id_acompanhamento numeric DEFAULT NULL
)
RETURNS TABLE (
    item varchar,
    quantidade_estoque float,
    mensagem varchar
) AS $$
DECLARE
    itens_faltando varchar;
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
            b.Nome_prod AS Nome_ingred
        FROM Produto b
        WHERE p_id_bebida IS NOT NULL AND b.Indice_prod = p_id_bebida
    ),
    -- Sobremesa é um item simples, pega direto pelo nome do produto
    Itens_Sobremesa AS (
        SELECT 
            s.Indice_prod,
            s.Nome_prod AS Nome_ingred
        FROM Produto s
        WHERE p_id_sobremesa IS NOT NULL AND s.Indice_prod = p_id_sobremesa
    ),
    -- Acompanhemento é um item simples, pega direto pelo nome do produto
    Itens_Acompanhamento AS (
        SELECT 
            a.Indice_prod,
            a.Nome_prod AS Nome_ingred
        FROM  Produto a
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
            ON e.Nome_produto = ic.Nome_ingred
    ),

    -- Verifica a quantidade dos itens escolhidos no estoque é maior que 0
    Itens_Faltando AS (
        SELECT 
            Nome_ingred
        FROM Disponibilidade_Combo AS d
        WHERE d.quantidade_estoque <= 0
    ),

Status_Combo AS (
        SELECT 
            CASE 
                WHEN EXISTS (SELECT 1 FROM Itens_Faltando) THEN 
                    'Faltam: ' || (
                        SELECT string_agg(Nome_ingred, ', ') 
                        FROM Itens_Faltando
                    )
                ELSE 'Combo disponível'
            END AS mensagem
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

--exemplo de aplicação
SELECT * FROM verificar_disponibilidade_combo_mensagem(
    21, 83, 84, 91
);