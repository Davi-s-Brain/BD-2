from Trabalho_BD2.IntegrationApplication.integration_api.core.db import get_connection

class ItemModel:
    def insert(self, name, description):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO items (name, description) VALUES (?, ?)",
                (name, description)
            )
            conn.commit()

    def get_all(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description FROM items")
            return cursor.fetchall()

    def update(self, item_id, name, description):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET name = ?, description = ? WHERE id = ?",
                (name, description, item_id)
            )
            conn.commit()
