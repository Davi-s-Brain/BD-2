-- Função para listar produtos com filtros opcionais
-- Esta função permite filtrar produtos por categoria, restrições alimentares e se são bebidas alco
CREATE OR REPLACE FUNCTION listar_produtos_com_filtros(
    p_categorias TEXT[] DEFAULT NULL,
    p_sem_gluten BOOLEAN DEFAULT NULL,
    p_sem_lactose BOOLEAN DEFAULT NULL,
    p_e_alcoolico BOOLEAN DEFAULT NULL
)
RETURNS TABLE (
    nome_produto VARCHAR,
    categoria VARCHAR,
    restricao VARCHAR,
    tipo_produto TEXT,
    e_alcoolico BOOLEAN,
    preco DOUBLE PRECISION,
    peso DOUBLE PRECISION,
    unidade VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.Nome_prod,
        p.Categoria,
        p.Restricao_alimentar,
        CASE 
            WHEN p.Lanche THEN 'Lanche'
            WHEN p.Bebida THEN 'Bebida'
            WHEN p.Sobremesa THEN 'Sobremesa'
            WHEN p.Acompanhamento THEN 'Acompanhamento'
            ELSE 'Outro'
        END AS tipo_produto,
        CASE 
            WHEN p.Bebida THEN b.E_Alcoolico 
            ELSE NULL 
        END AS e_alcoolico,
        p.Preco_prod::DOUBLE PRECISION,
        p.Peso_prod::DOUBLE PRECISION,
        p.Unidade_medida
    FROM Produto p
    LEFT JOIN Bebida b ON p.Indice_prod = b.Indice_prod
    WHERE 
        -- Filtros de categoria e restrições
        (p_categorias IS NULL OR p.Categoria = ANY(p_categorias))
        AND (p_sem_gluten IS NULL OR (p_sem_gluten = TRUE AND p.Restricao_alimentar ILIKE '%sem glúten%'))
        AND (p_sem_lactose IS NULL OR (p_sem_lactose = TRUE AND p.Restricao_alimentar ILIKE '%sem lactose%'))

        -- Lógica do filtro de bebida alcoólica:
        AND (
            -- Se p_e_alcoolico for NULL, ignora bebidas
            (p_e_alcoolico IS NULL AND p.Bebida = FALSE)

            -- Se p_e_alcoolico for TRUE ou FALSE, pega só bebidas com o valor correspondente
            OR (p_e_alcoolico IS NOT NULL AND p.Bebida = TRUE AND b.E_Alcoolico = p_e_alcoolico)
        );
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso da função com lnches da categoria 'Bovino' e bebidas alcoólicas:
SELECT * FROM listar_produtos_com_filtros(NULL, NULL, NULL, NULL);


-- Exemplo de uso da função com lnches da categoria 'Bovino' e bebidas alcoólicas:
SELECT * FROM listar_produtos_com_filtros(NULL, NULL, NULL, TRUE);

SELECT * FROM listar_produtos_com_filtros(ARRAY['Bovino','Suíno'], NULL, NULL, TRUE);
--aaaa cmit