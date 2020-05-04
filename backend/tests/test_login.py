import pytest

from .app_fixtures import *  # star import because pytest is moronic and if you use a fixture that itself uses a 2nd fixture, you have to import the 2nd fixture here too.  So fuck it just give me all of em
from .user_fixtures import *


def test_login_fail_with_no_user_in_db(flask_client, websocket_server):
    post_data = {'email': 'Anything', 'password': 'Anything'}
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 401


def test_login_fail_with_wrong_password(flask_client, user):
    new_user = user()
    post_data = {
        'email': new_user.username,
        'password': new_user.password,  # the password here is the already hashed password, so that is all but guaranteed to fail (I guess nothing prevents the hash not changing it but probs)
    }
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 401


def test_login_success_with_right_password(flask_client, user):
    password = 'correct-horse-battery-staple'
    new_user = user(password=password)

    post_data = {
        'email': new_user.username,
        'password': password,
    }
    rv = flask_client.post('login', json=post_data)
    assert rv.status_code == 200
