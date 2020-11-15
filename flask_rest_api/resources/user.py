from typing import Tuple, Dict

from flask_restful import Resource, reqparse

from flask_rest_api.models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True)
    parser.add_argument('password', type=str, required=True)

    def post(self) -> Tuple[Dict[str, str], int]:
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": f"The username {data['username']} already exists!"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201
