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


-- Tables Section
-- _____________ 

create table Cliente (
     Id_cliente numeric(10) not null,
     Primeiro_nome_client varchar(15) not null,
     Ultimo_nome_client varchar(20) not null,
     Data_nascimento_client date not null,
     CPF_client numeric(11) not null,
     Telefone_client numeric(12) not null,
     E_mail_client varchar(50) not null,
     Data_cadastro_client date not null,
     Genero_client varchar(10) not null,
     E_intolerante_lactose boolean default false,
     E_celiaco boolean default false,
     E_vegetariano boolean default false,
     E_vegano boolean default false,
     constraint ID_Cliente_ID primary key (Id_cliente));

create table Avaliacao (
     Indice_av serial not null,
     NPS float(10) not null,
     Campo_texto text not null,
     Data_av date not null,
     constraint ID_Avaliacao_ID primary key (Indice_av));

create table Bebida (
     Indice_prod serial not null,
     Marca varchar(20) not null,
     Sabor varchar(15) not null,
     Tipo varchar(10) not null,
     Indice_estoq serial not null,
     E_Alcolico boolean not null,
     constraint ID_Bebid_Produ_ID primary key (Indice_prod));

create table Sobremesa (
     Indice_prod serial not null,
     Indice_estoq serial not null,
     constraint ID_Sobrem_Produ_ID primary key (Indice_prod));

create table Acompanhamento (
     Indice_prod serial not null,
     Indice_estoq serial not null,
     constraint ID_Acomp_Produ_ID primary key (Indice_prod));

create table Ingrediente (
     Id_ingred numeric(10) not null,
     Tipo_ingred varchar(10) not null,
     Nome_ingred varchar(30) not null,
     Preco_venda_cliente float(10) not null,
     Peso_ingred float(10) not null,
     Indice_estoq serial not null,
     constraint ID_Ingrediente_ID primary key (Id_ingred));

create table Ambiente (
     ID_Amb numeric(10) not null,
     Indice_estoq serial not null,
     Id_ambiente numeric(10) not null,
     Tamanho_ambiente float(10) not null,
     Quantidade_desse_ambiente integer not null,
     Nivel_limpeza varchar(10) not null,
     Detetizado boolean default true,
     Salao boolean default false,
     Cozinha boolean default false,
     Banheiro boolean default false,
     constraint ID_Ambiente_ID primary key (ID_Amb),
     constraint SID_Ambie_Estoq_ID unique (Indice_estoq));

create table Pedido (
     Id_pedido serial not null,
     Data_pedido date not null,
     Hora_pedido varchar(10) not null,
     Valor_total_pedido float(10) not null,
     Forma_pagamento varchar(10) not null,
     E_delivery boolean default false,
     Observacao varchar(50) not null,
     Id_cliente numeric(10) not null,
     Id_func numeric(10) not null,
     constraint ID_Pedido_ID primary key (Id_pedido));
	 --Id_pedido serial PRIMARY KEY
	 --Id_cliente integer REFERENCES Cliente(Id_cliente)
	 --Id_func integer REFERENCES Funcionario(Id_func)

create table Lanche (
     Indice_prod serial not null,
     Ingredientes varchar(10) not null,
     Tamanho_lanche varchar(10) not null,
     Acompanhamento varchar(10) not null,
     Sobremesa varchar(10) not null,
     constraint ID_Lanch_Produ_ID primary key (Indice_prod));

create table Funcionario (
     Id_func serial not null,
     Nome_func varchar(50) not null,
     CPF numeric(11) UNIQUE not null,
     Data_nasc_func date not null,
     Cargo varchar(10) not null,
     Salario float(10) not null,
     Data_admissao date not null,
     Turno varchar(10) not null,
     Tipo_de_contrato varchar(10) not null,
     Status_func varchar(10) not null,
     Id_franquia serial not null,
     constraint ID_Funcionario_ID primary key (Id_func));

create table Brinde (
     Id_brinde numeric(10) not null,
     Indice_prod serial not null,
     Tipo_brinde varchar(10) not null,
     Indice_estoq serial not null,
     constraint ID_Brinde_ID primary key (Id_brinde),
     constraint SID_Brind_Lanch_ID unique (Indice_prod));

create table Estoque (
     Indice_estoq serial not null,
     Nome_produto varchar(30) not null,
     Quantidade integer not null,
     Unidade_medida varchar(10) not null,
     Data_fabricacao date not null,
     Data_validade date not null,
     Lote numeric(10) not null,
     Preco_compra_mercado float(10) not null,
     constraint ID_Estoque_ID primary key (Indice_estoq));

create table Salao (
     ID_Amb numeric(10) not null,
     Quant_cadeira integer not null,
     Quant_mesa integer not null,
     Quant_caixa_atend integer not null,
     Quant_totens_atend integer not null,
     Quant_lixeiras integer not null,
     constraint ID_Salao_Ambie_ID primary key (ID_Amb));

create table Cozinha (
     ID_Amb numeric(10) not null,
     Quant_geladeira integer not null,
     Quant_chapas integer not null,
     Quant_fogao integer not null,
     Quant_fritadeira integer not null,
     constraint ID_Cozin_Ambie_ID primary key (ID_Amb));

create table Banheiro (
     ID_Amb numeric(10) not null,
     Tipo_banheiro varchar(10) not null,
     Aceesivel boolean default false,
     Trans_incluido boolean default false,
     Quant_cabines integer not null,
     constraint ID_Banhe_Ambie_ID primary key (ID_Amb));

create table Produto (
     Indice_prod serial not null,
     Nome_prod varchar(30) not null,
     Preco_prod float(10) not null,
     Peso_prod float(10) not null,
     Unidade_medida varchar(10) not null,
     Categoria varchar(10) not null,
     Lanche boolean default false,
     Bebida boolean default false,
     Sobremesa boolean default false,
     Acompanhamento boolean default false,
     constraint ID_Produto_ID primary key (Indice_prod));

create table Franquia (
     Id_franquia numeric(10) not null,
     Nome_franquia varchar(50) not null,
     CNPJ numeric(14) not null,
     Endereco_franq varchar(100) not null,
     E_mail_franq varchar(50) not null,
     Data_inauguracao_franq date not null,
     constraint ID_Franquia_ID primary key (Id_franquia));

create table C_Escolhe_P (
     Id_cliente numeric(10) not null,
     Indice_prod serial not null,
     constraint ID_C_Escolhe_P_ID primary key (Indice_prod, Id_cliente));

create table C_Registra_A (
     Id_pedido numeric(10) not null,
     Id_cliente numeric(10) not null,
     Indice_av serial not null,
     constraint ID_C_Reg_Pedid_ID primary key (Id_pedido),
     constraint SID_C_Reg_Clien_ID unique (Id_cliente),
     constraint SID_C_Reg_Avali_ID unique (Indice_av));

create table F_Atende_C (
     Id_cliente numeric(10) not null,
     Id_func numeric(10) not null,
     constraint ID_F_Atende_C_ID primary key (Id_cliente, Id_func));

create table F_CompostaPor_A (
     ID_Amb numeric(10) not null,
     Id_franquia numeric(10) not null,
     constraint ID_F_CompostaPor_A_ID primary key (Id_franquia, ID_Amb));

create table F_Monta_L (
     Id_func numeric(10) not null,
     Indice_prod serial not null,
     constraint ID_F_Monta_L_ID primary key (Indice_prod, Id_func));

create table F_Vende_P (
     Id_franquia numeric(10) not null,
     Indice_prod serial not null,
     constraint ID_F_Vende_P_ID primary key (Indice_prod, Id_franquia));

create table L_Contem_I (
     Id_ingred numeric(10) not null,
     Indice_prod serial not null,
     constraint ID_L_Contem_I_ID primary key (Id_ingred, Indice_prod));

-- Insert Section
-- ______________ 




-- Constraints Section
-- ___________________ 

-- alter table Cliente add constraint ID_Cliente_CHK
--      check(exists(select * from Pedido
--                   where Pedido.Id_cliente = Id_cliente)); 

-- alter table Cliente add constraint ID_Cliente_CHK
--      check(exists(select * from C_Escolhe_P
--                   where C_Escolhe_P.Id_cliente = Id_cliente)); 

-- alter table Cliente add constraint ID_Cliente_CHK
--      check(exists(select * from F_Atende_C
--                   where F_Atende_C.Id_cliente = Id_cliente)); 

-- alter table Avaliacao add constraint ID_Avaliacao_CHK
--      check(exists(select * from C_Registra_A
--                   where C_Registra_A.Indice_av = Indice_av)); 

-- alter table Bebida add constraint ID_Bebid_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;

-- alter table Bebida add constraint REF_Bebid_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Sobremesa add constraint ID_Sobrem_Produ_FK
--      foreign key (Indice_prod) 
--      references Estoque;

-- alter table Acompanhamento add constraint ID_Acomp_Produ_FK
--      foreign key (Indice_prod)
--      references Estoque;

-- alter table Ingrediente add constraint REF_Ingre_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Ambiente add constraint ID_Ambiente_CHK
--      check(exists(select * from F_CompostaPor_A
--                   where F_CompostaPor_A.ID_Amb = ID_Amb)); 

-- alter table Ambiente add constraint EXCL_Ambiente
--      check((Banheiro is not null and Cozinha is null and Salao is null and Indice_estoq is null)
--            or (Banheiro is null and Cozinha is not null and Salao is null and Indice_estoq is null)
--            or (Banheiro is null and Cozinha is null and Salao is not null and Indice_estoq is null)
--            or (Banheiro is null and Cozinha is null and Salao is null and Indice_estoq is not null)
--            or (Banheiro is null and Cozinha is null and Salao is null and Indice_estoq is null)); 

-- alter table Ambiente add constraint SID_Ambie_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Pedido add constraint EQU_Pedid_Clien_FK
--      foreign key (Id_cliente)
--      references Cliente;

-- alter table Pedido add constraint REF_Pedid_Funci_FK
--      foreign key (Id_func)
--      references Funcionario;

-- alter table Lanche add constraint ID_Lanch_Produ_CHK
--      check(exists(select * from F_Monta_L
--                   where F_Monta_L.Indice_prod = Indice_prod)); 

-- alter table Lanche add constraint ID_Lanch_Produ_CHK
--      check(exists(select * from L_Contem_I
--                   where L_Contem_I.Indice_prod = Indice_prod)); 

-- alter table Lanche add constraint ID_Lanch_Produ_FK
--      foreign key (Indice_prod)
--      references Produto;

-- alter table Funcionario add constraint EQU_Funci_Franq_FK
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table Brinde add constraint REF_Brind_Estoq_FK
--      foreign key (Indice_estoq)
--      references Estoque;

-- alter table Brinde add constraint SID_Brind_Lanch_FK
--      foreign key (Indice_prod)
--      references Lanche;

-- alter table Estoque add constraint ID_Estoque_CHK
--      check(exists(select * from Ambiente
--                   where Ambiente.Indice_estoq = Indice_estoq)); 

-- alter table Salao add constraint ID_Salao_Ambie_FK
--      foreign key (ID_Amb)
--      references Ambiente;

-- alter table Cozinha add constraint ID_Cozin_Ambie_FK
--      foreign key (ID_Amb)
--      references Ambiente;

-- alter table Banheiro add constraint ID_Banhe_Ambie_FK
--      foreign key (ID_Amb)
--      references Ambiente;

-- alter table Produto add constraint ID_Produto_CHK
--      check(exists(select * from F_Vende_P
--                   where F_Vende_P.Indice_prod = Indice_prod)); 

-- alter table Produto add constraint EXCL_Produto
--      check((Lanche is not null and Bebida is null)
--            or (Lanche is null and Bebida is not null)
--            or (Lanche is null and Bebida is null)); 

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from Funcionario
--                   where Funcionario.Id_franquia = Id_franquia)); 

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from F_CompostaPor_A
--                   where F_CompostaPor_A.Id_franquia = Id_franquia)); 

-- alter table Franquia add constraint ID_Franquia_CHK
--      check(exists(select * from F_Vende_P
--                   where F_Vende_P.Id_franquia = Id_franquia)); 

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

-- alter table F_Atende_C add constraint REF_F_Ate_Funci_FK
--      foreign key (Id_func)
--      references Funcionario;

-- alter table F_Atende_C add constraint EQU_F_Ate_Clien
--      foreign key (Id_cliente)
--      references Cliente;

-- alter table F_CompostaPor_A add constraint EQU_F_Com_Franq
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table F_CompostaPor_A add constraint EQU_F_Com_Ambie_FK
--      foreign key (ID_Amb)
--      references Ambiente;

-- alter table F_Monta_L add constraint EQU_F_Mon_Lanch
--      foreign key (Indice_prod)
--      references Lanche;

-- alter table F_Monta_L add constraint REF_F_Mon_Funci_FK
--      foreign key (Id_func)
--      references Funcionario;

-- alter table F_Vende_P add constraint EQU_F_Ven_Produ
--      foreign key (Indice_prod)
--      references Produto;

-- alter table F_Vende_P add constraint EQU_F_Ven_Franq_FK
--      foreign key (Id_franquia)
--      references Franquia;

-- alter table L_Contem_I add constraint EQU_L_Con_Lanch_FK
--      foreign key (Indice_prod)
--      references Lanche;

-- alter table L_Contem_I add constraint REF_L_Con_Ingre
--      foreign key (Id_ingred)
--      references Ingrediente;


-- Index Section
-- _____________ 
