from .app_fixtures import *
from .user_fixtures import *


def test_websocket_auth_generated_when_logged_in(flask_client, logged_in_user):
    logged_in_user()
    rv = flask_client.get('get_websocket_auth_token')
    assert rv.status_code == 200
