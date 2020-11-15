from typing import Optional, Dict

from werkzeug.security import safe_str_cmp

from flask_rest_api.models.user import UserModel


def authenticate(username: str, password: str) -> Optional[UserModel]:
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload: Dict[str, int]) -> Optional[UserModel]:
    userid = payload['identity']
    return UserModel.find_by_id(userid)
