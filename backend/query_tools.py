from .exceptions import RedisKeyNotFoundError
from .redis_schema import PKByEmail, Users
from .scrum_types import RedisClient
from .structs import UserInfo


def get_user_by_email(email: str, redis_client: RedisClient) -> UserInfo:
    user_pk = redis_client.get(PKByEmail(email))
    if not user_pk:
        raise RedisKeyNotFoundError('No user with that email')
    user_dict = redis_client.hgetall(Users(user_pk))

    if not user_dict:
        raise RedisKeyNotFoundError('User info not found')
    new_user_obj = UserInfo.deserialize(user_dict)
    return new_user_obj
