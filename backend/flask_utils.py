from typing import Optional

from flask import abort, current_app, request, session
from flask_login import current_user
from sqlalchemy.sql import select

from .db_schema import Users
from .exceptions import UserNotFound
from .structs import UserInfo


def login_required_by_default() -> None:
    login_valid = current_user.is_authenticated(session)

    if request.endpoint and (login_valid or getattr(current_app.view_functions[request.endpoint], 'is_public', False)):
        return
    abort(401)


def _load_user(pk_str: str, db) -> UserInfo:

    select_statement = select([Users]).where(Users.c.id == int(pk_str))
    user_dict = db.execute(select_statement).fetchone()
    if user_dict is not None:
        user = UserInfo.deserialize(user_dict)
        return user
    raise UserNotFound


def load_user(pk_str: str) -> Optional[UserInfo]:
    try:
        return _load_user(pk_str, current_app.db)
    except UserNotFound:
        return None
