INSERT INTO Franquia(
    Id_franquia,
    Nome_franquia,
    CNPJ,
    Endereco_franq,
    E_mail_franq,
    Data_inauguracao_franq)
    VALUES
    (1, 'RanBurguer Centro',       12345678000101, 'Av. Brasil, 100',        'centro@ranburguer.com',     '2015-03-15'),
    (2, 'RanBurguer Sul',          23456789000112, 'Rua das Palmeiras, 85',  'sul@ranburguer.com',        '2016-07-22'),
    (3, 'RanBurguer Norte',        34567890000123, 'Rua Amazonas, 410',      'norte@ranburguer.com',      '2018-01-10'),
    (4, 'RanBurguer Leste',        45678900000134, 'Av. Independência, 900', 'leste@ranburguer.com',      '2019-05-05'),
    (5, 'RanBurguer Oeste',        56789000000145, 'Rua das Flores, 234',    'oeste@ranburguer.com',      '2020-11-12'),
    (6, 'RanBurguer Shopping Sul', 67890000000156, 'Shopping Sul, Piso 1',   'shop.sul@ranburguer.com',   '2021-04-30'),
    (7, 'RanBurguer Aeroporto',    78900000000167, 'Av. Aeroporto, 1000',    'aeroporto@ranburguer.com',  '2021-09-18'),
    (8, 'RanBurguer Estação',      89000000000178, 'Rua Central, 300',       'estacao@ranburguer.com',    '2022-03-08'),
    (9, 'RanBurguer Universidade', 90000000000189, 'Campus USP, CB',    'uni@ranburguer.com',        '2023-01-20'),
    (10,'RanBurguer Drive-Thru',   11223344556677, 'Rod. BR-101, km 120',    'drive@ranburguer.com',      '2023-08-15'),
    (11, 'RanBurguer Parque',        22113344556600, 'Rua do Parque, 123',          'parque@ranburguer.com',     '2021-06-01'),
    (12, 'RanBurguer Lagoa',         33114455667711, 'Av. Lagoa Azul, 987',         'lagoa@ranburguer.com',      '2020-02-20'),
    (13, 'RanBurguer Industrial',    44115566778822, 'Rua das Indústrias, 456',     'industrial@ranburguer.com', '2019-08-14'),
    (14, 'RanBurguer Jardim',        55116677889933, 'Rua Jardim das Rosas, 22',    'jardim@ranburguer.com',     '2022-12-01'),
    (15, 'RanBurguer Praia',         66117788990044, 'Av. Beira Mar, 765',          'praia@ranburguer.com',      '2023-05-25'),
    (16, 'RanBurguer Montanha',      77118899001155, 'Estrada da Serra, km 8',      'montanha@ranburguer.com',   '2017-09-30'),
    (17, 'RanBurguer Mercado',       88119900112266, 'Mercado Municipal, Loja 45',  'mercado@ranburguer.com',    '2016-04-12'),
    (18, 'RanBurguer Subúrbio',      99120011223377, 'Av. Suburbana, 2001',         'suburbio@ranburguer.com',   '2021-10-09'),
    (19, 'RanBurguer Vila Nova',     10221122334488, 'Rua Vila Nova, 333',          'vilanova@ranburguer.com',   '2022-02-17'),
    (20, 'RanBurguer Rodoviária',    11232233445599, 'Terminal Rodoviário, Box 3',  'rodoviaria@ranburguer.com', '2018-06-05');



INSERT INTO Cozinha(   
    Id_Amb,
    Quant_geladeira,
    Quant_chapas,
    Quant_fogao,
    Quant_fritadeira)
    VALUES
        (1, 2, 1, 1, 1),
        (2, 3, 2, 1, 2),
        (3, 4, 2, 2, 1),
        (4, 3, 1, 1, 2),
        (5, 4, 2, 2, 1),
        (6, 5, 3, 1, 2),
        (7, 2, 2, 1, 1),
        (8, 3, 3, 2, 2),
        (9, 4, 1, 1, 1),
        (10, 5, 2, 2, 3),
        (11, 3, 1, 1, 2),
        (12, 4, 2, 3, 1),
        (13, 5, 3, 2, 2),
        (14, 4, 1, 1, 3),
        (15, 5, 2, 2 ,1),
        (16 ,3 ,3 ,1 ,2 ),
        (17 ,4 ,2 ,2 ,3 ),
        (18 ,5 ,1 ,1 ,1 ),
        (19 ,2 ,3 ,2 ,2 ),
        (20 ,4 ,1 ,1 ,3 );

    create table Salao (
     Id_Amb numeric(5) not null,
     Quant_cadeira float(1) not null,
     Quant_mesa float(1) not null,
     Quant_caixa_atend float(1) not null,
     Quant_totens_atend float(1) not null,
     Quant_lixeiras float(1) not null,
     constraint ID_Salao_Ambie_ID primary key (Id_Amb));

INSERT INTO Salao(
    Id_Amb,
    Quant_cadeira,
    Quant_mesa,
    Quant_caixa_atend,
    Quant_totens_atend,
    Quant_lixeiras)
VALUES
    (1, 20, 10, 2, 3, 5),
    (2, 30, 15, 3, 4, 6),
    (3, 25, 12, 2, 3, 4),
    (4, 18, 9, 1, 2, 3),
    (5, 22, 11, 2, 3, 5),
    (6, 28, 14, 3, 4, 6),
    (7, 20, 10, 2, 3, 5),
    (8, 30, 15, 3, 4, 6),
    (9, 25, 12, 2, 3, 4),
    (10 ,18 ,9 ,1 ,2 ,3),
    (11 ,22 ,11 ,2 ,3 ,5),
    (12 ,28 ,14 ,3 ,4 ,6),
    (13 ,20 ,10 ,2 ,3 ,5),
    (14 ,30 ,15 ,3 ,4 ,6),
    (15 ,25 ,12 ,2 ,3 ,4),
    (16 ,18 ,9 ,1 ,2 ,3),
    (17 ,22 ,11 ,2 ,3 ,5),
    (18 ,28 ,14 ,3 ,4 ,6),
    (19 ,20 ,10 ,2 ,3 ,5),
    (20 ,30 ,15 ,3 ,4 ,6);
    