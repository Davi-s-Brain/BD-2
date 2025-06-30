from __future__ import annotations
from typing import List, Optional
from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection
from Trabalho_BD2.IntegrationApplication.integration_api.db.database_acess import DatabaseAccess
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemOut


class ItemModel:
    def __init__(self, db_access: DatabaseAccess = None):
        self.db = db_access or DatabaseAccess(get_connection)

    def insert(self, name: str, description: str, quantity: int, value: float) -> bool:
        """
        Insere um novo item no banco de dados (mantido o nome original)

        Args:
            name: Nome do item
            description: Descrição do item
            quantity: Quantidade em estoque
            value: Valor do item

        Returns:
            bool: True se inserido com sucesso
        """
        item_data = {
            'name': name,
            'description': description,
            'quantity': quantity,
            'value': value
        }
        self.db.add("items", item_data)
        return True

    def get_all(self) -> List[ItemOut]:
        """
        Retorna todos os itens (mantido o nome original)

        Returns:
            List[ItemOut]: Lista de todos os itens
        """
        rows = self.db.get("items")
        return [ItemOut(**row) for row in rows]

    def update(self, name: str, description: str, quantity: int, value: float) -> bool:
        """
        Atualiza um item (mantido o nome original)

        Args:
            name: Nome do item a ser atualizado
            description: Nova descrição
            quantity: Nova quantidade
            value: Novo valor

        Returns:
            bool: True se atualizado com sucesso
        """
        update_data = {
            'description': description,
            'quantity': quantity,
            'value': value
        }
        return self.db.update("items", update_data, {"name": name})

    def alterar_estoque(self, name: str, quantity_delta: int) -> bool:
        """
        Altera o estoque de um item (mantido o nome original)

        Args:
            name: Nome do item
            quantity_delta: Valor a ser adicionado/subtraído

        Returns:
            bool: True se atualizado com sucesso
        """
        # Primeiro obtemos o valor atual
        current = self.get_item(name)
        if not current:
            return False

        # Calculamos o novo valor
        new_quantity = current.quantity + quantity_delta

        # Atualizamos usando o método padrão
        return self.db.update(
            "items",
            {"quantity": new_quantity},
            {"name": name}
        )

    def get_item(self, name: str) -> Optional[ItemOut]:
        """
        Obtém um item pelo nome (mantido o nome original)

        Args:
            name: Nome do item

        Returns:
            ItemOut se encontrado, None caso contrário
        """
        row = self.db.get_one("items", conditions={"name": name})
        return ItemOut(**row) if row else None

    def create_order(self, name: str, product_id: int, product: str, quantity: int) -> bool:
        """
        Cria um novo pedido (mantido o nome original)

        Args:
            name: Nome do cliente
            product_id: ID do produto
            product: Nome do produto
            quantity: Quantidade

        Returns:
            bool: True se criado com sucesso
        """
        order_data = {
            'name': name,
            'id': product_id,
            'product': product,
            'quantity': quantity
        }
        self.db.add("orders", order_data)
        return True

    def delete_item(self, name: str) -> bool:
        """
        Deleta um item (mantido o nome original)

        Args:
            name: Nome do item a ser deletado

        Returns:
            bool: True se deletado com sucesso
        """
        return self.db.delete("items", {"name": name})