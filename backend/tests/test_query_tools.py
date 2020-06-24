import pytest

from ..exceptions import UserNotFound
from ..query_tools import get_user_by_email, get_user_by_pk
from .app_fixtures import *
from .user_fixtures import *


def test_get_user_by_email_happy_path(user, db_engine):
    u = user()
    queried_user = get_user_by_email(u.email, db_engine)
    assert u == queried_user


def test_get_user_by_pk_happy_path(user, db_engine):
    u = user()
    queried_user = get_user_by_pk(u.id, db_engine)
    assert u == queried_user


def test_get_user_by_email_throws_exception_when_not_found(user, db_engine):
    u = user()
    with pytest.raises(UserNotFound):
        get_user_by_email(u.email + 'randomsuffix', db_engine)
