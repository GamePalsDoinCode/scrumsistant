import json
from typing import Optional

from flask import abort, current_app, request, session
from flask_login import current_user, login_user, logout_user

from .exceptions import RedisKeyNotFoundError
from .flask_main import app, public_endpoint
from .query_tools import get_user_by_email
from .redis_schema import CurrentUsers, Users
from .scrum_types import FLASK_RESPONSE_TYPE, RedisKey
from .structs import HTTP_STATUS_CODE, WebsocketInfo
from .utils import cleanup_redis_dict

redis_client = app.redis_client
login_service = app.login_service


@app.before_request
def login_required_by_default() -> None:
    login_valid = current_user.is_authenticated(session)
    if login_valid or getattr(current_app.view_functions[request.endpoint], 'is_public', False):
        return
    abort(401)


@login_service.user_loader
def load_user(table_key: RedisKey) -> Optional[WebsocketInfo]:
    user_dict = redis_client.hgetall(table_key)
    if user_dict:
        user = WebsocketInfo.deserialize(user_dict)
        return user
    return None


@app.route('/login', methods=['POST'])
@public_endpoint
def login() -> FLASK_RESPONSE_TYPE:
    post_data = request.get_json()
    user_email = post_data['email']
    incoming_password = post_data['password']

    not_allowed_return_val = {'auth': 'not ok'}, HTTP_STATUS_CODE.HTTP_401_UNAUTHORIZED.value

    try:
        user = get_user_by_email(user_email, redis_client)
    except RedisKeyNotFoundError:
        return not_allowed_return_val

    password_ok = user.check_password(incoming_password)
    if password_ok:
        login_user(user)
        session.permanent = True
        return {'auth': 'ok'}
    return not_allowed_return_val


@app.route('/logout')
@public_endpoint
def logout() -> FLASK_RESPONSE_TYPE:
    logout_user()
    return ''


@app.route('/is_authenticated')
@public_endpoint
def is_authenticated() -> FLASK_RESPONSE_TYPE:
    if current_user.is_authenticated(session):
        return '', HTTP_STATUS_CODE.HTTP_200_OK.value
    return '', HTTP_STATUS_CODE.HTTP_401_UNAUTHORIZED.value
