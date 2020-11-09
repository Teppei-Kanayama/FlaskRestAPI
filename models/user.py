import sqlite3


class UserModel:
    def __init__(self, id_: int, username: str, password: str) -> None:
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
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
    def find_by_id(cls, id_: int) -> "UserModel":
        connection = sqlite3.connect('db/data.db')
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
