import random

import pytest

from ..structs import UserInfo
from .app_fixtures import websocket_server


@pytest.fixture
def user(websocket_server, faker):
    def _user(email=None, password=None, display_name=None, is_PM=None):
        if email is None:
            email = faker.email()
        if password is None:
            password = faker.password()
        if display_name is None:
            display_name = faker.name()
        if is_PM is None:
            is_PM = random.random() > 0.5
        new_user = UserInfo(
            pk=UserInfo.get_new_pk(websocket_server.redis), email=email, display_name=display_name, is_PM=is_PM
        )
        new_user.set_password(password)
        new_user.save_new_user(websocket_server.redis)
        return new_user

    return _user


@pytest.fixture
def logged_in_user(user, flask_client):
    def _logged_in_user(email=None, password=None, display_name=None):
        if not password:
            password = 'elephants-are-always-purple!##'
        new_user = user(email=email, password=password, display_name=display_name)
        post_data = {
            'email': new_user.email,
            'password': password,
        }
        flask_client.post('login', json=post_data)
        return new_user

    return _logged_in_user
