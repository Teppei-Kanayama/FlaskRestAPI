import sqlite3
from typing import Dict, List, Optional, Tuple

from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='Price of the item')

    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return dict(message="Item not found."), 404

    def post(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        if ItemModel.find_by_name(name):
            return dict(message=f'An item {name} already exists!'), 400
        posted_data = self.parser.parse_args()
        item = ItemModel(name=name, price=posted_data['price'])
        try:
            item.save_to_db()
        except Exception:
            return dict(message='An error occurred inserting item!'), 500
        return item.json(), 201

    def delete(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return dict(message=f'An item {name} successfully deleted!'), 200
        return dict(message=f"An item {name} doesn't exist!"), 200

    def put(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.price = data['price']
            except Exception:
                return dict(message='An error occurred updating item!'), 500
        else:
            try:
                item = ItemModel(name=name, price=data['price'])
            except Exception:
                return dict(message='An error occurred inserting item!'), 500
        item.save_to_db()
        return item.json(), 201


class ItemList(Resource):
    def get(self) -> Tuple[Dict[str, List], int]:
        return {"items": [item.json() for item in ItemModel.query.all()]}, 200
