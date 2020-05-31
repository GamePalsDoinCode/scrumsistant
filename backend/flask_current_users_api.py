import json

from flask import Blueprint, current_app, request
from flask_login import current_user
from sqlalchemy.sql import select

from .db_schema import Users
from .redis_schema import CurrentUsers
from .scrum_types import FLASK_RESPONSE_TYPE
from .structs import HTTP_STATUS_CODE

bp = Blueprint('current_users_api', __name__)


@bp.route('/current_users', methods=['GET', 'POST',])
def current_users() -> FLASK_RESPONSE_TYPE:
    if request.method == 'GET':
        current_pks = {int(pk) for pk in current_app.redis_client.smembers(CurrentUsers())} | {current_user.id}
        query = select([Users.c.display_name, Users.c.id]).where(Users.c.id.in_(current_pks))
        sorted_current_user_tuples = [
            tuple(row_proxy) for row_proxy in sorted(current_app.db.execute(query).fetchall(), key=lambda tup: tup[1])
        ]
        return json.dumps(sorted_current_user_tuples)
    elif request.method == 'POST':
        user = current_user
        post_data = request.get_json()
        display_name = post_data['displayName']
        user.display_name = display_name
        user = user.save(current_app.db)

        message_for_browser = {
            'type': 'userJoined',
            'displayName': user.display_name,
            'pk': user.id,
        }
        ipc_message = {
            'messageType': 'userUpdated',
            'pk': user.id,
            'broadcastTo': 'all',
            'message': json.dumps(message_for_browser),
        }
        current_app.redis_client.publish('flask-IPC', json.dumps(ipc_message))
        return user.serialize(serialize_method=json.dumps)
    else:
        return '', HTTP_STATUS_CODE.HTTP_404_NOT_FOUND.value
