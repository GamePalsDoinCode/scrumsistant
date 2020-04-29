import json

from .structs import MessageType
from .utils import notify_users


async def handle_get_usernames(websocket):
    # TODO move to flask
    await websocket.send(json.dumps({'type': 'getUsernames', 'usernames': ['SUPER PUNK']}))
    # payload = {
    #   'type': 'getUsernames',
    #   'usernames': [
    #       user.username for user in WEBSOCKET_INFO_DICT.values()
    #       if user.username != 'Uninitalized'
    #   ],
    # }
    # await websocket.send(json.dumps(payload))


async def handle_new_user_joined(websocket, data):
    # TODO move to flask
    return
    # name = data['name']
    # WEBSOCKET_INFO_DICT[websocket].username = name
    # payload = {
    #   'type': MessageType.USER_JOINED.value,
    #   'name': name,
    # }
    # await notify_users(json.dumps(payload))
