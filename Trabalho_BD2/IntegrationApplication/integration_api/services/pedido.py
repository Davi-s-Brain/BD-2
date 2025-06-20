from typing import List, Optional, Dict, Tuple

from Trabalho_BD2.IntegrationApplication.integration_api.models.pedido import Pedido


class PedidoService:
    def __init__(self):
        self.pedido_model = Pedido()

    def criar_pedido(self, data: Dict) -> int:
        """Cria um novo pedido e retorna o ID gerado."""
        return self.pedido_model.create(data)

    def listar_pedidos(self) -> List[Tuple]:
        """Retorna todos os pedidos cadastrados."""
        return self.pedido_model.get_all()

    def buscar_pedido_por_id(self, pedido_id: int) -> Optional[Tuple]:
        """Busca um pedido específico pelo ID."""
        return self.pedido_model.get_by_id(pedido_id)

    def atualizar_pedido(self, pedido_id: int, dados: Dict) -> bool:
        """Atualiza os campos fornecidos de um pedido."""
        return self.pedido_model.update(pedido_id, dados)

    def deletar_pedido(self, pedido_id: int) -> bool:
        """Remove um pedido pelo ID."""
        return self.pedido_model.delete(pedido_id)
