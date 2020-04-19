import json

from utils import notify_users
from structs import MessageType, get_info_dict

WEBSOCKET_INFO_DICT = get_info_dict()


async def handle_get_usernames(websocket):
    payload = {
        "type": "getUsernames",
        "usernames": [user.username for user in WEBSOCKET_INFO_DICT.values() if user.username != "Uninitalized"],
    }
    await websocket.send(json.dumps(payload))


async def handle_new_user_joined(websocket, data):
    name = data["name"]
    WEBSOCKET_INFO_DICT[websocket].username = name
    payload = {
        "type": MessageType.USER_JOINED.value,
        "name": name,
    }
    await notify_users(json.dumps(payload))
