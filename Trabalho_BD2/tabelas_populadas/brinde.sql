create table Brinde (
     Id_brinde numeric(5) not null,
     Indice_prod numeric(5) not null,
     Tipo_brinde varchar(20) not null,
     Indice_estoq serial not null,
     constraint ID_Brinde_ID primary key (Id_brinde),
     constraint SID_Brind_Lanch_ID unique (Indice_prod));

INSERT INTO Brinde (Id_brinde, Indice_prod, Tipo_brinde, Indice_estoq) VALUES
(1, 57, 'carrinho', 97),
(2, 58, 'boneca', 98),
(3, 59, 'pelucia', 99),
(4, 60, 'jogo', 100);