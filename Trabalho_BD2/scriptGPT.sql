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

CREATE TABLE Estoque (
    Indice_estoq serial PRIMARY KEY,
    Nome_produto varchar(50) NOT NULL,
    Quantidade numeric(10,2) NOT NULL,
    Unidade_medida varchar(20),
    Data_fabricacao date,
    Data_validade date,
    Lote varchar(20),
    Preco_compra numeric(10,2)
);
