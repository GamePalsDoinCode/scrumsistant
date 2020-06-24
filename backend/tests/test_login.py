import pytest

from ..redis_schema import CurrentUsers
from .app_fixtures import *  # star import because pytest is moronic and if you use a fixture that itself uses a 2nd fixture, you have to import the 2nd fixture here too.  So fuck it just give me all of em
from .user_fixtures import *


def test_login_fail_with_no_user_in_db(flask_client, websocket_server):
    post_data = {'email': 'Anything', 'password': 'Anything'}
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 401


def test_login_fail_with_wrong_password(flask_client, user):
    new_user = user()
    post_data = {
        'email': new_user.email,
        'password': new_user.password,  # the password here is the already hashed password, so that is all but guaranteed to fail (I guess nothing prevents the hash not changing it but probs)
    }
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 401


def test_login_success_with_right_password(flask_client, user):
    password = 'correct-horse-battery-staple'
    new_user = user(password=password)

    post_data = {
        'email': new_user.email,
        'password': password,
    }
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 200


def test_logout_with_noone_logged_in_is_fine(flask_client):
    rv = flask_client.get('logout')
    assert rv.status_code == 200


def test_is_authenticated_fails_when_not_logged_in(flask_client):
    rv = flask_client.get('is_authenticated')
    assert rv.status_code == 401


def test_is_authenticated_succeeds_when_logged_in(logged_in_user, flask_client):
    logged_in_user()
    rv = flask_client.get('is_authenticated')
    assert rv.status_code == 200


def test_is_authenticated_fails_after_logging_out(logged_in_user, flask_client):
    logged_in_user()
    flask_client.get('logout')
    rv = flask_client.get('is_authenticated')
    assert rv.status_code == 401


def test_login_required_by_default_decorator_works(logged_in_user, flask_client):
    # first, hit any endpoint while not logged in, get a 401
    rv = flask_client.get('current_users')
    assert rv.status_code == 401
    # now, log in, hit same endpoint.  Don't care about the response, just that its not a 401
    logged_in_user()
    rv = flask_client.get('current_users')
    assert rv.status_code != 401


def test_redis_current_users_is_filled_out_when_logging_in(logged_in_user, user, redis):
    logged_in = logged_in_user(add_to_redis=True)
    not_logged_in = user()

    redis_current_user_ids = {int(pk) for pk in redis.smembers(CurrentUsers())}

    assert logged_in.id in redis_current_user_ids
    assert not_logged_in.id not in redis_current_user_ids
