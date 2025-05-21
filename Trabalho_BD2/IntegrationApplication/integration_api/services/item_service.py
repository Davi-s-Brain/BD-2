from Trabalho_BD2.IntegrationApplication.integration_api.models.item_model import ItemModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder

class ItemService:
    def __init__(self):
        self.model = ItemModel()

    def get_all_items(self):
        self.model.get_all()
    def create_item(self, item: ItemCreate):
        self.model.insert(item.name, item.description, item.quantity, item.value)

    def create_order(self, order: CreateOrder):
        self.model.create_order(order.name, order.id, order.product, order.quantity)

    def update_item(self, item: ItemUpdate):
        self.model.update(item.name, item.description, item.quantity, item.value)

    def listar_estoque(self):
        items = self.model.get_all()
        return [
            {
                "name": item[0],
                "description": item[1],
                "quantity": item[2],
                "value" : item[3]
            }
            for item in items
        ]

    def alterar_estoque(self, product, quantity_delta):
        self.model.alterar_estoque(product, quantity_delta)

    def get_item(self,name):
        return self.model.get_item(name)

    def delete(self,item):
        self.model.delete_item(item)

