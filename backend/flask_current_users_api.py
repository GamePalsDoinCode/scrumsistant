import json

from flask import request
from flask_login import current_user

from .flask_main import app, redis_client
from .redis_schema import CurrentUsers, Users
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE
from .utils import cleanup_redis_dict


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
