    INSERT INTO Ambiente(
         Id_Amb,
         Id_franquia,
         Tamanho_ambiente,
         Quantidade_desse_ambiente,
         Nivel_limpeza,
         Detetizado,
         Salao,
         Cozinha)
        VALUES
        (1,1, 8.0, 1, 'Limpo', true, true, false),
        (2,1, 17.0, 2, 'Moderado', false, false, true),
        (3,2, 12.0, 1, 'Sujo', false, true, false),
        (4,2, 6.0, 2, 'Limpo', true,  false, true),
        (5,3, 19.0, 1, 'Moderado', false, true, false),
        (6,3, 7.0, 2, 'Limpo', true, false, true),
        (7,4, 14.0, 1, 'Sujo', false, true, false),
        (8,4, 11.0, 2, 'Moderado', false, false, true),
        (9,5, 16.0, 1, 'Limpo', true, true, false),
        (10,5, 5.0, 2, 'Sujo', false, false, true),
        (11,6, 13.0, 1, 'Moderado', false, true, false),
        (12,6, 20.0, 2, 'Limpo', true, false, true),
        (13,7, 9.0, 1, 'Sujo', false, true, false),
        (14,7, 15.0, 2, 'Moderado', false, false, true),
        (15,8, 18.0, 1, 'Limpo', true, true, false),
        (16,8, 10.0, 2, 'Sujo', false, false, true),
        (17,9, 7.0, 1, 'Moderado', false, true, false),
        (18,9, 13.0, 2, 'Limpo', true, false, true),
        (19,10, 6.0, 1, 'Sujo', false, true, false),
        (20,10, 17.0, 2, 'Moderado', false, false, true),
        (21,11, 12.0, 1, 'Limpo', true, true, false),
        (22,11, 8.0, 2, 'Sujo', false, false, true),
        (23,12, 14.0, 1, 'Moderado', false, true, false),
        (24,12, 9.0, 2, 'Limpo', true, false, true),
        (25,13, 16.0, 1, 'Sujo', false, true, false),
        (26,13, 5.0, 2, 'Moderado', false, false, true),
        (27,14, 18.0, 1, 'Limpo', true, true, false),
        (28,14, 10.0, 2, 'Sujo', false, false, true),
        (29,15, 20.0, 1, 'Moderado', false, true, false),
        (30,15, 7.0, 2, 'Limpo', true, false, true),
        (31,16, 13.0, 1, 'Sujo', false, true, false),
        (32,16, 11.0, 2, 'Moderado', false, false, true),
        (33,17, 9.0, 1, 'Limpo', true, true, false),
        (34,17, 15.0, 2, 'Sujo', false, false, true),
        (35,18, 14.0, 1, 'Moderado', false, true, false),
        (36,18, 8.0, 2, 'Limpo', true, false, true),
        (37,19, 16.0, 1, 'Sujo', false, true, false),
        (38,19, 5.0, 2, 'Moderado', false, false, true),
        (39,20, 18.0, 1, 'Limpo', true, true, false),
        (40,20, 10.0, 2, 'Sujo', false, false, true);

    INSERT INTO Cozinha(
        Id_Amb,
        Quant_geladeira,
        Quant_chapas,
        Quant_fogao,
        Quant_fritadeira
            ) VALUES
            (2,2,5,2,4),
            (4,4,7,5,1),
            (6,1,5,5,2),
            (8,1,1,4,3),
            (10,5,6,2,1),
            (12,3,4,2,4),
            (14,4,3,1,4),
            (16,4,5,3,2),
            (18,3,2,5,3),
            (20,4,6,1,1),
            (22,2,2,2,2),
            (24,3,2,4,3),
            (26,1,2,5,3),
            (28,5,3,5,4),
            (30,1,1,1,1),
            (32,1,6,5,2),
            (34,5,7,5,3),
            (36,4,6,4,4),
            (38,2,7,1,2),
            (40,2,3,4,2);

    INSERT INTO Salao(
        Id_Amb,
        Quant_cadeira,
        Quant_mesa,
        Quant_caixa_atend,
        Quant_totens_atend,
        Quant_lixeiras
    ) VALUES
        (1,2,5,2,4,2),
        (3,4,7,5,1,2),
        (5,1,5,5,2,2),
        (7,1,1,4,3,2),
        (9,5,6,2,1,2),
        (11,3,4,2,4,2),
        (13,4,3,1,4,2),
        (15,4,5,3,2,2),
        (17,3,2,5,3,2),
        (19,4,6,1,1,2),
        (21,2,2,2,2,2),
        (23,3,2,4,3,2),
        (25,1,2,5,3,2),
        (27,5,3,5,4,2),
        (29,1,1,1,1,2),
        (31,1,6,5,2,2),
        (33,5,7,5,3,2),
        (35,4,6,4,4,2),
        (37,2,7,1,2,2),
        (39,2,3,4,2,2);