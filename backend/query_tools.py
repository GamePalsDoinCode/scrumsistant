from .scrum_types import REDIS_CLIENT_TEMP_TYPE
from .structs import WebsocketInfo


def get_user_by_email(email: str, redis_client: REDIS_CLIENT_TEMP_TYPE) -> WebsocketInfo:
    user_pk = redis_client.get(email)
    if not user_pk:
        raise TypeError  # TODO implement custom error type
    user_dict = redis_client.hgetall(f'user_{int(user_pk)}')

    if not user_dict:
        raise TypeError  # TODO implement custom error type
    new_user_obj = WebsocketInfo.deserialize(user_dict)
    return new_user_obj
