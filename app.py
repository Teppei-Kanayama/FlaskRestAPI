from typing import Dict, List, Optional, Tuple

from flask import Flask, request
from flask_jwt import JWT, jwt_required
from flask_restful import Resource, Api

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'dummy'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items: List[Dict[str, str]] = []


class Item(Resource):
    @jwt_required()
    def get(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        item = next(filter(lambda x: x['name'] == name, items), None)
        return dict(item=item), 200 if item else 404

    def post(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return dict(message=f'An item {name} already exists!'), 400
        data = request.get_json()
        item = dict(name=name, price=data['price'])
        items.append(item)
        return item, 201


class ItemList(Resource):

    def get(self) -> Tuple[Dict[str, List], int]:
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
app.run(port=5000, debug=True)
