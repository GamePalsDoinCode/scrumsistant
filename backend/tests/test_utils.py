import pytest
from hypothesis import given
from hypothesis.strategies import dictionaries, text

from ..exceptions import RedisKeyNotFoundError
from ..flask_utils import _load_user, load_user
from ..redis_schema import Users
from ..utils import cleanup_redis_dict, transform_to_redis_safe_dict
from .app_fixtures import *
from .user_fixtures import *


@given(dictionaries(text(min_size=1), text(min_size=1), min_size=1))
@pytest.mark.filterwarnings(
    'ignore:.*'
)  # this test warns that the fixture is not reset each test run and recommends using a context manager, which we do. so i want to disable just that warning, but the regex filtering any more specific than that isnt working TODO
def test_redis_round_trip(redis, test_dict):
    # procedure -
    # - generate random dict
    # - pass through transform_to_redis_safe_dict
    # - pass through cleanup_redis_dict
    # - check they are the same

    # limitations
    # right now cleanup_redis_dict is really only meant for user encoding, so it assumes all values are strings
    # so this is not a full test of the transform function

    redis_safe_dict = transform_to_redis_safe_dict(test_dict)
    with hypothesis_safe_redis(redis) as redis:
        redis.hmset('key', redis_safe_dict)
        redised_dict = redis.hgetall('key')
        normal_dict = cleanup_redis_dict(redised_dict)
        assert normal_dict == test_dict


def test__load_user_loads_correct_user(redis, user):
    # objects compare on identity so would fail
    # so we will compare serialized versions
    new_user = user()
    loaded_user = _load_user(Users(new_user.pk), redis)
    assert new_user.serialize() == loaded_user.serialize()


def test__load_user_throws_exception_when_user_not_found(redis):
    with pytest.raises(RedisKeyNotFoundError):
        _load_user(Users(1), redis)


def test_load_user_returns_none_when_user_not_found(flask_app):
    assert load_user(1) == None
