import sqlite3
from typing import Dict, List, Tuple, Optional

DB_NAME = "data.sqlite"

MIGRATIONS_TABLE = """
CREATE TABLE IF NOT EXISTS migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""


class DatabaseManager:
    def __init__(self, db_name: str = DB_NAME):
        self.db_name = db_name

    def produtos_mais_vendidos_periodo(self, data_inicio: str, data_fim: str) -> List[Dict]:
        """
        Retorna os produtos mais vendidos em um período específico

        Args:
            data_inicio: Data de início no formato 'YYYY-MM-DD'
            data_fim: Data de fim no formato 'YYYY-MM-DD'

        Returns:
            Lista de dicionários com os produtos mais vendidos no período
        """
        query = """
        SELECT 
            pr.Indice_prod AS id_produto,
            pr.Nome_prod AS nome_produto,
            CASE 
                WHEN pr.Lanche = 1 THEN 'Lanche'
                WHEN pr.Bebida = 1 THEN 'Bebida'
                WHEN pr.Sobremesa = 1 THEN 'Sobremesa'
                WHEN pr.Acompanhamento = 1 THEN 'Acompanhamento'
                ELSE 'Outro'
            END AS tipo_produto,
            COUNT(*) AS quantidade_vendida
        FROM Pedido_Produto pp
        JOIN Pedido p ON pp.Id_pedido = p.Id_pedido
        JOIN Produto pr ON pp.Indice_prod = pr.Indice_prod
        WHERE p.Data_pedido BETWEEN ? AND ?
        GROUP BY pr.Indice_prod, pr.Nome_prod, pr.Lanche, pr.Bebida, pr.Sobremesa, pr.Acompanhamento
        ORDER BY quantidade_vendida DESC
        """

        return self._execute(query, (data_inicio, data_fim), fetch=True)
    def reset_carrinho_table(self):
        migration_name = "reset_carrinho_table"

        if self.migration_applied(migration_name):
            print(f"Migration '{migration_name}' já aplicada")
            return

        commands = [
            "DROP TABLE IF EXISTS Carrinho",
            """
            CREATE TABLE IF NOT EXISTS Carrinho (
                id_carrinho INTEGER PRIMARY KEY,
                id_usuario INTEGER NOT NULL,
                data_criacao TEXT NOT NULL,
                data_atualizacao TEXT NOT NULL
            )
            """
        ]

        self.apply_migration(migration_name, commands)

    def _execute(self, query: str, params: Tuple = None, fetch: bool = False) -> Optional[List[Dict]]:
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(query, params or ())

            if fetch:
                return [dict(row) for row in cursor.fetchall()]

            conn.commit()
            return None

    def migration_applied(self, name: str) -> bool:
        query = "SELECT id FROM migrations WHERE name = ?"
        return bool(self._execute(query, (name,), fetch=True))

    def column_exists(self, table: str, column: str) -> bool:
        """Verifica se uma coluna existe em uma tabela"""
        query = f"PRAGMA table_info({table})"
        columns = self._execute(query, fetch=True)
        return any(col['name'] == column for col in columns)

    def apply_migration(self, name: str, sql_commands: List[str]):
        """Aplica uma migração apenas se ela ainda não foi aplicada"""
        if self.migration_applied(name):
            print(f"Migration '{name}' já aplicada")
            return

        try:
            for cmd in sql_commands:
                self._execute(cmd)

            self._execute("INSERT INTO migrations (name) VALUES (?)", (name,))
            print(f"Migration '{name}' aplicada com sucesso")
        except Exception as e:
            print(f"Erro aplicando migration '{name}': {str(e)}")
            raise

    def add_quantidade_column(self):
        """Adiciona a coluna Quantidade apenas se ela não existir"""
        migration_name = "add_quantidade_to_ingrediente"
        column_name = "Quantidade"
        table_name = "Ingrediente"

        # Verifica se a coluna já existe
        if self.column_exists(table_name, column_name):
            print(f"Coluna '{column_name}' já existe na tabela '{table_name}'. Pulando migração.")
            # Registra a migração como aplicada mesmo que a coluna já exista
            if not self.migration_applied(migration_name):
                self._execute("INSERT INTO migrations (name) VALUES (?)", (migration_name,))
            return

        commands = [
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} INTEGER DEFAULT 1;"
        ]
        self.apply_migration(migration_name, commands)

    def delete_null_id_ingredientes(self):
        migration_name = "delete_null_id_ingredientes"

        if self.migration_applied(migration_name):
            print(f"Migration '{migration_name}' já aplicada")
            return

        commands = [
            "DELETE FROM Ingrediente WHERE Id_ingred IS NULL"
        ]

        self.apply_migration(migration_name, commands)

    def init_db(self):
        # Cria tabela de migrações primeiro
        self._execute(MIGRATIONS_TABLE)

        # Definições das tabelas
        tables = {
            "items": """
            CREATE TABLE IF NOT EXISTS items (
                name TEXT NOT NULL PRIMARY KEY,
                description TEXT,
                quantity INTEGER NOT NULL,
                value REAL NOT NULL
            )
            """,
            "Bebidas": """
            CREATE TABLE IF NOT EXISTS Bebidas (
                Indice_prod INTEGER PRIMARY KEY AUTOINCREMENT,
                Marca TEXT NOT NULL,
                Sabor TEXT NOT NULL,
                Indice_estoq INTEGER NOT NULL,
                E_Alcolico BOOLEAN NOT NULL
            )
            """,
            "orders": """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
            """,
            "Cliente": """
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
                E_vegano BOOLEAN NOT NULL,
                Senha_cliente TEXT NOT NULL
            )
            """,
            "Carrinho": """
            CREATE TABLE IF NOT EXISTS Carrinho (
                id_carrinho INTEGER PRIMARY KEY,
                id_usuario INTEGER NOT NULL,
                data_criacao TEXT NOT NULL,
                data_atualizacao TEXT NOT NULL
            )
            """,
            "Carrinho_Item": """
            CREATE TABLE IF NOT EXISTS Carrinho_Item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                id_carrinho INTEGER NOT NULL,
                id_item INTEGER NOT NULL,
                nome TEXT NOT NULL,
                preco REAL NOT NULL,
                quantidade INTEGER NOT NULL,
                observacoes TEXT,
                categoria TEXT,
                FOREIGN KEY (id_carrinho) REFERENCES Carrinho(id_carrinho)
            )
            """,
            "Funcionario": """
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
                Id_franquia INTEGER,
                Senha_func TEXT
            )
            """,
            "Ingrediente": """
            CREATE TABLE IF NOT EXISTS Ingrediente (
                Id_ingred INTEGER PRIMARY KEY,
                Tipo_ingred TEXT NOT NULL,
                Nome_ingred TEXT NOT NULL,
                Preco_venda_cliente REAL NOT NULL,
                Peso_ingred REAL NOT NULL,
                Indice_estoq INTEGER NOT NULL
            )
            """,
            "Lanches": """
            CREATE TABLE IF NOT EXISTS Lanches (
                Id_lanche INTEGER PRIMARY KEY,
                Nome_lanche TEXT NOT NULL,
                Preco_venda REAL NOT NULL,
                Tipo TEXT NOT NULL
            )
            """,
            "Pedido": """
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
            """,
            "Produto": """
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
            """,
            "Pedido_Produto": """
            CREATE TABLE IF NOT EXISTS Pedido_Produto (
                Id_pedido INTEGER,
                Indice_prod INTEGER,
                Quantidade INTEGER NOT NULL,
                FOREIGN KEY (Id_pedido) REFERENCES Pedido(Id_pedido),
                FOREIGN KEY (Indice_prod) REFERENCES Produto(Indice_prod),
                PRIMARY KEY (Id_pedido, Indice_prod)
            )
            """,
            "Estoque": """
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
            """,
            "Ingredientes_Lanche": """
            CREATE TABLE IF NOT EXISTS Ingredientes_Lanche (
                Id_lanche INTEGER,
                Id_ingred INTEGER,
                Quantidade INTEGER NOT NULL,
                FOREIGN KEY (Id_lanche) REFERENCES Lanches(Id_lanche),
                FOREIGN KEY (Id_ingred) REFERENCES Ingrediente(Id_ingred),
                PRIMARY KEY (Id_lanche, Id_ingred)
            )
            """
        }

        # Criar todas as tabelas
        for table_name, ddl in tables.items():
            self._execute(ddl)

        # Executar migração para adicionar coluna Quantidade
        self.add_quantidade_column()
        self.delete_null_id_ingredientes()


# Mantém a função get_connection para compatibilidade com outros módulos
def get_connection():
    return sqlite3.connect(DB_NAME)