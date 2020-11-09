import sqlite3
from typing import Tuple, Dict

from flask_restful import Resource, reqparse

from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self) -> Tuple[Dict[str, str], int]:
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": f"The username {data['username']} already exists!"}, 400

        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201