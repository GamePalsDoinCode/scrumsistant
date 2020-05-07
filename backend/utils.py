from typing import Any, Dict

from .scrum_types import REDIS_SAFE_DICT_INPUT


def cleanup_redis_dict(dict_from_redis: Dict[bytes, bytes]) -> Dict[str, str]:
    return {k.decode('utf8'): v.decode('utf8') for k, v in dict_from_redis.items()}


def transform_to_redis_safe_dict(dict_with_nones: Dict[Any, Any]) -> REDIS_SAFE_DICT_INPUT:
    # this will turn any toplevel None values -> 'null'
    return {k: 'null' if v is None else v for k, v in dict_with_nones.items()}
