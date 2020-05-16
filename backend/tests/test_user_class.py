import json
import os

import pytest
from hypothesis import assume, given, settings
from hypothesis.strategies import booleans, emails, integers, none, one_of, text

from ..exceptions import UserNameTakenError
from ..structs import UserInfo
from .app_fixtures import *
from .user_fixtures import *


@given(
    pk=integers(),
    display_name=text(min_size=1),
    email=emails(),
    password=one_of(none(), text(min_size=1)),
    is_PM=booleans(),
)
@settings(max_examples=10)  # something about this takes forever!
@pytest.mark.filterwarnings(
    'ignore:.*'
)  # this test warns that the fixture is not reset each test run and recommends using a context manager, which we do. so i want to disable just that warning, but the regex filtering any more specific than that isnt working TODO
def test_serialize_deserialize_roundtrip_through_redis(redis, pk, display_name, email, password, is_PM):
    user = UserInfo(pk=pk, display_name=display_name, email=email, is_PM=is_PM)
    if password:
        user.set_password(password)
    with hypothesis_safe_redis(redis) as redis:
        redis.hmset('key', user.serialize())
        round_tripped_user = UserInfo.deserialize(redis.hgetall('key'))
        assert user == round_tripped_user


def test_serialize_skip_list_works_with_valid_key(user):
    u = user()
    serialized_user = u.serialize(serialize_method=dict)
    serialized_user_skip = u.serialize(skip_list=['pk'], serialize_method=dict)
    assert 'pk' in serialized_user and 'pk' not in serialized_user_skip


def test_serialize_skip_list_ignores_invalid_key(user):
    u = user()
    serialized_user = u.serialize(serialize_method=dict)
    serialized_user_bad_key = u.serialize(serialize_method=dict, skip_list=['blarg'])
    assert serialized_user == serialized_user_bad_key


def test__check_not_overwriting_happy_path(user, redis):
    u = user()
    u.display_name = 'another name!'
    u.update_user(redis)
    assert True  # above will throw an exception if the test fails


@given(pk=integers(), display_name=text(min_size=1), email=emails(), password=text(min_size=1))
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


@given(one_of(none(), text(min_size=1)), text(min_size=1))
def test_password_checking_works(password, wrong_password):
    assume(password != wrong_password)
    u = UserInfo(pk=1)
    if password:
        u.set_password(password)
    assert not u.check_password(wrong_password)
    if password:
        assert u.check_password(password)
    else:
        assert not u.check_password(password)


if os.environ.get('TRAVIS'):
    # test password hashing times out in CI, little too long
    # so just cut it short for now
    # TODO investigate using a CI profile instead of this manual call
    reduced_max = settings(
        max_examples=1, deadline=500
    )  # deadline is in milliseconds.  In CI it takes about 325 ms, the default deadline is 200
else:
    reduced_max = settings(max_examples=10)
test_password_checking_works = reduced_max(test_password_checking_works)


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
