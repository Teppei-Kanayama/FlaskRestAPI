from typing import Dict, Any, Optional

from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    def __init__(self, name: str, price: float) -> None:
        self.name = name
        self.price = price

    def json(self) -> Dict[str, Any]:
        return {'name': self.name, 'price': self.price}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # def insert_items(self) -> None:
    #     connection = sqlite3.connect('db/data.db')
    #     cursor = connection.cursor()
    #     query = "INSERT INTO items VALUES (?, ?)"
    #     cursor.execute(query, (self.name, self.price))
    #     connection.commit()
    #     connection.close()
    #
    # def update_items(self) -> None:
    #     connection = sqlite3.connect('db/data.db')
    #     cursor = connection.cursor()
    #     query = "UPDATE items SET price=? WHERE name=?"
    #     cursor.execute(query, (self.price, self.name))
    #     connection.commit()
    #     connection.close()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def find_by_name(name: str) -> Optional["ItemModel"]:
        # connection = sqlite3.connect('db/data.db')
        # cursor = connection.cursor()
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone()
        # connection.close()
        # if row:
        #     return ItemModel(*row)
        return ItemModel.query.filter_by(name=name).first()
