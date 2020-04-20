import json

from flask import Flask, request
from flask_cors import CORS
from flask_redis import FlaskRedis

from dataclasses_serialization.json import JSONSerializer

from .structs import WebsocketInfo


try:
    from .local_settings import SERVER_NAME, REDIS_URL, REDIS_PASSWORD, REDIS_PORT
except:
    SERVER_NAME = 'me'
    REDIS_URL = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 0

REDIS_URL = f'redis://:{REDIS_PASSWORD}@{REDIS_URL}:{REDIS_PORT}/{REDIS_DB}'

app = Flask(__name__)
CORS(app)
redis_client = FlaskRedis(app)
redis_pub_sub = redis_client.pubsub(ignore_subscribe_messages=True,)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/current_users', methods=['GET', 'POST',])
def current_users():
    if request.method == 'GET':
        current_pks = [f'user_{pk}' for pk in redis_client.smembers('currentUserPKs')]
        current_users_serial = redis_client.mget(current_pks)
        print(current_users_serial)
        current_usernames = [
            JSONSerializer.deserialize(WebsocketInfo, user).username
            for user in current_users_serial
            if user is not None
        ]
        return json.dumps(current_usernames)
    elif request.method == 'POST':
        post_data = request.get_json()
        user_pk = post_data['pk']  # TODO: needs auth
        user_name = post_data['username']
        redis_client.hset(f'user_{user_pk}', 'username', user_name)
        user_dict = {k.decode('utf8'): v.decode('utf8') for k, v in redis_client.hgetall(f'user_{user_pk}').items()}
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
