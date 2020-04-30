from .exceptions import *
from .redis_schema import *
from .scrum_types import REDIS_CLIENT_TEMP_TYPE
from .structs import WebsocketInfo


def get_user_by_email(email: str, redis_client: REDIS_CLIENT_TEMP_TYPE) -> WebsocketInfo:
    user_pk = redis_client.get(PKByEmail(email))
    if not user_pk:
        raise RedisKeyNotFoundError('No user with that email')
    user_dict = redis_client.hgetall(Users(user_pk))

    if not user_dict:
        raise RedisKeyNotFoundError('User info not found')
    new_user_obj = WebsocketInfo.deserialize(user_dict)
    return new_user_obj
