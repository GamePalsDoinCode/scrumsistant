from typing import Any, List, Optional, Union


class RedisTableMeta(type):
    def __call__(cls: Any, *args: Optional[List[Union[str, bytes]]], **kwargs) -> str:
        # Actually the type of cls is RedisTable but mypy doesn't really grasp what I'm doing
        # It also doesn't understand the return type
        # https://github.com/python/mypy/issues/8595
        val = args[0] if args else None
        if val and isinstance(val, bytes):
            val = val.decode('utf8')
        return cls.table_template.format(val)


class RedisTable(metaclass=RedisTableMeta):
    pass
