from typing import Any, Dict, NewType, Tuple, Union

from typing_extensions import TypedDict

RedisKey = NewType('RedisKey', str)
RedisKeyAllowedInput = Union[str, int, bytes]

REDIS_SAFE_INPUT = Union[str, int, bool]
REDIS_SAFE_DICT_INPUT = Dict[str, REDIS_SAFE_INPUT]
REDIS_DICT_OUTPUT = Dict[bytes, bytes]
REDIS_SCALAR_OUTPUT = bytes


FLASK_ROUTE_RESPONSE_VAL = Union[str, Dict[Any, Any]]
FLASK_ROUTE_RESPONSE_CODE = int
FLASK_RESPONSE_TYPE = Union[FLASK_ROUTE_RESPONSE_VAL, Tuple[FLASK_ROUTE_RESPONSE_VAL, FLASK_ROUTE_RESPONSE_CODE]]

WEBSOCKET_TEMP_TYPE = Any
REDIS_PUBSUB_TEMP_TYPE = Any
REDIS_PIPELINE_TEMP_TYPE = Any


class RedisClient:
    # pylint: disable=no-self-use,unused-argument
    def get(self, key: RedisKey) -> REDIS_SCALAR_OUTPUT:
        ...

    def set(self, key: RedisKey, val: REDIS_SAFE_INPUT) -> None:
        ...

    def setex(self, key: RedisKey, expire_time: int, val: REDIS_SAFE_INPUT) -> None:
        # expire time is in seconds
        ...

    def delete(self, key: RedisKey) -> None:
        ...

    def hset(self, key: RedisKey, attr_name: str, val: REDIS_SAFE_INPUT) -> None:
        ...

    def hmset(self, key: RedisKey, val: REDIS_SAFE_DICT_INPUT) -> None:
        ...

    def hgetall(self, key: RedisKey) -> REDIS_DICT_OUTPUT:
        ...

    def pubsub(self, ignore_subscribe_messages: bool) -> REDIS_PUBSUB_TEMP_TYPE:
        ...

    def publish(self, channel_name: str, message: str) -> None:
        ...

    def pipeline(self) -> REDIS_PIPELINE_TEMP_TYPE:
        ...

    def smembers(self, key: RedisKey) -> REDIS_DICT_OUTPUT:
        ...

    def sadd(self, key: RedisKey, val: REDIS_SAFE_INPUT) -> None:
        ...

    def srem(self, key: RedisKey, val: REDIS_SAFE_INPUT) -> None:
        ...

    def incr(self, key: RedisKey) -> REDIS_SCALAR_OUTPUT:
        ...


AuthInfoPacket = TypedDict('AuthInfoPacket', {'signedToken': bytes, 'verifyKey': str})
