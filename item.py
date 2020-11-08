import sqlite3
from typing import Dict, List, Optional, Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price of the item')

    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return dict(name=row[0], price=row[1]), 200
        return dict(message="Item not found."), 404

    def post(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return dict(message=f'An item {name} already exists!'), 400
        data = self.parser.parse_args()
        item = dict(name=name, price=data['price'])
        items.append(item)
        return item, 201

    def delete(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return dict(message=f'An item {name} successfully deleted!'), 200

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
