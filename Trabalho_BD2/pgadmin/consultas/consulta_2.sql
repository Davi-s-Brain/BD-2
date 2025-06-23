--2ª CONSULTA--------------------------------------------------------------------
--selecionar os produtos do pedido
    --selecionar os lanches dos produtos
            --selecionar os ingredientes dos lanches
                    --verificar no estoque
    --selecionar as bebidas
    --selecionar as sobremesas
    
-- Ingredientes dos lanches do pedido e sua disponibilidade
-- Essas três partes te dão todos os itens do pedido que estão sem estoque.
-- Se nenhuma linha for retornada, então tudo está disponível.
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    i.Nome_ingred,
    e.Quantidade AS quantidade_estoque
FROM Produto AS p
    JOIN L_Contem_I AS lci ON lci.Indice_prod = p.Indice_prod
    JOIN Ingrediente AS i ON i.Id_ingred = lci.Id_ingred
    JOIN Estoque AS e ON e.Indice_estoq = i.Indice_estoq
WHERE e.Quantidade <= 0;

-- Bebidas do pedido e sua disponibilidade
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    b.Marca,
    e.Quantidade AS quantidade_estoque
FROM Pedido AS p
    JOIN Bebida AS b ON b.Indice_prod = p.Indice_prod
    JOIN Estoque AS e ON e.Indice_estoq = b.Indice_estoq
WHERE e.Quantidade <= 0;

-- Sobremesas do pedido e sua disponibilidade
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    s.Sabor,
    e.Quantidade AS quantidade_estoque
FROM Pedido p
    JOIN Sobremesa s ON s.Indice_prod = p.Indice_prod
    JOIN Estoque e ON e.Indice_estoq = s.Indice_estoq
WHERE e.Quantidade <= 0;


--segunda consulta parte 1
--
UPDATE Estoque e
SET Quantidade = Quantidade - 1
FROM Ingrediente i
JOIN L_Contem_I lci ON lci.Id_ingred = i.Id_ingred
JOIN Ped_Escolhe_Prod pep ON pep.Indice_prod = lci.Indice_prod
WHERE i.Indice_estoq = e.Indice_estoq
  AND pep.Id_pedido = <ID_DO_PEDIDO>;

UPDATE Estoque e
SET Quantidade = Quantidade - pep.Quantidade
FROM Bebida b
JOIN Ped_Escolhe_Prod pep ON pep.Indice_prod = b.Indice_prod
WHERE b.Indice_estoq = e.Indice_estoq
  AND pep.Id_pedido = <ID_DO_PEDIDO>;

UPDATE Estoque e
SET Quantidade = Quantidade - pep.Quantidade
FROM Sobremesa s
JOIN Ped_Escolhe_Prod pep ON pep.Indice_prod = s.Indice_prod
WHERE s.Indice_estoq = e.Indice_estoq
  AND pep.Id_pedido = <ID_DO_PEDIDO>;
