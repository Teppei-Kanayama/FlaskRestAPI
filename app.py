from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from security import authenticate, identity
from resources.user import UserRegister

app = Flask(__name__)
app.config['SQLARCHEMY_DATABASE_URI'] = 'sqlite///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dummy'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    from db import db
    app.run(port=5000, debug=True)
