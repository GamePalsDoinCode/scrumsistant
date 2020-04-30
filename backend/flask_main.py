import json
from datetime import timedelta
from typing import Optional

from flask import Flask, abort, request, session
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, logout_user
from flask_redis import FlaskRedis

from .exceptions import RedisKeyNotFoundError
from .local_settings import FLASK_SECRET_KEY, REDIS_DB, REDIS_PASSWORD, REDIS_PORT, REDIS_URL
from .query_tools import get_user_by_email
from .redis_schema import *
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE, AnonymousUserWrapper, WebsocketInfo
from .utils import cleanup_redis_dict

REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/{REDIS_DB}'

app = Flask(__name__)
app.secret_key = FLASK_SECRET_KEY
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # login session lifetime.  can be any timedelta obj
CORS(app)
redis_client = FlaskRedis(app)
redis_pub_sub = redis_client.pubsub(ignore_subscribe_messages=True,)
login_service = LoginManager(app)
login_service.anonymous_user = AnonymousUserWrapper
# login_service.login_view = 'login'


@app.before_request
def login_required_by_default() -> None:
    login_valid = current_user.is_authenticated(session)
    if login_valid or getattr(app.view_functions[request.endpoint], 'is_public', False):
        return
    abort(401)


def public_endpoint(function):
    function.is_public = True
    return function


@login_service.user_loader
def load_user(table_key: str) -> Optional[WebsocketInfo]:
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


@app.route('/current_users', methods=['GET', 'POST',])
def current_users() -> FLASK_RESPONSE_TYPE:
    if request.method == 'GET':
        current_pks = [Users(pk) for pk in redis_client.smembers(CurrentUsers())]
        pipe = redis_client.pipeline()
        for table_key in current_pks:
            pipe.hgetall(table_key)
        current_user_dicts = [cleanup_redis_dict(user) for user in pipe.execute() if user]
        current_usernames = [user['username'] for user in current_user_dicts]
        return json.dumps(current_usernames)
    elif request.method == 'POST':
        user = current_user
        user_pk = user.pk
        post_data = request.get_json()
        user_name = post_data['username']
        # TODO - run this through the user.save method n stuff
        redis_client.hset(Users(user_pk), 'username', user_name)
        user_dict = {k.decode('utf8'): v.decode('utf8') for k, v in redis_client.hgetall(Users(user_pk)).items()}
        message_for_browser = {
            'type': 'userJoined',
            'name': user_dict['username'],
            'pk': int(user_dict['pk']),
        }
        ipc_message = {
            'messageType': 'userUpdated',
            'pk': int(user_dict['pk']),
            'broadcastTo': 'all',
            'message': json.dumps(message_for_browser),
        }
        redis_client.publish('flask-IPC', json.dumps(ipc_message))
        return user_dict
    else:
        return '', HTTP_STATUS_CODE.HTTP_404_NOT_FOUND.value
