-- Database: RanBurguer

-- DROP DATABASE IF EXISTS "RanBurguer";

CREATE DATABASE "RanBurguer"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Portuguese_Brazil.1252'
    LC_CTYPE = 'Portuguese_Brazil.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- Tables Section
-- _____________ 

CREATE TABLE Cliente (
    Id_cliente serial PRIMARY KEY,
    Primeiro_nome_cliente varchar(50) NOT NULL,
    Ultimo_nome_cliente varchar(50) NOT NULL,
    Data_nascimento_cliente date NOT NULL,
    CPF_cliente varchar(14) UNIQUE NOT NULL,
    Telefone_cliente varchar(15),
    Email_cliente varchar(100),
    Data_cadastro_cliente date DEFAULT CURRENT_DATE,
    Genero_cliente varchar(10),
    E_intolerante_lactose boolean DEFAULT false,
    E_celiaco boolean DEFAULT false,
    E_vegetariano boolean DEFAULT false,
    E_vegano boolean DEFAULT false
);

CREATE TABLE Avaliacao (
    Indice_av serial PRIMARY KEY,
    NPS float NOT NULL,
    Campo_texto text,
    Data_av date DEFAULT CURRENT_DATE
);

CREATE TABLE Bebida (
    Indice_prod serial PRIMARY KEY,
    Marca varchar(50) NOT NULL,
    Sabor varchar(50),
    Gelo_e_limao boolean DEFAULT false,
    Canudo boolean DEFAULT false,
    Indice_estoq integer REFERENCES Estoque(Indice_estoq)
);

CREATE TABLE Ingrediente (
    Id_ingred serial PRIMARY KEY,
    Tipo_ingred varchar(50) NOT NULL,
    Nome_ingred varchar(50) NOT NULL,
    Preco_venda_cliente numeric(10,2) NOT NULL,
    Peso_ingred numeric(5,2) NOT NULL
);

CREATE TABLE Pedido (
    Id_pedido serial PRIMARY KEY,
    Data_pedido date DEFAULT CURRENT_DATE,
    Hora_pedido time DEFAULT CURRENT_TIME,
    Valor_total_pedido numeric(10,2) NOT NULL,
    Forma_pagamento varchar(20),
    E_delivery boolean DEFAULT false,
    Observacao text,
    Id_cliente integer REFERENCES Cliente(Id_cliente),
    Id_func integer REFERENCES Funcionario(Id_func)
);

CREATE TABLE Funcionario (
    Id_func serial PRIMARY KEY,
    Nome_func varchar(50) NOT NULL,
    CPF varchar(14) UNIQUE NOT NULL,
    Data_nasc_func date NOT NULL,
    Cargo varchar(50),
    Salario numeric(10,2),
    Data_admissao date DEFAULT CURRENT_DATE,
    Turno varchar(20),
    Tipo_de_contrato varchar(20),
    Status varchar(20)
);

CREATE TABLE Produto (
    Indice_prod serial PRIMARY KEY,
    Nome_prod varchar(50) NOT NULL,
    Preco_prod numeric(10,2) NOT NULL,
    Peso_prod numeric(5,2),
    Unidade_medida varchar(20),
    Categoria varchar(20)
);

create table Estoque (
    Indice_estoq serial not null,
    Nome_produto varchar(50) not null,
    Quantidade numeric(10,2) not null,
    Unidade_medida varchar(20) not null,
    Data_fabricacao date not null,
    Data_validade date not null,
    Lote numeric(10) not null,
    Preco_compra_mercado numeric(12,2) not null,
    constraint ID_Estoque_ID primary key (Indice_estoq)
);

create table Salao (
    ID_Amb numeric(10) not null,
    Quant_cadeira numeric(10) not null,
    Quant_mesa numeric(10) not null,
    Quant_caixa_atend numeric(10) not null,
    Quant_totens_atend numeric(10) not null,
    Quant_lixeiras numeric(10) not null,
    constraint ID_Salao_Ambie_ID primary key (ID_Amb)
);

create table Cozinha (
    ID_Amb numeric(10) not null,
    Quant_geladeira numeric(10) not null,
    Quant_chapas numeric(10) not null,
    Quant_fogao numeric(10) not null,
    Quant_fritadeira numeric(10) not null,
    constraint ID_Cozin_Ambie_ID primary key (ID_Amb)
);

create table Banheiro (
    ID_Amb numeric(10) not null,
    Tipo_banheiro varchar(20) not null,
    Acessivel char(1) not null check (Acessivel in ('S', 'N')),
    Trans_incluido char(1) not null check (Trans_incluido in ('S', 'N')),
    Quant_cabines numeric(10) not null,
    constraint ID_Banhe_Ambie_ID primary key (ID_Amb)
);

create table Produto (
    Indice_prod serial not null,
    Nome_prod varchar(50) not null,
    Preco_prod numeric(12,2) not null,
    Peso_prod numeric(10,3) not null,
    Unidade_medida varchar(20) not null,
    Categoria varchar(50) not null,
    Lanche boolean default false,
    Bebida boolean default false,
    constraint ID_Produto_ID primary key (Indice_prod)
);

create table Franquia (
    Id_franquia serial not null,
    Nome_franquia varchar(50) not null,
    CNPJ numeric(14) not null,
    Endereco_franq varchar(100) not null,
    E_mail_franq varchar(50) not null,
    Data_inauguracao_franq date not null,
    constraint ID_Franquia_ID primary key (Id_franquia)
);

create table C_Escolhe_P (
    Id_cliente numeric(10) not null,
    Indice_prod numeric(10) not null,
    constraint ID_C_Escolhe_P_ID primary key (Indice_prod, Id_cliente)
);

create table C_Registra_A (
    Id_pedido numeric(10) not null,
    Id_cliente numeric(10) not null,
    Indice_av numeric(10) not null,
    constraint ID_C_Reg_Pedid_ID primary key (Id_pedido),
    constraint SID_C_Reg_Clien_ID unique (Id_cliente),
    constraint SID_C_Reg_Avali_ID unique (Indice_av)
);

create table F_Atende_C (
    Id_cliente numeric(10) not null,
    Id_func numeric(10) not null,
    constraint ID_F_Atende_C_ID primary key (Id_cliente, Id_func)
);

create table F_CompostaPor_A (
    ID_Amb numeric(10) not null,
    Id_franquia numeric(10) not null,
    constraint ID_F_CompostaPor_A_ID primary key (Id_franquia, ID_Amb)
);

create table F_Monta_L (
    Id_func numeric(10) not null,
    Indice_prod numeric(10) not null,
    constraint ID_F_Monta_L_ID primary key (Indice_prod, Id_func)
);

create table F_Vende_P (
    Id_franquia numeric(10) not null,
    Indice_prod numeric(10) not null,
    constraint ID_F_Vende_P_ID primary key (Indice_prod, Id_franquia)
);

create table L_Contem_I (
    Id_ingred numeric(10) not null,
    Indice_prod numeric(10) not null,
    constraint ID_L_Contem_I_ID primary key (Id_ingred, Indice_prod)
);
