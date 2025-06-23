from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from typing import List, Optional, Dict, Any


class IngredienteService:
    def __init__(self):
        self.id: Optional[int] = None
        self.Tipo_ingred: Optional[str] = None
        self.Nome_ingred: Optional[str] = None
        self.Preco_venda_cliente: Optional[float] = None
        self.Peso_ingred: Optional[float] = None
        self.Indice_estoq: Optional[int] = None

    @staticmethod
    def create(Tipo_ingred: str, Nome_ingred: str, Preco_venda_cliente: float,
               Peso_ingred: float, Indice_estoq: int, Quantidade: int) -> int:
        """Cria um novo ingrediente e retorna o ID gerado."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO ingrediente 
                (Tipo_ingred, Nome_ingred, Preco_venda_cliente, Peso_ingred, Indice_estoq, Quantidade)
                VALUES (?, ?, ?, ?, ?, ?)""",
                (Tipo_ingred, Nome_ingred, Preco_venda_cliente, Peso_ingred, Indice_estoq, Quantidade)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        """Retorna todos os ingredientes."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT Id_ingred, Tipo_ingred, Nome_ingred, 
                Preco_venda_cliente, Peso_ingred, Indice_estoq, Quantidade 
                FROM ingrediente"""
            )
            colunas = [col[0] for col in cursor.description]
            return [dict(zip(colunas, row)) for row in cursor.fetchall()]

    @staticmethod
    def get_by_id(ingrediente_id: int) -> Optional[Dict[str, Any]]:
        """Busca um ingrediente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT Id_ingred, Tipo_ingred, Nome_ingred, 
                Preco_venda_cliente, Peso_ingred, Indice_estoq, Quantidade
                FROM ingrediente WHERE Id_ingred = ?""",
                (ingrediente_id,)
            )
            row = cursor.fetchone()
            if row:
                colunas = [col[0] for col in cursor.description]
                return dict(zip(colunas, row))
            return None
    @staticmethod
    def get_by_name(Nome_ingred: str) -> Optional[Dict[str, Any]]:
        """Busca um ingrediente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT Id_ingred, Tipo_ingred, Nome_ingred, 
                Preco_venda_cliente, Peso_ingred, Indice_estoq, Quantidade
                FROM ingrediente WHERE Nome_ingred = ?""",
                (Nome_ingred,)
            )
            row = cursor.fetchone()
            if row:
                colunas = [col[0] for col in cursor.description]
                return dict(zip(colunas, row))
            return None

    @staticmethod
    def update(ingrediente_id: int, dados: Dict[str, Any]) -> bool:
        """Atualiza um ingrediente existente."""
        campos = []
        valores = []
        for campo, valor in dados.items():
            if valor is not None:
                campos.append(f"{campo} = ?")
                valores.append(valor)

        if not campos:
            return False

        valores.append(ingrediente_id)
        query = f"""UPDATE ingrediente 
                   SET {', '.join(campos)}
                   WHERE Id_ingred = ?"""

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def delete(ingrediente_id: int) -> bool:
        """Remove um ingrediente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM ingrediente WHERE Id_ingred = ?",
                (ingrediente_id,)
            )
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def alterar_estoque(nome_ingrediente: str, quantidade: int) -> bool:
        """Altera a quantidade em estoque de um ingrediente.

        Args:
            nome_ingrediente: Nome do ingrediente a ser alterado
            quantidade: Quantidade a ser adicionada (positiva) ou removida (negativa)

        Returns:
            bool: True se a operação foi bem sucedida, False caso contrário
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            # Primeiro verifica se o ingrediente existe e pega a quantidade atual
            cursor.execute(
                "SELECT Quantidade FROM ingrediente WHERE Nome_ingred = ?",
                (nome_ingrediente,)
            )
            result = cursor.fetchone()

            if not result:
                return False  # Ingrediente não encontrado

            quantidade_atual = result[0]
            nova_quantidade = quantidade_atual + quantidade

            # Não permite estoque negativo
            if nova_quantidade < 0:
                return False

            # Atualiza o estoque
            cursor.execute(
                "UPDATE ingrediente SET Quantidade = ? WHERE Nome_ingred = ?",
                (nova_quantidade, nome_ingrediente)
            )
            conn.commit()
            return cursor.rowcount > 0