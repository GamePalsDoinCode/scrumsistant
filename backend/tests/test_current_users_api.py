import pytest
from hypothesis import given

from ..redis_schema import CurrentUsers
from ..structs import HTTP_STATUS_CODE
from .app_fixtures import *
from .user_fixtures import *


def test_current_users_returns_all_logged_in_users(flask_client, logged_in_user, user, redis):

    # these will be logged in
    # only one can use the logged in user fixture, because the last one logged in would be the only one logged in
    # because the flask client is not multiple clients
    u1 = logged_in_user(add_to_redis=True)
    u2 = user()
    u3 = user()
    # so we use the regular user fixture and manually fill out the redis fields
    # we rely on other tests to guarantee that the redis current users table is filled out properly on login
    redis.sadd(CurrentUsers(), u2.id)
    redis.sadd(CurrentUsers(), u3.id)

    # this guy will be left not logged in, as a control
    u4 = user()

    rv = flask_client.get('current_users')
    user_tuples = rv.json

    user_pks = {tup[1] for tup in user_tuples}
    assert user_pks == {u1.id, u2.id, u3.id}
    assert u4.id not in user_pks  # kind of meaningless after previous line, but makes pylint feel better
