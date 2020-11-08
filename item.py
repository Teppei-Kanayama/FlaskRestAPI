import sqlite3
from typing import Dict, List, Optional, Tuple, Any

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price of the item')

    @classmethod
    def _find_by_name(cls, name: str) -> Optional[Dict[str, Any]]:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return dict(name=row[0], price=row[1])

    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        item = self._find_by_name(name)
        if item:
            return item, 200
        return dict(message="Item not found."), 404

    def post(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        if self._find_by_name(name):
            return dict(message=f'An item {name} already exists!'), 400
        posted_data = self.parser.parse_args()
        item = dict(name=name, price=posted_data['price'])

        # TODO: functionize
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (item['name'], item['price']))
        connection.commit()
        connection.close()

        return item, 201

    def delete(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name, ))
        connection.commit()
        connection.close()
        return dict(message=f'An item {name} successfully deleted!'), 200  # TODO: detect when failing to dalete.

    def put(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        data = self.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)

        # create a new item
        if item is None:
            item = dict(name=name, price=data['price'])
            items.append(item)
            return item, 201

        # update an existing item
        item.update(data)
        return item, 201


class ItemList(Resource):
    def get(self) -> Tuple[Dict[str, List], int]:
        return {'items': items}, 200
