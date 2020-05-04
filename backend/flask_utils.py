from typing import Optional

from flask import abort, current_app, request, session
from flask_login import current_user

from .scrum_types import RedisKey
from .structs import WebsocketInfo


# @app.before_request
def login_required_by_default() -> None:
    login_valid = current_user.is_authenticated(session)
    if login_valid or getattr(current_app.view_functions[request.endpoint], 'is_public', False):
        return
    abort(401)


def load_user(table_key: RedisKey) -> Optional[WebsocketInfo]:
    user_dict = current_app.redis_client.hgetall(table_key)
    if user_dict:
        user = WebsocketInfo.deserialize(user_dict)
        return user
    return None
