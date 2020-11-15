from typing import Dict, Tuple, Any

from flask_restful import Resource

from flask_rest_api.models.store import StoreModel


class Store(Resource):

    def get(self, name: str) -> Tuple[Dict[str, Any], int]:
        store = StoreModel.find_by_name(name)
        if store:
            return store.json(), 200
        return dict(message="Store not found."), 404

    def post(self, name: str) -> Tuple[Dict[str, Any], int]:
        if StoreModel.find_by_name(name):
            return dict(message=f'An store with name {name} already exists!'), 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception:
            return dict(message='An error occurred creating store!'), 500
        return store.json(), 201

    def delete(self, name: str) -> Tuple[Dict[str, Any], int]:
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return dict(message=f'An store {name} deleted.'), 200


class StoreList(Resource):

    def get(self) -> Tuple[Dict[str, Any], int]:
        return {"stores": [store.json() for store in StoreModel.query.all()]}, 200
