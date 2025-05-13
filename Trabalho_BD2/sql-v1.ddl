-- *********************************************
-- * Standard SQL generation                   
-- *--------------------------------------------
-- * DB-MAIN version: 11.0.2              
-- * Generator date: Sep 14 2021              
-- * Generation date: Tue May 13 20:31:12 2025 
-- * LUN file: C:\Users\Windows\OneDrive\Área de Trabalho\Trabalho_BD2\Trabalho BD2 v1.lun 
-- * Schema: SCRIPT/SQL 
-- ********************************************* 


-- Database Section
-- ________________ 

create database SCRIPT;


-- DBSpace Section
-- _______________


-- Tables Section
-- _____________ 

create table Cliente (
     Id_cliente numeric(1) not null,
     Primeiro_nome_client varchar(1) not null,
     Ultimo_nome_client varchar(1) not null,
     Data_nascimento_client date not null,
     CPF_client numeric(1) not null,
     Telefone_client numeric(1) not null,
     E_mail_client varchar(1) not null,
     Data_cadastro_client date not null,
     Genero_client varchar(1) not null,
     E_intolerante_lactose char not null,
     E_celiaco char not null,
     E_vegetariano char not null,
     E_vegano char not null,
     constraint ID_Cliente_ID primary key (Id_cliente));

create table Avaliacao (
     Indice_av -- Index attribute not implemented -- not null,
     NPS float(1) not null,
     Campo_texto varchar(1) not null,
     Data_av date not null,
     constraint ID_Avaliacao_ID primary key (Indice_av));

create table Bebida (
     Indice_prod char(1) not null,
     Marca varchar(1) not null,
     Sabor varchar(1) not null,
     Gelo_e_limao char not null,
     Quer_destruir_o_planeta_com_canudo char not null,
     Indice_estoq -- Index attribute not implemented --,
     constraint ID_Bebid_Produ_ID primary key (Indice_prod));

create table Ingrediente (
     Id_ingred numeric(1) not null,
     Tipo_ingred varchar(1) not null,
     Nome_ingred varchar(1) not null,
     Preco_venda_cliente float(1) not null,
     Peso_ingred float(1) not null,
     Indice_estoq -- Index attribute not implemented --,
     constraint ID_Ingrediente_ID primary key (Id_ingred));

create table Ambiente (
     ID_Amb -- Sequence attribute not implemented -- not null,
     Indice_estoq -- Index attribute not implemented --,
     Id_ambiente numeric(1) not null,
     Tamanho_ambiente float(1) not null,
     Quantidade_desse_ambiente char(1) not null,
     Nivel_limpeza varchar(1) not null,
     Detetizado char not null,
     Salao numeric(10),
     Cozinha numeric(10),
     Banheiro numeric(10),
     constraint ID_Ambiente_ID primary key (ID_Amb),
     constraint SID_Ambie_Estoq_ID unique (Indice_estoq));

create table Pedido (
     Id_pedido numeric(1) not null,
     Number_pedido -- Index attribute not implemented -- not null,
     Data_pedido date not null,
     Hora_pedido varchar(1) not null,
     Valor_total_pedido float(1) not null,
     Forma_pagamento varchar(1) not null,
     E_delivery char not null,
     Observacao varchar(1) not null,
     Id_cliente numeric(1) not null,
     Id_func numeric(1) not null,
     constraint ID_Pedido_ID primary key (Id_pedido));

create table Lanche (
     Indice_prod char(1) not null,
     Ingredientes varchar(1) not null,
     Tamanho_lanche varchar(1) not null,
     Acompanhamento varchar(1) not null,
     constraint ID_Lanch_Produ_ID primary key (Indice_prod));

create table Funcionario (
     Id_func numeric(1) not null,
     Nome_func varchar(1) not null,
     CPF numeric(1) not null,
     Data_nasc_func date not null,
     Cargo varchar(1) not null,
     Salario float(1) not null,
     Data_admissao date not null,
     Turno varchar(1) not null,
     Tipo_de_contrato varchar(1) not null,
     Status varchar(1) not null,
     Id_franquia -- Index attribute not implemented -- not null,
     constraint ID_Funcionario_ID primary key (Id_func));

create table Brinde (
     Id_brinde numeric(1) not null,
     Indice_prod char(1) not null,
     Tipo_brinde varchar(1) not null,
     Indice_estoq -- Index attribute not implemented -- not null,
     constraint ID_Brinde_ID primary key (Id_brinde),
     constraint SID_Brind_Lanch_ID unique (Indice_prod));

create table Estoque (
     Indice_estoq -- Index attribute not implemented -- not null,
     Nome_produto varchar(1) not null,
     Quantidade float(1) not null,
     Unidade_medida varchar(1) not null,
     Data_fabricacao date not null,
     Data_validade date not null,
     Lote numeric(1) not null,
     Preco_compra_mercado float(1) not null,
     constraint ID_Estoque_ID primary key (Indice_estoq));

create table Salao (
     ID_Amb numeric(10) not null,
     Quant_cadeira float(1) not null,
     Quant_mesa float(1) not null,
     Quant_caixa_atend float(1) not null,
     Quant_totens_atend float(1) not null,
     Quant_lixeiras float(1) not null,
     constraint ID_Salao_Ambie_ID primary key (ID_Amb));

create table Cozinha (
     ID_Amb numeric(10) not null,
     Quant_geladeira float(1) not null,
     Quant_chapas float(1) not null,
     Quant_fogao char(1) not null,
     Quant_fritadeira char(1) not null,
     constraint ID_Cozin_Ambie_ID primary key (ID_Amb));

create table Banheiro (
     ID_Amb numeric(10) not null,
     Tipo_banheiro varchar(1) not null,
     Aceesivel char not null,
     Trans_incluido char not null,
     Quant_cabines float(1) not null,
     constraint ID_Banhe_Ambie_ID primary key (ID_Amb));

create table Produto (
     Indice_prod char(1) not null,
     Nome_prod varchar(1) not null,
     Preco_prod float(1) not null,
     Peso_prod float(1) not null,
     Unidade_medida float(1) not null,
     Categoria varchar(1) not null,
     Lanche char(1),
     Bebida char(1),
     constraint ID_Produto_ID primary key (Indice_prod));

create table Franquia (
     Id_franquia -- Index attribute not implemented -- not null,
     Nome_franquia varchar(1) not null,
     CNPJ numeric(1) not null,
     Endereco_franq varchar(1) not null,
     E_mail_franq varchar(1) not null,
     Data_inauguracao_franq date not null,
     constraint ID_Franquia_ID primary key (Id_franquia));

create table C_Escolhe_P (
     Id_cliente numeric(1) not null,
     Indice_prod char(1) not null,
     constraint ID_C_Escolhe_P_ID primary key (Indice_prod, Id_cliente));

create table C_Registra_A (
     Id_pedido numeric(1) not null,
     Id_cliente numeric(1) not null,
     Indice_av -- Index attribute not implemented -- not null,
     constraint ID_C_Reg_Pedid_ID primary key (Id_pedido),
     constraint SID_C_Reg_Clien_ID unique (Id_cliente),
     constraint SID_C_Reg_Avali_ID unique (Indice_av));

create table F_Atende_C (
     Id_cliente numeric(1) not null,
     Id_func numeric(1) not null,
     constraint ID_F_Atende_C_ID primary key (Id_cliente, Id_func));

create table F_CompostaPor_A (
     ID_Amb numeric(10) not null,
     Id_franquia -- Index attribute not implemented -- not null,
     constraint ID_F_CompostaPor_A_ID primary key (Id_franquia, ID_Amb));

create table F_Monta_L (
     Id_func numeric(1) not null,
     Indice_prod char(1) not null,
     constraint ID_F_Monta_L_ID primary key (Indice_prod, Id_func));

create table F_Vende_P (
     Id_franquia -- Index attribute not implemented -- not null,
     Indice_prod char(1) not null,
     constraint ID_F_Vende_P_ID primary key (Indice_prod, Id_franquia));

create table L_Contem_I (
     Id_ingred numeric(1) not null,
     Indice_prod char(1) not null,
     constraint ID_L_Contem_I_ID primary key (Id_ingred, Indice_prod));


-- Constraints Section
-- ___________________ 

alter table Cliente add constraint ID_Cliente_CHK
     check(exists(select * from Pedido
                  where Pedido.Id_cliente = Id_cliente)); 

alter table Cliente add constraint ID_Cliente_CHK
     check(exists(select * from C_Escolhe_P
                  where C_Escolhe_P.Id_cliente = Id_cliente)); 

alter table Cliente add constraint ID_Cliente_CHK
     check(exists(select * from F_Atende_C
                  where F_Atende_C.Id_cliente = Id_cliente)); 

alter table Avaliacao add constraint ID_Avaliacao_CHK
     check(exists(select * from C_Registra_A
                  where C_Registra_A.Indice_av = Indice_av)); 

alter table Bebida add constraint ID_Bebid_Produ_FK
     foreign key (Indice_prod)
     references Produto;

alter table Bebida add constraint REF_Bebid_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

alter table Ingrediente add constraint REF_Ingre_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

alter table Ambiente add constraint ID_Ambiente_CHK
     check(exists(select * from F_CompostaPor_A
                  where F_CompostaPor_A.ID_Amb = ID_Amb)); 

alter table Ambiente add constraint EXCL_Ambiente
     check((Banheiro is not null and Cozinha is null and Salao is null and Indice_estoq is null)
           or (Banheiro is null and Cozinha is not null and Salao is null and Indice_estoq is null)
           or (Banheiro is null and Cozinha is null and Salao is not null and Indice_estoq is null)
           or (Banheiro is null and Cozinha is null and Salao is null and Indice_estoq is not null)
           or (Banheiro is null and Cozinha is null and Salao is null and Indice_estoq is null)); 

alter table Ambiente add constraint SID_Ambie_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

alter table Pedido add constraint EQU_Pedid_Clien_FK
     foreign key (Id_cliente)
     references Cliente;

alter table Pedido add constraint REF_Pedid_Funci_FK
     foreign key (Id_func)
     references Funcionario;

alter table Lanche add constraint ID_Lanch_Produ_CHK
     check(exists(select * from F_Monta_L
                  where F_Monta_L.Indice_prod = Indice_prod)); 

alter table Lanche add constraint ID_Lanch_Produ_CHK
     check(exists(select * from L_Contem_I
                  where L_Contem_I.Indice_prod = Indice_prod)); 

alter table Lanche add constraint ID_Lanch_Produ_FK
     foreign key (Indice_prod)
     references Produto;

alter table Funcionario add constraint EQU_Funci_Franq_FK
     foreign key (Id_franquia)
     references Franquia;

alter table Brinde add constraint REF_Brind_Estoq_FK
     foreign key (Indice_estoq)
     references Estoque;

alter table Brinde add constraint SID_Brind_Lanch_FK
     foreign key (Indice_prod)
     references Lanche;

alter table Estoque add constraint ID_Estoque_CHK
     check(exists(select * from Ambiente
                  where Ambiente.Indice_estoq = Indice_estoq)); 

alter table Salao add constraint ID_Salao_Ambie_FK
     foreign key (ID_Amb)
     references Ambiente;

alter table Cozinha add constraint ID_Cozin_Ambie_FK
     foreign key (ID_Amb)
     references Ambiente;

alter table Banheiro add constraint ID_Banhe_Ambie_FK
     foreign key (ID_Amb)
     references Ambiente;

alter table Produto add constraint ID_Produto_CHK
     check(exists(select * from F_Vende_P
                  where F_Vende_P.Indice_prod = Indice_prod)); 

alter table Produto add constraint EXCL_Produto
     check((Lanche is not null and Bebida is null)
           or (Lanche is null and Bebida is not null)
           or (Lanche is null and Bebida is null)); 

alter table Franquia add constraint ID_Franquia_CHK
     check(exists(select * from Funcionario
                  where Funcionario.Id_franquia = Id_franquia)); 

alter table Franquia add constraint ID_Franquia_CHK
     check(exists(select * from F_CompostaPor_A
                  where F_CompostaPor_A.Id_franquia = Id_franquia)); 

alter table Franquia add constraint ID_Franquia_CHK
     check(exists(select * from F_Vende_P
                  where F_Vende_P.Id_franquia = Id_franquia)); 

alter table C_Escolhe_P add constraint REF_C_Esc_Produ
     foreign key (Indice_prod)
     references Produto;

alter table C_Escolhe_P add constraint EQU_C_Esc_Clien_FK
     foreign key (Id_cliente)
     references Cliente;

alter table C_Registra_A add constraint ID_C_Reg_Pedid_FK
     foreign key (Id_pedido)
     references Pedido;

alter table C_Registra_A add constraint SID_C_Reg_Clien_FK
     foreign key (Id_cliente)
     references Cliente;

alter table C_Registra_A add constraint SID_C_Reg_Avali_FK
     foreign key (Indice_av)
     references Avaliacao;

alter table F_Atende_C add constraint REF_F_Ate_Funci_FK
     foreign key (Id_func)
     references Funcionario;

alter table F_Atende_C add constraint EQU_F_Ate_Clien
     foreign key (Id_cliente)
     references Cliente;

alter table F_CompostaPor_A add constraint EQU_F_Com_Franq
     foreign key (Id_franquia)
     references Franquia;

alter table F_CompostaPor_A add constraint EQU_F_Com_Ambie_FK
     foreign key (ID_Amb)
     references Ambiente;

alter table F_Monta_L add constraint EQU_F_Mon_Lanch
     foreign key (Indice_prod)
     references Lanche;

alter table F_Monta_L add constraint REF_F_Mon_Funci_FK
     foreign key (Id_func)
     references Funcionario;

alter table F_Vende_P add constraint EQU_F_Ven_Produ
     foreign key (Indice_prod)
     references Produto;

alter table F_Vende_P add constraint EQU_F_Ven_Franq_FK
     foreign key (Id_franquia)
     references Franquia;

alter table L_Contem_I add constraint EQU_L_Con_Lanch_FK
     foreign key (Indice_prod)
     references Lanche;

alter table L_Contem_I add constraint REF_L_Con_Ingre
     foreign key (Id_ingred)
     references Ingrediente;


-- Index Section
-- _____________ 

create unique index ID_Cliente_IND
     on Cliente (Id_cliente);

create unique index ID_Avaliacao_IND
     on Avaliacao (Indice_av);

create unique index ID_Bebid_Produ_IND
     on Bebida (Indice_prod);

create index REF_Bebid_Estoq_IND
     on Bebida (Indice_estoq);

create unique index ID_Ingrediente_IND
     on Ingrediente (Id_ingred);

create index REF_Ingre_Estoq_IND
     on Ingrediente (Indice_estoq);

create unique index ID_Ambiente_IND
     on Ambiente (ID_Amb);

create unique index SID_Ambie_Estoq_IND
     on Ambiente (Indice_estoq);

create unique index ID_Pedido_IND
     on Pedido (Id_pedido);

create index EQU_Pedid_Clien_IND
     on Pedido (Id_cliente);

create index REF_Pedid_Funci_IND
     on Pedido (Id_func);

create unique index ID_Lanch_Produ_IND
     on Lanche (Indice_prod);

create unique index ID_Funcionario_IND
     on Funcionario (Id_func);

create index EQU_Funci_Franq_IND
     on Funcionario (Id_franquia);

create unique index ID_Brinde_IND
     on Brinde (Id_brinde);

create index REF_Brind_Estoq_IND
     on Brinde (Indice_estoq);

create unique index SID_Brind_Lanch_IND
     on Brinde (Indice_prod);

create unique index ID_Estoque_IND
     on Estoque (Indice_estoq);

create unique index ID_Salao_Ambie_IND
     on Salao (ID_Amb);

create unique index ID_Cozin_Ambie_IND
     on Cozinha (ID_Amb);

create unique index ID_Banhe_Ambie_IND
     on Banheiro (ID_Amb);

create unique index ID_Produto_IND
     on Produto (Indice_prod);

create unique index ID_Franquia_IND
     on Franquia (Id_franquia);

create unique index ID_C_Escolhe_P_IND
     on C_Escolhe_P (Indice_prod, Id_cliente);

create index EQU_C_Esc_Clien_IND
     on C_Escolhe_P (Id_cliente);

create unique index ID_C_Reg_Pedid_IND
     on C_Registra_A (Id_pedido);

create unique index SID_C_Reg_Clien_IND
     on C_Registra_A (Id_cliente);

create unique index SID_C_Reg_Avali_IND
     on C_Registra_A (Indice_av);

create unique index ID_F_Atende_C_IND
     on F_Atende_C (Id_cliente, Id_func);

create index REF_F_Ate_Funci_IND
     on F_Atende_C (Id_func);

create unique index ID_F_CompostaPor_A_IND
     on F_CompostaPor_A (Id_franquia, ID_Amb);

create index EQU_F_Com_Ambie_IND
     on F_CompostaPor_A (ID_Amb);

create unique index ID_F_Monta_L_IND
     on F_Monta_L (Indice_prod, Id_func);

create index REF_F_Mon_Funci_IND
     on F_Monta_L (Id_func);

create unique index ID_F_Vende_P_IND
     on F_Vende_P (Indice_prod, Id_franquia);

create index EQU_F_Ven_Franq_IND
     on F_Vende_P (Id_franquia);

create unique index ID_L_Contem_I_IND
     on L_Contem_I (Id_ingred, Indice_prod);

create index EQU_L_Con_Lanch_IND
     on L_Contem_I (Indice_prod);

