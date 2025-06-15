INSERT INTO Pedido (
    Id_pedido,
    Data_pedido,
    Hora_pedido,
    Valor_total_pedido,
    Forma_pagamento,
    E_delivery,
    Observacao,
    Id_cliente,
    Id_func
)
    VALUES
    (1, '2024-06-15', '12:00', 100.00, 'Cartao', TRUE, 'Primeiro pedido', 1, 1),
    (2, '2024-06-16', '13:15', 120.50, 'Dinheiro', FALSE, 'Pedido rápido', 2, 2),
    (3, '2024-06-17', '14:30', 80.75, 'Pix', TRUE, 'Sem observações', 3, 3),
    (4, '2024-06-18', '15:45', 200.00, 'Cartao', FALSE, 'Cliente frequente', 4, 4),
    (5, '2024-06-19', '16:00', 95.00, 'Dinheiro', TRUE, 'Primeira compra', 5, 5),
    (6, '2024-06-20', '12:10', 110.00, 'Cartao', FALSE, 'Pedido normal', 6, 1),
    (7, '2024-06-21', '13:20', 130.50, 'Dinheiro', TRUE, 'Pedido especial', 7, 2),
    (8, '2024-06-22', '14:40', 90.75, 'Pix', FALSE, '', 8, 3),
    (9, '2024-06-23', '15:50', 210.00, 'Cartao', TRUE, 'Cliente novo', 9, 4),
    (10, '2024-06-24', '16:05', 105.00, 'Dinheiro', FALSE, 'Pedido rápido', 10, 5),
    (11, '2024-06-25', '12:15', 115.00, 'Cartao', TRUE, 'Pedido comum', 11, 1),
    (12, '2024-06-26', '13:25', 140.50, 'Dinheiro', FALSE, 'Pedido especial', 12, 2),
    (13, '2024-06-27', '14:45', 100.75, 'Pix', TRUE, 'Sem observações', 13, 3),
    (14, '2024-06-28', '15:55', 220.00, 'Cartao', FALSE, 'Cliente fiel', 14, 4),
    (15, '2024-06-29', '16:10', 115.00, 'Dinheiro', TRUE, 'Primeira compra', 15, 5),
    (16, '2024-06-30', '12:20', 120.00, 'Cartao', FALSE, 'Pedido normal', 16, 1),
    (17, '2024-07-01', '13:30', 150.50, 'Dinheiro', TRUE, 'Pedido especial', 17, 2),
    (18, '2024-07-02', '14:50', 110.75, 'Pix', FALSE, 'Sem observações', 18, 3),
    (19, '2024-07-03', '16:00', 230.00, 'Cartao', TRUE, 'Cliente novo', 19, 4)
    (20, '2024-07-04', '16:15', 125.00, 'Dinheiro', FALSE, 'Pedido rápido', 20, 5);
