import sqlite3
from typing import Dict, Any, Optional


class ItemModel:
    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def json(self) -> Dict[str, Any]:
        return {'name': self._name, 'price': self._price}

    def insert_items(self) -> None:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self._name, self._price))
        connection.commit()
        connection.close()

    def update_items(self) -> None:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self._price, self._name))
        connection.commit()
        connection.close()

    @staticmethod
    def find_by_name(name: str) -> Optional["ItemModel"]:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return ItemModel(*row)
