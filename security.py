from typing import Optional, Dict

from werkzeug.security import safe_str_cmp

from user import User


def authenticate(username: str, password: str) -> Optional[User]:
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload: Dict[str, int]) -> Optional[User]:
    userid = payload['identity']
    return User.find_by_id(userid)
