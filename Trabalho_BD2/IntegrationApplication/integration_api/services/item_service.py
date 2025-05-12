from integration_api.models.item_model import ItemModel
from integration_api.schemas.item import ItemCreate, ItemUpdate

class ItemService:
    def __init__(self):
        self.model = ItemModel()

    def get_all_items(self):
        self.model.get_all()

    def create_item(self, item: ItemCreate):
        self.model.insert(item.name, item.description)

    def update_item(self, item_id: int, item: ItemUpdate):
        self.model.update(item_id, item.name, item.description)
