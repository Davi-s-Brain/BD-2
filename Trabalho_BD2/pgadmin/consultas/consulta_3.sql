-- Função para listar produtos com filtros opcionais
-- Esta função permite filtrar produtos por categoria, restrições alimentares e se são bebidas alco
CREATE OR REPLACE FUNCTION listar_produtos_com_filtros(
    p_categorias TEXT[] DEFAULT NULL,         -- Uma ou mais categorias
    p_sem_gluten BOOLEAN DEFAULT NULL,        -- TRUE para sem glúten
    p_sem_lactose BOOLEAN DEFAULT NULL,       -- TRUE para sem lactose
    p_e_alcoolico BOOLEAN DEFAULT NULL        -- TRUE para bebidas alcoólicas, FALSE para não alcoólicas
)
RETURNS TABLE (
    nome_produto TEXT,
    categoria TEXT,
    restricao TEXT,
    tipo_produto TEXT,
    e_alcoolico BOOLEAN,
    preco NUMERIC,
    peso NUMERIC,
    unidade TEXT
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
        b.E_Alcoolico,
        p.Preco_prod,
        p.Peso_prod,
        p.Unidade_medida
    FROM Produto p
    LEFT JOIN Bebida b ON p.Indice_prod = b.Indice_prod
    WHERE 
        --  Filtro por categoria
        (p_categorias IS NULL OR p.Categoria = ANY(p_categorias))
        
        -- Filtro por restrição: sem glúten
        AND (p_sem_gluten IS NULL OR (p_sem_gluten = TRUE AND p.Restricao_alimentar ILIKE '%sem glúten%'))

        -- Filtro por restrição: sem lactose
        AND (p_sem_lactose IS NULL OR (p_sem_lactose = TRUE AND p.Restricao_alimentar ILIKE '%sem lactose%'))

        -- Filtro por álcool (aplica só para bebidas)
        AND (
            p.Bebida = FALSE 
            OR p_e_alcoolico IS NULL 
            OR (p_e_alcoolico IS NOT NULL AND b.E_Alcoolico = p_e_alcoolico)
        );
END;
$$ LANGUAGE plpgsql;

-- Exemplo de uso da função com lnches da categoria 'Bovino' e bebidas alcoólicas:
SELECT * FROM listar_produtos_com_filtros(ARRAY['Bovino'], NULL, NULL, TRUE);
--aaaa cmit