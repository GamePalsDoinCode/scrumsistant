from typing import Optional

from flask import abort, current_app, request, session
from flask_login import current_user

from .exceptions import RedisKeyNotFoundError
from .scrum_types import RedisClient, RedisKey
from .structs import UserInfo


def login_required_by_default() -> None:
    login_valid = current_user.is_authenticated(session)
    if login_valid or getattr(current_app.view_functions[request.endpoint], 'is_public', False):
        return
    abort(401)


def _load_user(table_key: RedisKey, redis_client: RedisClient):
    user_dict = redis_client.hgetall(table_key)
    if user_dict:
        user = UserInfo.deserialize(user_dict)
        return user
    raise RedisKeyNotFoundError


def load_user(table_key: RedisKey) -> Optional[UserInfo]:
    try:
        return _load_user(table_key, current_app.redis_client)
    except RedisKeyNotFoundError:
        return None
