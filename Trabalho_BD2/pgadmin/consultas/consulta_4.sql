-- CRIA UM FUNÇÃO A QUAL RECEBE UM TERMO DE BUSCA E RETORNA OS PRODUTOS QUE CONTENHAM ESSE TERMO NO NOME, INGREDIENTES OU DESCRIÇÃO
DROP function if exists buscar_por_termo;

CREATE OR REPLACE FUNCTION buscar_por_termo(
    p_termo_busca TEXT
)
RETURNS TABLE (
    id_produto NUMERIC,
    nome_produto VARCHAR,
    categoria VARCHAR,
    tipo_produto text,
    preco NUMERIC(10,2),
    peso NUMERIC(10,2),
    unidade VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH ingredientes_relacionados AS (
        SELECT DISTINCT 
            p.Indice_prod,
            i.Nome_ingred
        FROM Produto p
        JOIN L_Contem_I lci ON lci.Indice_prod = p.Indice_prod
        JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
    ),

    ingredientes_texto_lanche AS (
        SELECT 
            l.Indice_prod,
            l.Ingredientes
        FROM Lanche l
    ),

    produtos_encontrados AS (
        SELECT DISTINCT 
            p.Indice_prod,
            p.Nome_prod,
            p.Categoria,
            CASE 
                WHEN p.Lanche THEN 'Lanche'
                WHEN p.Bebida THEN 'Bebida'
                WHEN p.Sobremesa THEN 'Sobremesa'
                WHEN p.Acompanhamento THEN 'Acompanhamento'
                ELSE 'Outro'
            END AS tipo_produto,
            p.Preco_prod::NUMERIC(10,2),
        	p.Peso_prod::NUMERIC(10,2),
            p.Unidade_medida
        FROM Produto p

        LEFT JOIN ingredientes_relacionados ir ON p.Indice_prod = ir.Indice_prod
        LEFT JOIN ingredientes_texto_lanche il ON p.Indice_prod = il.Indice_prod

        WHERE 
            p_termo_busca IS NULL
            OR (
                p.Nome_prod ILIKE '%' || p_termo_busca || '%'
                OR ir.Nome_ingred ILIKE '%' || p_termo_busca || '%'
                OR il.Ingredientes ILIKE '%' || p_termo_busca || '%'
            )
    )

    SELECT 
        pe.Indice_prod AS id_produto,
        pe.Nome_prod,
        pe.Categoria,
        pe.tipo_produto,
        pe.Preco_prod,
        pe.Peso_prod,
        pe.Unidade_medida
    FROM produtos_encontrados pe
    ORDER BY pe.Nome_prod;
END;
$$ LANGUAGE plpgsql;

--EXEMPLO de consulta:
SELECT * FROM buscar_por_termo('peito de peru');