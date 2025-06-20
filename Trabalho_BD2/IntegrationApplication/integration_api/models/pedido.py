from typing import List, Optional, Tuple, Dict
from datetime import date, time
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection


class Pedido:

    def create(self, data: Dict) -> int:
        """
        Cria um novo pedido. Espera um dicionário com as chaves:
        - Data_pedido, Hora_pedido, Valor_total_pedido, Forma_pagamento,
          E_delivery, Observacao, Id_cliente, Id_func
        """
        with get_connection() as conn:
            cursor = conn.cursor()

            # Converter datetime.date e datetime.time para strings
            data_pedido = data["Data_pedido"].isoformat() if isinstance(data["Data_pedido"], date) else data[
                "Data_pedido"]
            hora_pedido = data["Hora_pedido"].isoformat() if isinstance(data["Hora_pedido"], time) else data[
                "Hora_pedido"]

            cursor.execute("""
                INSERT INTO pedido (
                    Data_pedido, Hora_pedido, Valor_total_pedido,
                    Forma_pagamento, E_delivery, Observacao,
                    Id_cliente, Id_func
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data_pedido,
                hora_pedido,
                data["Valor_total_pedido"],
                data["Forma_pagamento"],
                data["E_delivery"],
                data.get("Observacao"),
                data["Id_cliente"],
                data["Id_func"]
            ))
            conn.commit()
            return cursor.lastrowid

    def get_all(self) -> List[Dict]:
        """Retorna todos os pedidos como dicionários."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Id_pedido, Data_pedido, Hora_pedido, Valor_total_pedido,
                       Forma_pagamento, E_delivery, Observacao,
                       Id_cliente, Id_func
                FROM pedido
            """)
            columns = [column[0] for column in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_by_id(self, pedido_id: int) -> Optional[Tuple]:
        """Busca um pedido pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Id_pedido, Data_pedido, Hora_pedido, Valor_total_pedido,
                       Forma_pagamento, E_delivery, Observacao,
                       Id_cliente, Id_func
                FROM pedido
                WHERE Id_pedido = ?
            """, (pedido_id,))
            return cursor.fetchone()

    def update(self, pedido_id: int, dados: dict) -> bool:
        """Atualiza os campos fornecidos de um pedido."""
        campos = []
        valores = []

        for campo, valor in dados.items():
            if valor is not None:
                # Converter datetime.date e datetime.time para strings
                if campo in ["Data_pedido", "Hora_pedido"]:
                    if isinstance(valor, date):
                        valor = valor.isoformat()
                    elif isinstance(valor, time):
                        valor = valor.isoformat()

                campos.append(f"{campo} = ?")
                valores.append(valor)

        if not campos:
            return False  # Nada a atualizar

        valores.append(pedido_id)

        query = f"""
            UPDATE pedido
            SET {', '.join(campos)}
            WHERE Id_pedido = ?
        """

        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, valores)
            conn.commit()
            return cursor.rowcount > 0

    def delete(self, pedido_id: int) -> bool:
        """Remove um pedido pelo ID."""
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pedido WHERE Id_pedido = ?", (pedido_id,))
            conn.commit()
            return cursor.rowcount > 0