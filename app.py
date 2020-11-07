from typing import Dict, List, Optional, Tuple

from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

items: List[Dict[str, str]] = []


class Item(Resource):
    def get(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        for item in items:
            if item['name'] == name:
                return item, 200
        return dict(item=None), 404

    def post(self, name: str) -> Tuple[Dict[str, Optional[str]], int]:
        item = dict(name=name, price=12.00)
        items.append(item)
        return item, 201


api.add_resource(Item, '/item/<string:name>')
app.run(port=5000)
