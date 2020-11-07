from typing import Dict, Optional

from werkzeug.security import safe_str_cmp

from user import User

users = [
    User(1, 'teppei', 'password')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username: str, password: str) -> Dict[str, str]:
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload) -> Optional[int]:
    userid = payload['identity']
    return userid_mapping.get(userid, None)
