from .redis_schema_base import RedisTable


class OwnsConnection(RedisTable):
    table_template = 'owns-connection:{}'


class PKByEmail(RedisTable):
    table_template = 'email:{}'


class Users(RedisTable):
    table_template = 'user:{}'


class CurrentUsers(RedisTable):
    table_template = 'currentUserPKs'
