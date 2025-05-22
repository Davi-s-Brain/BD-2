from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from typing import List, Optional, Tuple

class Ingrediente:
    def create(self, Tipo_ingred: str, Nome_ingred: str, Preco_venda_cliente: float, 
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

    def get_all(self) -> List[Tuple]:
        """Retorna todos os ingredientes."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT Id_ingred, Tipo_ingred, Nome_ingred, 
                Preco_venda_cliente, Peso_ingred, Indice_estoq 
                FROM ingrediente"""
            )
            return cursor.fetchall()

    def get_by_id(self, ingrediente_id: int) -> Optional[Tuple]:
        """Busca um ingrediente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT Id_ingred, Tipo_ingred, Nome_ingred, 
                Preco_venda_cliente, Peso_ingred, Indice_estoq 
                FROM ingrediente WHERE Id_ingred = ?""",
                (ingrediente_id,)
            )
            return cursor.fetchone()

    def update(self, ingrediente_id: int, dados: dict) -> bool:
        """Atualiza um ingrediente existente."""
        # Constrói a query dinamicamente baseada nos campos a serem atualizados
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

    def delete(self, ingrediente_id: int) -> bool:
        """Remove um ingrediente pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM ingrediente WHERE Id_ingred = ?",
                (ingrediente_id,)
            )
            conn.commit()
            return cursor.rowcount > 0