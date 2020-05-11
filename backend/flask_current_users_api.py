import json

from flask import Blueprint, current_app, request
from flask_login import current_user

from .redis_schema import CurrentUsers, Users
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE
from .utils import cleanup_redis_dict

bp = Blueprint('current_users_api', __name__)


@bp.route('/current_users', methods=['GET', 'POST',])
def current_users() -> FLASK_RESPONSE_TYPE:
    if request.method == 'GET':
        current_pks = [Users(pk) for pk in current_app.redis_client.smembers(CurrentUsers())]
        pipe = current_app.redis_client.pipeline()
        for table_key in current_pks:
            pipe.hgetall(table_key)
        current_user_dicts = [cleanup_redis_dict(user) for user in pipe.execute() if user]
        current_usernames = [user['display_name'] for user in current_user_dicts]
        return json.dumps(current_usernames)
    elif request.method == 'POST':
        user = current_user
        post_data = request.get_json()
        display_name = post_data['displayName']
        user.display_name = display_name
        user = user.update_user(current_app.redis_client)

        message_for_browser = {
            'type': 'userJoined',
            'displayName': user.display_name,
            'pk': user.pk,
        }
        ipc_message = {
            'messageType': 'userUpdated',
            'pk': user.pk,
            'broadcastTo': 'all',
            'message': json.dumps(message_for_browser),
        }
        current_app.redis_client.publish('flask-IPC', json.dumps(ipc_message))
        return user.serialize(serialize_method=json.dumps)
    else:
        return '', HTTP_STATUS_CODE.HTTP_404_NOT_FOUND.value
