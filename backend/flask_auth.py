import os

import nacl.encoding  # type: ignore
import nacl.signing  # type: ignore
from flask import Blueprint, current_app, request, session
from flask_login import current_user, login_user, logout_user

from .exceptions import RedisKeyNotFoundError
from .flask_main import public_endpoint
from .local_settings import FLASK_SECRET_KEY
from .query_tools import get_user_by_email
from .redis_schema import AuthToken
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['POST'])
@public_endpoint
def login() -> FLASK_RESPONSE_TYPE:
    post_data = request.get_json()
    user_email = post_data['email']
    incoming_password = post_data['password']

    not_allowed_return_val = {'auth': 'not ok'}, HTTP_STATUS_CODE.HTTP_401_UNAUTHORIZED.value

    try:
        user = get_user_by_email(user_email, current_app.redis_client)
    except RedisKeyNotFoundError:
        return not_allowed_return_val

    password_ok = user.check_password(incoming_password)
    if password_ok:
        login_user(user)
        session.permanent = True
        return {'auth': 'ok'}
    return not_allowed_return_val


@bp.route('/logout')
@public_endpoint
def logout() -> FLASK_RESPONSE_TYPE:
    logout_user()
    return ''


@bp.route('/is_authenticated')
@public_endpoint
def is_authenticated() -> FLASK_RESPONSE_TYPE:
    if current_user.is_authenticated(session):
        return '', HTTP_STATUS_CODE.HTTP_200_OK.value
    return '', HTTP_STATUS_CODE.HTTP_401_UNAUTHORIZED.value


@bp.route('/get_websocket_auth_token')
def get_websocket_auth_token() -> FLASK_RESPONSE_TYPE:
    token = os.urandom(24).hex().encode('utf8')
    signing_key = nacl.signing.SigningKey(FLASK_SECRET_KEY[:32])
    signed_message = signing_key.sign(token).hex()
    verify_key = signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf8')
    user_pk = current_user.pk
    current_app.redis_client.setex(AuthToken(token), 10, user_pk)
    return {
        'signedToken': signed_message,
        'verifyKey': verify_key,
    }
