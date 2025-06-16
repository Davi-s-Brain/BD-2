-- *********************************************
-- * Standard SQL generation                   
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Thu Jun 12 17:05:37 2025 
-- * LUN file: C:\Users\Windows\OneDrive\Documentos\GitHub\BD-2\Trabalho_BD2\Trabalho BD2 v11-06-2025.lun 
-- * Schema: SQL/SQL 
-- ********************************************* 


-- Database Section
-- ________________ 

DROP database if exists RanBurguer;
create database RanBurguer;


-- DBSpace Section
-- _______________


-- Tables Section
-- _____________ 

--Saritcha amor da minha vida
create table Acompanhamento (--ok
     Indice_prod numeric(5) not null,
     Tipo_acompanhamento varchar(50) not null,
     Indice_estoq serial,
     constraint ID_Acomp_Produ_ID primary key (Indice_prod));

create table Ambiente (--ok
     Id_Amb numeric(5) not null,
     Id_franquia numeric(5) not null,
     Tamanho_ambiente float(3)not null,
     Quantidade_desse_ambiente float(1) not null,
     Nivel_limpeza varchar(20) not null,
     Detetizado boolean not null,
     Salao boolean,
     Cozinha boolean,
     constraint Id_Ambiente_ID primary key (Id_Amb));

create table Avaliacao (--ok
     Indice_av numeric(5) not null,
     NPS float(1) not null,
     Campo_texto varchar(200) not null,
     Data_av date not null,
     constraint ID_Avaliacao_ID primary key (Indice_av));

create table Bebida (--ok
     Indice_prod numeric(5) not null,
     Marca varchar(50) not null,
     Sabor varchar(50) not null,
     E_Alcoolico boolean not null,
     Indice_estoq serial,
     constraint ID_Bebid_Produ_ID primary key (Indice_prod));

create table Brinde (--ok
     Id_brinde numeric(5) not null,
     Indice_prod numeric(5) not null,
     Tipo_brinde varchar(20) not null,
     Indice_estoq serial not null,
     constraint ID_Brinde_ID primary key (Id_brinde),
     constraint SID_Brind_Lanch_ID unique (Indice_prod));

create table Ped_Escolhe_Prod (--NÃO
     Id_Pedido serial,
     Indice_prod numeric(5) not null,
     Quantidade numeric(2) not null,
     constraint ID_Ped_Escolhe_Prod_ID primary key (Id_Pedido, Indice_prod)
     constraint ID_Pedido_ID foreign key (Id_Pedido));

create table C_Registra_A (--NÃO
     Id_pedido uuid not null,
     Id_cliente numeric(11) not null,
     Indice_av numeric(5) not null,
     constraint ID_C_Reg_Pedid_ID primary key (Id_pedido),
     constraint SID_C_Reg_Clien_ID unique (Id_cliente),
     constraint SID_C_Reg_Avali_ID unique (Indice_av));

create table Cliente (--ok
     Id_cliente numeric(11) not null,
     Primeiro_nome_client varchar(50) not null,
     Ultimo_nome_client varchar(50) not null,
     Data_nascimento_client date not null,
     CPF_client numeric(11) not null,
     Telefone_client numeric(11) not null,
     E_mail_client varchar(50) not null,
     Data_cadastro_client date not null,
     Genero_client varchar(10) not null,
     E_intolerante_lactose boolean not null,
     E_celiaco boolean not null,
     E_vegetariano boolean not null,
     E_vegano boolean not null,
     Senha_cliente varchar(20) not null,
     constraint ID_Cliente_ID primary key (Id_cliente),
     constraint CPF_client unique (CPF_client));

create table Cozinha (--ok
     Id_Amb numeric(5) not null,
     Quant_geladeira float(1) not null,
     Quant_chapas float(1) not null,
     Quant_fogao float(1) not null,
     Quant_fritadeira float(1) not null,
     constraint ID_Cozin_Ambie_ID primary key (Id_Amb));

--Rafa amor da vida da Sarah
create table Estoque (--ok
     Indice_estoq serial not null,
     Nome_produto varchar(50) not null,
     Quantidade float(1) not null,
     Unidade_medida varchar(2) not null,
     Data_fabricacao date not null,
     Data_validade date not null,
     Lote numeric(8) not null,
     Preco_compra_mercado float(1) not null
     constraint ID_Estoque_ID primary key (Indice_estoq)
     );

create table F_Vende_P (--NÃO
     Id_franquia numeric(5) not null,
     Indice_prod numeric(5) not null,
     constraint ID_F_Vende_P_ID primary key (Indice_prod, Id_franquia));

create table Franquia (--ok
     Id_franquia numeric(5) not null,
     Nome_franquia varchar(50) not null,
     CNPJ numeric(14) not null,
     Endereco_franq varchar(50) not null,
     E_mail_franq varchar(50) not null,
     Data_inauguracao_franq date not null,
     constraint ID_Franquia_ID primary key (Id_franquia));
     --alter table foreing key

create table Funcionario (--ok
     Id_func numeric(5) not null,
     Nome_func varchar(50) not null,
     CPF numeric(11) not null,
     Data_nasc_func date not null,
     Cargo varchar(1) not null,
     Salario float(1) not null,
     Data_admissao date not null,
     Turno varchar(20) not null,
     Tipo_de_contrato varchar(20) not null,
     Status_func varchar(20) not null,
     Id_franquia serial not null,
     Senha_Func varchar(20) not null,
     constraint ID_Funcionario_ID primary key (Id_func));

create table Ingrediente (--ok
     Id_ingred numeric(5) not null,
     Tipo_ingred varchar(50) not null,
     Nome_ingred varchar(50) not null,
     Preco_venda_cliente float(1) not null,
     Peso_ingred float(1) not null,
     Indice_estoq serial,
     constraint ID_Ingrediente_ID primary key (Id_ingred));

create table L_Contem_I (--NÃO
     Id_ingred numeric(5) not null,
     Indice_prod numeric(5) not null,
     constraint ID_L_Contem_I_ID primary key (Id_ingred, Indice_prod));

create table Lanche (--ok
     Indice_prod numeric(5) not null,
     Ingredientes varchar(100) not null,
     Tamanho_lanche varchar(20) not null,
     constraint ID_Lanch_Produ_ID primary key (Indice_prod));

create table Pedido (--ok
     Id_pedido serial not null,
     Data_pedido date not null,
     Hora_pedido varchar(5) not null,
     Valor_total_pedido float(1) not null,
     Forma_pagamento varchar(20) not null,
     E_delivery boolean not null,
     Observacao varchar(200) not null,
     Id_func numeric(1) not null,
     Id_cliente numeric(11) not null,
     constraint ID_Pedido_ID primary key (Id_pedido));

create table Produto (--ok
     Indice_prod numeric(5) not null,
     Nome_prod varchar(50) not null,
     Preco_prod float(1) not null,
     Peso_prod float(1) not null,
     Unidade_medida varchar(2) not null,
     Restricao_alimentar varchar(50) not null,
     Categoria varchar(50) not null,
     Sobremesa boolean,
     Lanche boolean,
     Bebida boolean,
     Acompanhamento boolean,
     constraint ID_Produto_ID primary key (Indice_prod));

create table Salao (--ok
     Id_Amb numeric(5) not null,
     Quant_cadeira float(1) not null,
     Quant_mesa float(1) not null,
     Quant_caixa_atend float(1) not null,
     Quant_totens_atend float(1) not null,
     Quant_lixeiras float(1) not null,
     constraint ID_Salao_Ambie_ID primary key (Id_Amb));

create table Sobremesa (--ok
     Indice_prod numeric(5) not null,
     Tipo_sobremesa varchar(50) not null,
     Sabor varchar(50) not null,
     Indice_estoq serial,
     constraint ID_Sobre_Produ_ID primary key (Indice_prod));


-- -- Constraints Section
-- -- ___________________ 

-- alter table Acompanhamento add constraint ID_Acomp_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;

-- alter table Acompanhamento add constraint REF_Acomp_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Ambiente add constraint Id_Ambiente_CHK
--      check(exists(select * from F_CompostaPor_A
--                   where F_CompostaPor_A.Id_Amb = Id_Amb)); 

-- alter table Ambiente add constraint EXCL_Ambiente
--      check((Cozinha is not null and Salao is null and Indice_estoq is null)
--            or (Cozinha is null and Salao is not null and Indice_estoq is null)
--            or (Cozinha is null and Salao is null and Indice_estoq is not null)
--            or (Cozinha is null and Salao is null and Indice_estoq is null)); 

-- alter table Ambiente add constraint SId_Ambie_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Avaliacao add constraint ID_Avaliacao_CHK
--      check(exists(select * from C_Registra_A
--                   where C_Registra_A.Indice_av = Indice_av)); 

-- alter table Bebida add constraint ID_Bebid_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;

-- alter table Bebida add constraint REF_Bebid_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Brinde add constraint SID_Brind_Lanch_FK
--      foreign key (Indice_prod)
--      references Lanche;

-- alter table Brinde add constraint REF_Brind_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table C_Escolhe_P add constraint REF_C_Esc_Produ
--      foreign key (Indice_prod)
--      references Produto;

-- alter table C_Escolhe_P add constraint EQU_C_Esc_Clien_FK
--      foreign key (Id_cliente)
--      references Cliente;

-- alter table C_Registra_A add constraint ID_C_Reg_Pedid_FK
--      foreign key (Id_pedido)
--      references Pedido;

-- alter table C_Registra_A add constraint SID_C_Reg_Clien_FK
--      foreign key (Id_cliente)
--      references Cliente;

-- alter table C_Registra_A add constraint SID_C_Reg_Avali_FK
--      foreign key (Indice_av)
--      references Avaliacao;

-- alter table Cliente add constraint ID_Cliente_CHK
--      check(exists(select * from C_Escolhe_P
--                   where C_Escolhe_P.Id_cliente = Id_cliente)); 

-- alter table Cliente add constraint ID_Cliente_CHK
--      check(exists(select * from Pedido
--                   where Pedido.Id_cliente = Id_cliente)); 

-- alter table Cozinha add constraint ID_Cozin_Ambie_FK
--      foreign key (Id_Amb)
--      references Ambiente;

-- alter table Estoque add constraint ID_Estoque_CHK
--      check(exists(select * from Ambiente
--                   where Ambiente.Indice_estoq = Indice_estoq)); 

-- alter table F_CompostaPor_A add constraint EQU_F_Com_Franq
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table F_CompostaPor_A add constraint EQU_F_Com_Ambie_FK
--      foreign key (Id_Amb)
--      references Ambiente;

-- alter table F_Vende_P add constraint EQU_F_Ven_Produ
--      foreign key (Indice_prod)
--      references Produto;

-- alter table F_Vende_P add constraint EQU_F_Ven_Franq_FK
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from F_CompostaPor_A
--                   where F_CompostaPor_A.Id_franquia = Id_franquia)); 

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from F_Vende_P
--                   where F_Vende_P.Id_franquia = Id_franquia)); 

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from Funcionario
--                   where Funcionario.Id_franquia = Id_franquia)); 

-- alter table Funcionario add constraint EQU_Funci_Franq_FK
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table Ingrediente add constraint REF_Ingre_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table L_Contem_I add constraint EQU_L_Con_Lanch_FK
--      foreign key (Indice_prod)
--      references Lanche;

-- alter table L_Contem_I add constraint REF_L_Con_Ingre
--      foreign key (Id_ingred)
--      references Ingrediente;

-- alter table Lanche add constraint ID_Lanch_Produ_CHK
--      check(exists(select * from L_Contem_I
--                   where L_Contem_I.Indice_prod = Indice_prod)); 

-- alter table Lanche add constraint ID_Lanch_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;

-- alter table Pedido add constraint REF_Pedid_Funci_FK
--      foreign key (Id_func)
--      references Funcionario;

-- alter table Pedido add constraint EQU_Pedid_Clien_FK
--      foreign key (Id_cliente)
--      references Cliente;

-- alter table Produto add constraint ID_Produto_CHK
--      check(exists(select * from F_Vende_P
--                   where F_Vende_P.Indice_prod = Indice_prod)); 

-- alter table Produto add constraint EXCL_Produto
--      check((Acompanhamento is not null and Sobremesa is null and Lanche is null and Bebida is null)
--            or (Acompanhamento is null and Sobremesa is not null and Lanche is null and Bebida is null)
--            or (Acompanhamento is null and Sobremesa is null and Lanche is not null and Bebida is null)
--            or (Acompanhamento is null and Sobremesa is null and Lanche is null and Bebida is not null)
--            or (Acompanhamento is null and Sobremesa is null and Lanche is null and Bebida is null)); 

-- alter table Salao add constraint ID_Salao_Ambie_FK
--      foreign key (Id_Amb)
--      references Ambiente;

-- alter table Sobremesa add constraint REF_Sobre_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Sobremesa add constraint ID_Sobre_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;


-- -- Index Section
-- -- _____________ 

-- create unique index ID_Acomp_Produ_IND
--      on Acompanhamento (Indice_prod);

-- create index REF_Acomp_Estoq_IND
--      on Acompanhamento (Indice_estoq);

-- create unique index Id_Ambiente_IND
--      on Ambiente (Id_Amb);

-- create unique index SId_Ambie_Estoq_IND
--      on Ambiente (Indice_estoq);

-- create unique index ID_Avaliacao_IND
--      on Avaliacao (Indice_av);

-- create unique index ID_Bebid_Produ_IND
--      on Bebida (Indice_prod);

-- create index REF_Bebid_Estoq_IND
--      on Bebida (Indice_estoq);

-- create unique index ID_Brinde_IND
--      on Brinde (Id_brinde);

-- create unique index SID_Brind_Lanch_IND
--      on Brinde (Indice_prod);

-- create index REF_Brind_Estoq_IND
--      on Brinde (Indice_estoq);

-- create unique index ID_C_Escolhe_P_IND
--      on C_Escolhe_P (Indice_prod, Id_cliente);

-- create index EQU_C_Esc_Clien_IND
--      on C_Escolhe_P (Id_cliente);

-- create unique index ID_C_Reg_Pedid_IND
--      on C_Registra_A (Id_pedido);

-- create unique index SID_C_Reg_Clien_IND
--      on C_Registra_A (Id_cliente);

-- create unique index SID_C_Reg_Avali_IND
--      on C_Registra_A (Indice_av);

-- create unique index ID_Cliente_IND
--      on Cliente (Id_cliente);

-- create unique index ID_Cozin_Ambie_IND
--      on Cozinha (Id_Amb);

-- create unique index ID_Estoque_IND
--      on Estoque (Indice_estoq);

-- create unique index ID_F_CompostaPor_A_IND
--      on F_CompostaPor_A (Id_franquia, Id_Amb);

-- create index EQU_F_Com_Ambie_IND
--      on F_CompostaPor_A (Id_Amb);

-- create unique index ID_F_Vende_P_IND
--      on F_Vende_P (Indice_prod, Id_franquia);

-- create index EQU_F_Ven_Franq_IND
--      on F_Vende_P (Id_franquia);

-- create unique index ID_Franquia_IND
--      on Franquia (Id_franquia);

-- create unique index ID_Funcionario_IND
--      on Funcionario (Id_func);

-- create index EQU_Funci_Franq_IND
--      on Funcionario (Id_franquia);

-- create unique index ID_Ingrediente_IND
--      on Ingrediente (Id_ingred);

-- create index REF_Ingre_Estoq_IND
--      on Ingrediente (Indice_estoq);

-- create unique index ID_L_Contem_I_IND
--      on L_Contem_I (Id_ingred, Indice_prod);

-- create index EQU_L_Con_Lanch_IND
--      on L_Contem_I (Indice_prod);

-- create unique index ID_Lanch_Produ_IND
--      on Lanche (Indice_prod);

-- create unique index ID_Pedido_IND
--      on Pedido (Id_pedido);

-- create index REF_Pedid_Funci_IND
--      on Pedido (Id_func);

-- create index EQU_Pedid_Clien_IND
--      on Pedido (Id_cliente);

-- create unique index ID_Produto_IND
--      on Produto (Indice_prod);

-- create unique index ID_Salao_Ambie_IND
--      on Salao (Id_Amb);

-- create index REF_Sobre_Estoq_IND
--      on Sobremesa (Indice_estoq);

-- create unique index ID_Sobre_Produ_IND
--      on Sobremesa (Indice_prod);

