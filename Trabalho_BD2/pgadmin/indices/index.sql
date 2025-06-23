-- Extensão necessária para busca textual otimizada (ILIKE)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Índices para autenticação
CREATE INDEX idx_funcionario_login 
ON Funcionario (Id_func, Senha_func);

-- Índices para filtros e buscas de produtos
CREATE INDEX idx_produto_categoria 
ON Produto (Categoria);

CREATE INDEX idx_produto_bebida 
ON Produto (Bebida);

CREATE INDEX idx_restricao_alimentar_trgm 
ON Produto USING gin (Restricao_alimentar gin_trgm_ops);

-- Índices para bebidas alcoólicas
CREATE INDEX idx_bebida_ealcoolico 
ON Bebida (E_Alcoolico);

-- Índice para filtro por data em pedidos
CREATE INDEX idx_pedido_data 
ON Pedido (Data_pedido);

-- Índices para relacionamento de pedidos com produtos
CREATE INDEX idx_ped_escolhe_prod_idpedido 
ON Ped_Escolhe_Prod (Id_pedido);

CREATE INDEX idx_ped_escolhe_prod_indiceprod 
ON Ped_Escolhe_Prod (Indice_prod);

-- Índices para busca textual (nome e ingredientes)
CREATE INDEX idx_nome_produto_trgm 
ON Produto USING gin (Nome_prod gin_trgm_ops);

CREATE INDEX idx_nome_ingred_trgm 
ON Ingrediente USING gin (Nome_ingred gin_trgm_ops);

CREATE INDEX idx_lanche_ingredientes_trgm 
ON Lanche USING gin (Ingredientes gin_trgm_ops);

-- Índices para verificação e atualização de estoque
CREATE INDEX idx_estoque_nome_produto 
ON Estoque (Nome_produto);

-- Índice adicional essencial para teste_7 e consulta_7
CREATE INDEX idx_lcontemi_indiceprod 
ON L_Contem_I (Indice_prod);