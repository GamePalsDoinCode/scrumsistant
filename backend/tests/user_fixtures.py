import pytest

from ..structs import WebsocketInfo
from .app_fixtures import websocket_server


@pytest.fixture
def user(websocket_server, faker):
    def _user(email=None, password=None):
        if email is None:
            email = faker.email()
        if password is None:
            password = faker.password()
        new_user = WebsocketInfo(pk=WebsocketInfo.get_new_pk(websocket_server.redis), username=email,)
        new_user.set_password(password)
        new_user.save_new_user(websocket_server.redis)
        return new_user

    return _user
