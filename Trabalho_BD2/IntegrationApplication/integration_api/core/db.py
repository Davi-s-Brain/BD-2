import sqlite3

DB_NAME = "local.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Tabela de Bebidas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Bebidas (
            Indice_prod INTEGER PRIMARY KEY AUTOINCREMENT,
            Marca TEXT NOT NULL,
            Sabor TEXT NOT NULL,
            Indice_estoq INTEGER NOT NULL,
            E_Alcolico BOOLEAN NOT NULL
        )
        """)

        # Tabela de Cliente
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Cliente (
            Id_cliente INTEGER PRIMARY KEY,
            Primeiro_nome_client TEXT NOT NULL,
            Ultimo_nome_client TEXT NOT NULL,
            Data_nascimento_client TEXT NOT NULL,
            CPF_client TEXT NOT NULL UNIQUE,
            Telefone_client TEXT NOT NULL,
            E_mail_client TEXT NOT NULL,
            Data_cadastro_client TEXT NOT NULL,
            Genero_client TEXT NOT NULL,
            E_intolerante_lactose BOOLEAN NOT NULL,
            E_celiaco BOOLEAN NOT NULL,
            E_vegetariano BOOLEAN NOT NULL,
            E_vegano BOOLEAN NOT NULL
        )
        """)

        # Tabela de Funcionário
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Funcionario (
            Id_func INTEGER PRIMARY KEY,
            Nome_func TEXT NOT NULL,
            CPF TEXT NOT NULL UNIQUE,
            Data_nasc_func TEXT NOT NULL,
            Cargo TEXT NOT NULL,
            Salario REAL NOT NULL,
            Data_admissao TEXT NOT NULL,
            Turno TEXT NOT NULL,
            Tipo_de_contrato TEXT NOT NULL,
            Status_func TEXT NOT NULL,
            Id_franquia INTEGER
        )
        """)

        # Tabela de Ingrediente
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ingrediente (
            Id_ingred INTEGER PRIMARY KEY,
            Tipo_ingred TEXT NOT NULL,
            Nome_ingred TEXT NOT NULL,
            Preco_venda_cliente REAL NOT NULL,
            Peso_ingred REAL NOT NULL,
            Indice_estoq INTEGER NOT NULL
        )
        """)

        # Tabela de Lanches
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Lanches (
            Id_lanche INTEGER PRIMARY KEY,
            Nome_lanche TEXT NOT NULL,
            Preco_venda REAL NOT NULL,
            Tipo TEXT NOT NULL
        )
        """)

        # Tabela de Pedidos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedido (
            Id_pedido INTEGER PRIMARY KEY,
            Data_pedido TEXT NOT NULL,
            Hora_pedido TEXT NOT NULL,
            Valor_total_pedido REAL NOT NULL,
            Forma_pagamento TEXT NOT NULL,
            E_delivery BOOLEAN NOT NULL,
            Observacao TEXT,
            Id_cliente INTEGER NOT NULL,
            Id_func INTEGER NOT NULL,
            FOREIGN KEY (Id_cliente) REFERENCES Cliente(Id_cliente),
            FOREIGN KEY (Id_func) REFERENCES Funcionario(Id_func)
        )
        """)

        # Tabela de Produto
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produto (
            Indice_prod INTEGER PRIMARY KEY,
            Nome_prod TEXT NOT NULL,
            Preco_prod REAL NOT NULL,
            Peso_prod REAL NOT NULL,
            Unidade_medida TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            Lanche BOOLEAN NOT NULL,
            Bebida BOOLEAN NOT NULL,
            Sobremesa BOOLEAN NOT NULL,
            Acompanhamento BOOLEAN NOT NULL
        )
        """)

        # Tabela de Pedido_Produto (relacionamento entre Pedido e Produto)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedido_Produto (
            Id_pedido INTEGER,
            Indice_prod INTEGER,
            Quantidade INTEGER NOT NULL,
            FOREIGN KEY (Id_pedido) REFERENCES Pedido(Id_pedido),
            FOREIGN KEY (Indice_prod) REFERENCES Produto(Indice_prod),
            PRIMARY KEY (Id_pedido, Indice_prod)
        )
        """)

        # Tabela de Estoque
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Estoque (
            Indice_estoq INTEGER PRIMARY KEY,
            Nome_produto TEXT NOT NULL,
            Quantidade INTEGER NOT NULL,
            Unidade_medida TEXT NOT NULL,
            Data_fabricacao TEXT NOT NULL,
            Data_validade TEXT NOT NULL,
            Lote TEXT NOT NULL,
            Preco_compra_mercado REAL NOT NULL
        )
        """)

        # Tabela de Ingredientes_Lanche (relacionamento entre Ingrediente e Lanche)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Ingredientes_Lanche (
            Id_lanche INTEGER,
            Id_ingred INTEGER,
            Quantidade INTEGER NOT NULL,
            FOREIGN KEY (Id_lanche) REFERENCES Lanches(Id_lanche),
            FOREIGN KEY (Id_ingred) REFERENCES Ingrediente(Id_ingred),
            PRIMARY KEY (Id_lanche, Id_ingred)
        )
        """)

        conn.commit()

def get_connection():
    return sqlite3.connect(DB_NAME)