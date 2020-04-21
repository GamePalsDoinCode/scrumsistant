import json

from flask import Flask, request
from flask_cors import CORS
from flask_redis import FlaskRedis

from dataclasses_serialization.json import JSONSerializer

from .structs import WebsocketInfo
from .utils import cleanup_redis_dict


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


@app.route('/current_users', methods=['GET', 'POST',])
def current_users():
    print(f'current_users {request.method}')
    if request.method == 'GET':
        current_pks = [f'user_{int(pk)}' for pk in redis_client.smembers('currentUserPKs')]
        pipe = redis_client.pipeline()
        for pk in current_pks:
            pipe.hgetall(pk)
        current_user_dicts = [cleanup_redis_dict(user) for user in pipe.execute() if user]
        current_usernames = [user['username'] for user in current_user_dicts]
        print(current_usernames)
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
