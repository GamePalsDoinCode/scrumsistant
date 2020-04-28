from .exceptions import *
from .structs import WebsocketInfo


def get_user_by_email(email, redis_client):
    user_pk = redis_client.get(email)
    if not user_pk:
        raise RedisKeyNotFoundError('No user with that email')
    user_dict = redis_client.hgetall(f'user_{int(user_pk)}')

    if not user_dict:
        raise RedisKeyNotFoundError('User info not found')
    new_user_obj = WebsocketInfo.deserialize(user_dict)
    return new_user_obj
