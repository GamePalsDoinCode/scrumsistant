import json

from flask import Blueprint, current_app, request
from flask_login import current_user

from .query_tools import get_user_by_pk
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE

bp = Blueprint('users_api', __name__)


@bp.route('/users/<user_pk>', methods=['GET', 'POST',])
def users(user_pk) -> FLASK_RESPONSE_TYPE:
    if request.method == 'GET':
        user_pk = request.view_args['user_pk']
        user = get_user_by_pk(user_pk, current_app.db)
        return user.serialize(serialize_method=dict)
    elif request.method == 'POST':
        user = current_user
        post_data = request.get_json()
        display_name = post_data['display_name']
        user.display_name = display_name
        user.save(current_app.db)

        message_for_browser = {'channel': 'currentTeam', 'message': {'userUpdated': (user.display_name, user.id)}}
        ipc_message = {
            'messageType': 'userUpdated',
            'pk': user.id,
            'broadcastTo': 'all',
            'message': json.dumps(message_for_browser),
        }
        current_app.redis_client.publish('flask-IPC', json.dumps(ipc_message))
        return user.serialize(serialize_method=dict)
    else:
        return '', HTTP_STATUS_CODE.HTTP_404_NOT_FOUND.value
