--login
SELECT * FROM Funcionario
WHERE Id_func = 'id' AND
      Senha_func = 'senha';

--selecionar os produtos do pedido
    --selecionar os lanches dos produtos
            --selecionar os ingredientes dos lanches
                    --verificar no estoque
    --selecionar as bebidas
    --selecionar as sobremesas
    
-- Ingredientes dos lanches do pedido e sua disponibilidade
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    i.Nome_ingred,
    e.Quantidade AS quantidade_estoque
FROM Pedido p
JOIN Ped_Escolhe_Prod pe ON pe.Id_Pedido = p.Id_pedido
JOIN L_Contem_I lci ON lci.Indice_prod = pe.Indice_prod
JOIN Ingrediente i ON i.Id_ingred = lci.Id_ingred
JOIN Estoque e ON e.Indice_estoq = i.Indice_estoq
WHERE e.Quantidade > 0;

-- Bebidas do pedido e sua disponibilidade
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    b.Marca,
    e.Quantidade AS quantidade_estoque
FROM Pedido p
JOIN Ped_Escolhe_Prod pe ON pe.Id_Pedido = p.Id_pedido
JOIN Bebida b ON b.Indice_prod = pe.Indice_prod
JOIN Estoque e ON e.Indice_estoq = b.Indice_estoq
WHERE e.Quantidade > 0;

-- Sobremesas do pedido e sua disponibilidade
SELECT
    p.Id_pedido,
    pe.Indice_prod,
    s.Sabor,
    e.Quantidade AS quantidade_estoque
FROM Pedido p
JOIN Ped_Escolhe_Prod pe ON pe.Id_Pedido = p.Id_pedido
JOIN Sobremesa s ON s.Indice_prod = pe.Indice_prod
JOIN Estoque e ON e.Indice_estoq = s.Indice_estoq
WHERE e.Quantidade > 0;
