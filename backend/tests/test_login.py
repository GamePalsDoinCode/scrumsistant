import pytest

from .fixtures import flask_client, websocket_server


@pytest.mark.asyncio
def test_login_fail_with_no_user_in_db(flask_client, websocket_server):
    post_data = {'username': 'Anything', 'password': 'Anything'}
    rv = flask_client.post('login', data=post_data)

    assert rv.status_code == 401
