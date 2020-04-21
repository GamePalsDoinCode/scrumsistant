import asyncio
import json


async def notify_users(payload, users=None):
    if users is None:
        users = WEBSOCKET_INFO_DICT.keys()
    await asyncio.wait([user.send(payload) for user in users])


def cleanup_redis_dict(dict_from_redis):
    return {k.decode('utf8'): v.decode('utf8') for k, v in dict_from_redis.items()}
