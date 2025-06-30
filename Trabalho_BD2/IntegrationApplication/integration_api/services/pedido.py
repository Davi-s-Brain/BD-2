from typing import List, Optional
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.pedido import PedidoCreate, PedidoUpdate, PedidoOut
from Trabalho_BD2.IntegrationApplication.integration_api.models.pedido import PedidoModel


class PedidoService:
    def __init__(self, pedido_model: PedidoModel = None):
        self.model = pedido_model or PedidoModel()

    def criar_pedido(self, pedido_data: PedidoCreate) -> PedidoOut:
        """
        Cria um novo pedido

        Args:
            pedido_data: Dados do pedido a ser criado

        Returns:
            PedidoOut: Pedido criado
        """
        return self.model.create(pedido_data)

    def listar_pedidos(self) -> List[PedidoOut]:
        """
        Retorna todos os pedidos cadastrados

        Returns:
            Lista de PedidoOut
        """
        return self.model.get_all()

    def buscar_pedido_por_id(self, pedido_id: int) -> Optional[PedidoOut]:
        """
        Busca um pedido pelo ID

        Args:
            pedido_id: ID do pedido

        Returns:
            PedidoOut se encontrado, None caso contrário
        """
        return self.model.get_by_id(pedido_id)

    def atualizar_pedido(self, pedido_id: int, update_data: PedidoUpdate) -> Optional[PedidoOut]:
        """
        Atualiza os dados de um pedido

        Args:
            pedido_id: ID do pedido a ser atualizado
            update_data: Dados parciais para atualização

        Returns:
            PedidoOut atualizado se encontrado, None caso contrário
        """
        return self.model.update(pedido_id, update_data)

    def deletar_pedido(self, pedido_id: int) -> bool:
        """
        Remove um pedido

        Args:
            pedido_id: ID do pedido a ser removido

        Returns:
            True se removido com sucesso, False caso contrário
        """
        return self.model.delete(pedido_id)