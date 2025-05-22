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
               Peso_ingred: float, Indice_estoq: int) -> int:
        """Cria um novo ingrediente e retorna o ID gerado."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO ingrediente 
                (Tipo_ingred, Nome_ingred, Preco_venda_cliente, Peso_ingred, Indice_estoq)
                VALUES (?, ?, ?, ?, ?)""",
                (Tipo_ingred, Nome_ingred, Preco_venda_cliente, Peso_ingred, Indice_estoq)
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
                Preco_venda_cliente, Peso_ingred, Indice_estoq 
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
                Preco_venda_cliente, Peso_ingred, Indice_estoq 
                FROM ingrediente WHERE Id_ingred = ?""",
                (ingrediente_id,)
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