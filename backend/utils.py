import asyncio
import json

from structs import get_info_dict, WebsocketInfo

WEBSOCKET_INFO_DICT = get_info_dict()


async def register(websocket):
    WEBSOCKET_INFO_DICT[websocket] = WebsocketInfo(
        username='Uninitalized',
    )


async def unregister(websocket):
    dropped_user_info = WEBSOCKET_INFO_DICT.pop(websocket, None)
    if dropped_user_info:
        payload = json.dumps({
            'type': 'userLeft',
            'usernamer': dropped_user_info.username
        })
        await notify_users(payload)


async def notify_users(payload, users=None):
    if users is None:
        users = WEBSOCKET_INFO_DICT.keys()
    await asyncio.wait([
        user.send(payload) for user in users
    ])
