from .scrum_types import RedisKey, RedisKeyAllowedInput


def _table_base(table_name: str, template_val: RedisKeyAllowedInput) -> RedisKey:
    if isinstance(template_val, bytes):
        template_val = template_val.decode('utf8')
    return RedisKey(table_name.format(str(template_val)))


def OwnsConnection(template_val: RedisKeyAllowedInput) -> RedisKey:
    return _table_base('owns-connection:{}', template_val)


def CurrentUsers() -> RedisKey:
    return _table_base('currentUserPks', '')


def AuthToken(token: bytes) -> RedisKey:
    return _table_base('AuthToken:{}', token)
