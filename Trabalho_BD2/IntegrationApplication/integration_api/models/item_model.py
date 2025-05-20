from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection

class ItemModel:
    def insert(self, name, description, quantity, value):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, description, quantity, value) VALUES (?, ?, ?, ?)",
                (name, description, quantity, value)
            )
            conn.commit()

    def get_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, description, quantity, value FROM items")
            return cursor.fetchall()

    def update(self, names, description, quantity, value):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET description = ?, quantity = ?, value = ? WHERE name = ?",
                (description, quantity, value, name)
            )
            conn.commit()

    def alterar_estoque(self, name, quantity_delta):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET quantity = quantity + ? WHERE name = ?",
                (quantity_delta, name)
            )
            conn.commit()

    def get_item(self, name):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, description, quantity FROM items WHERE name = ?",
                (name,)
            )
            return cursor.fetchone()
    def create_order(self, name, product_id, product, quantity):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO orders (name, id, product, quantity) VALUES (?, ?, ?, ?)",
                (name, product_id, product, quantity)
            )
            conn.commit()
