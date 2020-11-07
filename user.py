import sqlite3
from typing import Tuple, Dict

from flask_restful import Resource, reqparse


class User:
    def __init__(self, id_: int, username: str, password: str) -> None:
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> "User":
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, id_: int) -> "User":
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (id_,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self) -> Tuple[Dict[str, str], int]:
        connection = sqlite3.connect('db/data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        data = self.parser.parse_args()
        cursor.execute(query, (data['username'], data['password']))
        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
