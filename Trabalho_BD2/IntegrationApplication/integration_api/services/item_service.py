from Trabalho_BD2.IntegrationApplication.integration_api.models.item_model import ItemModel
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.item import ItemCreate, ItemUpdate
from Trabalho_BD2.IntegrationApplication.integration_api.schemas.order import CreateOrder
from Trabalho_BD2.IntegrationApplication.integration_api.services.ingrediente_service import IngredienteService


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
        ingredienteService = IngredienteService ()
        items = ingredienteService.get_all()
        return [
            {
                "id": item["Id_ingred"],
                "nome": item["Nome_ingred"],
                "tipo": item["Tipo_ingred"],
                "preco": item["Preco_venda_cliente"],
                "peso": item["Peso_ingred"],
                "quantidade": item["Indice_estoq"]
            }
            for item in items
        ]
    def alterar_estoque(self, product, quantity_delta):
        self.model.alterar_estoque(product, quantity_delta)

    def get_item(self,name):
        return self.model.get_item(name)

    def delete(self,item):
        self.model.delete_item(item)

    def get_orders(self):
        return self.model.get_all_orders()

    def create(self, data):
        return self.model.create_func(data)
