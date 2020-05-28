from typing import Any, Dict

from .scrum_types import REDIS_SAFE_DICT_INPUT


def cleanup_redis_dict(dict_from_redis: Dict[bytes, bytes]) -> Dict[str, str]:
    return {k.decode('utf8'): v.decode('utf8') for k, v in dict_from_redis.items()}


def transform_to_redis_safe_dict(dict_with_nones_or_bool: Dict[Any, Any]) -> REDIS_SAFE_DICT_INPUT:
    # this will turn any toplevel None values -> 'null', and any bools to the string version of their value
    none_dict = {k: 'null' for k, v in dict_with_nones_or_bool.items() if v is None}
    bool_dict = {k: str(v) for k, v in dict_with_nones_or_bool.items() if isinstance(v, bool)}
    handled_keys = none_dict.keys() | bool_dict.keys()

    the_rest = {k: v for k, v in dict_with_nones_or_bool.items() if not k in handled_keys}
    return {**the_rest, **bool_dict, **none_dict}
