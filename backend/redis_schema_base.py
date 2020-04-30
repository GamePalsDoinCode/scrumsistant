class RedisTableMeta(type):
    def __call__(cls, *args, **kwargs):
        val = args[0] if args else None
        if val and type(val) == bytes:
            val = val.decode('utf8')
        return cls.table_template.format(val)


class RedisTable(metaclass=RedisTableMeta):
    pass
