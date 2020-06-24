from sqlalchemy.sql import select

from .db_schema import Users
from .exceptions import UserNotFound
from .scrum_types import DB_CONN
from .structs import UserInfo


def _one_result_or_exception(db_result, exc):
    if not db_result:
        raise exc
    return db_result


def get_user_by_email(email: str, db: DB_CONN) -> UserInfo:
    query = select([Users]).where(Users.c.email == email)
    result = _one_result_or_exception(db.execute(query).fetchone(), UserNotFound('No user with that email'),)
    return UserInfo.deserialize(result)


def get_user_by_pk(pk: str, db: DB_CONN) -> UserInfo:
    query = select([Users]).where(Users.c.id == pk)
    result = _one_result_or_exception(db.execute(query).fetchone(), UserNotFound('No user with that id'),)
    return UserInfo.deserialize(result)
