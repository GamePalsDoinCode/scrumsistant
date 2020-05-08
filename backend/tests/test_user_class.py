import json

import pytest
from hypothesis import assume, given, settings
from hypothesis.strategies import emails, integers, none, one_of, text

from ..exceptions import UserNameTakenError
from ..structs import UserInfo
from .app_fixtures import *
from .user_fixtures import *


@given(pk=integers(), display_name=text(min_size=1), email=emails(), password=one_of(text(min_size=1), none()))
@settings(max_examples=10)  # something about this takes forever!
def test_serialize_deserialize_roundtrip_through_redis(redis, pk, display_name, email, password):
    user = UserInfo(pk=pk, display_name=display_name, email=email)
    user.set_password(password)
    with hypothesis_safe_redis(redis) as redis:
        redis.hmset('key', user.serialize())
        round_tripped_user = UserInfo.deserialize(redis.hgetall('key'))
        assert user == round_tripped_user


@given(pk=integers(), display_name=text(min_size=1), email=emails(), password=one_of(text(min_size=1), none()))
@settings(max_examples=10)  # something about this takes forever!
def test_deserialize_not_from_redis(pk, display_name, email, password):
    u = UserInfo(pk=pk, display_name=display_name, email=email)
    u.set_password(password)
    ser = u.serialize(serialize_method=json.dumps)
    u2 = UserInfo.deserialize(json.loads(ser), from_redis=False)
    assert u == u2


@given(email=emails())
def test_is_anonymous(email):
    u = UserInfo(pk=1, email=email)
    assert u.is_anonymous() == (email == '')


@given(one_of(none(), text(min_size=1)), text())
@settings(max_examples=10)  # password hashing is expensive
def test_password_checking_works(password, wrong_password):
    assume(password != wrong_password)
    u = UserInfo(pk=1)

    u.set_password(password)
    assert not u.check_password(wrong_password)
    if password is None:
        assert not u.check_password(password)
    else:
        assert u.check_password(password)


def test_update_user_happy_path(user, redis):
    u = user()
    u.email = 'newemail@newtown.com'
    u.update_user(redis)
    assert u.email == 'newemail@newtown.com'


def test_update_user_fails_if_overwriting(user, redis):
    u1 = user()
    u2 = user()
    u2.pk = u1.pk
    with pytest.raises(UserNameTakenError):
        u2.update_user(redis)
