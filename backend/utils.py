import asyncio
import json


async def notify_users(payload, users=None):
    if users is None:
        users = WEBSOCKET_INFO_DICT.keys()
    await asyncio.wait([user.send(payload) for user in users])
