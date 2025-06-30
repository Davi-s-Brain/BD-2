from __future__ import annotations

from datetime import date, time
from typing import List, Optional
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut


class PedidoModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.db = db_access or DatabaseAccess(get_connection)

    def create(self, pedido: PedidoCreate) -> PedidoOut:
        """
        Cria um novo pedido no banco de dados

        Args:
            pedido: Dados do pedido a ser criado

        Returns:
            PedidoOut: Pedido criado com ID gerado
        """
        # Cria um dicionário com os dados do pedido
        if pedido.Id_pedido is not None:
            pedido.Id_pedido = None

        pedido_dict = pedido.model_dump()

        # Converte datas e horas para string ISO
        if 'Data_pedido' in pedido_dict and pedido_dict['Data_pedido'] is not None:
            pedido_dict['Data_pedido'] = pedido_dict['Data_pedido'].isoformat()

        if 'Hora_pedido' in pedido_dict and pedido_dict['Hora_pedido'] is not None:
            pedido_dict['Hora_pedido'] = str(pedido_dict['Hora_pedido'])
        pedido_dict['Id_pedido'] = self.get_proximo_id_pedido(self.db)

        # Envia os dados convertidos para o banco de dados
        self.db.add("pedido", pedido_dict)
        pedidoOut = self.get_by_id(pedido_dict['Id_pedido'])
        return pedidoOut
    def get_all(self) -> List[PedidoOut]:
        """
        Retorna todos os pedidos cadastrados

        Returns:
            Lista de PedidoOut
        """
        rows = self.db.get("pedido")
        return [self._row_to_pedido_out(row) for row in rows]

    def get_proximo_id_pedido(self, db: DatabaseAccess) -> int:
        """Garante que o próximo Id_pedido seja baseado no maior valor numérico real"""
        try:
            resultado = db._execute_query(
                "SELECT MAX(CAST(Id_pedido AS INTEGER)) AS max_id FROM Pedido",
                fetch=True
            )

            ultimo_id = resultado[0]['max_id'] if resultado and resultado[0]['max_id'] is not None else 0
            return int(ultimo_id) + 1

        except Exception as e:
            raise RuntimeError(f"Erro ao obter próximo Id_pedido: {e}")

    def get_by_id(self, pedido_id: int) -> Optional[PedidoOut]:
        """
        Busca um pedido pelo ID

        Args:
            pedido_id: ID do pedido

        Returns:
            PedidoOut se encontrado, None caso contrário
        """
        row = self.db.get_one("Pedido", conditions={"Id_pedido": pedido_id})
        return self._row_to_pedido_out(row) if row else None

    def update(self, pedido_id: int, update_data: PedidoUpdate) -> Optional[PedidoOut]:
        """
        Atualiza os dados de um pedido

        Args:
            pedido_id: ID do pedido a ser atualizado
            update_data: Dados parciais para atualização

        Returns:
            PedidoOut atualizado se encontrado, None caso contrário
        """
        update_dict = update_data.model_dump(exclude_unset=True)

        # Converte datas e horas para string se presentes
        if 'Data_pedido' in update_dict:
            update_dict['Data_pedido'] = update_dict['Data_pedido'].isoformat()
        if 'Hora_pedido' in update_dict:
            update_dict['Hora_pedido'] = update_dict['Hora_pedido'].isoformat()

        if not update_dict:
            return self.get_by_id(pedido_id)

        self.db.update("pedido", update_dict, {"Id_pedido": pedido_id})
        return self.get_by_id(pedido_id)

    def delete(self, pedido_id: int) -> bool:
        """
        Remove um pedido do banco de dados

        Args:
            pedido_id: ID do pedido a ser removido

        Returns:
            True se removido com sucesso, False caso contrário
        """
        # Verifica se existe antes de deletar
        if not self.get_by_id(pedido_id):
            return False

        self.db.delete("pedido", {"Id_pedido": pedido_id})
        return True

    from datetime import date, time

    def _row_to_pedido_out(self, row: dict) -> PedidoOut:
        """
        Converte uma linha do banco para o schema PedidoOut

        Args:
            row: Dicionário com dados do pedido

        Returns:
            PedidoOut: Pedido convertido
        """
        # Converte Data_pedido
        if 'Data_pedido' in row and row['Data_pedido']:
            if isinstance(row['Data_pedido'], str):
                row['Data_pedido'] = date.fromisoformat(row['Data_pedido'])

        # Converte Hora_pedido
        if 'Hora_pedido' in row and row['Hora_pedido']:
            time_str = row['Hora_pedido']
            if isinstance(time_str, str):
                time_str = time_str.strip().split('T')[-1]  # Remove data se vier no formato ISO
                time_str = time_str.split('.')[0]  # Remove microssegundos
                parts = list(map(int, time_str.split(':')))
                if len(parts) == 3:
                    hours, minutes, seconds = parts
                elif len(parts) == 2:
                    hours, minutes = parts
                    seconds = 0
                else:
                    raise ValueError(f"Formato inválido de hora: {time_str}")
                row['Hora_pedido'] = time(hours, minutes, seconds)
        return PedidoOut(**row)
