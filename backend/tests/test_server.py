import json
from unittest import mock

import pytest

from ..redis_schema import CurrentUsers, OwnsConnection
from .app_fixtures import *
from .user_fixtures import *


async def test_register(user, websocket_server, websocket_client):
    u = user()
    await websocket_server.register(websocket_client, u)
    assert websocket_server.websocket_info_dict[websocket_client] == u.pk
    assert websocket_server.redis.get(OwnsConnection(u.pk)).decode('utf8') == websocket_server.SERVER_NAME
    assert websocket_server.redis.sismember(CurrentUsers(), u.pk)


async def test_unregister_of_nonregistered_user(websocket_server, websocket_client):
    orig_keys = websocket_server.redis.keys()
    await websocket_server.unregister(websocket_client)
    cur_keys = websocket_server.redis.keys()
    assert orig_keys == cur_keys


async def test_unregister_of_registered_user(user, websocket_server, websocket_client):
    u = user()
    await websocket_server.register(websocket_client, u)
    await websocket_server.unregister(websocket_client)
    assert not websocket_server.redis.get(OwnsConnection(u.pk))
    assert not websocket_server.redis.sismember(CurrentUsers(), u.pk)


async def test_verify_websocket_auth_happy_path(websocket_server, websocket_client, flask_client, logged_in_user):
    logged_in_user()
    rv = flask_client.get('get_websocket_auth_token')

    message = {'msg': 'authTokenVerification', 'data': rv.json}
    await websocket_client.send(json.dumps(message))
    await websocket_client.recv()
    # on an auth failure, the server will close the connection


async def test_verify_websocket_auth_with_garbage_data_fails(websocket_server, websocket_client):
    message = {
        'msg': 'authTokenVerification',
        'data': {1: 1},
    }
    await websocket_client.send(json.dumps(message))
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        await websocket_client.recv()


async def test_verify_websocket_auth_with_false_data_fails(websocket_server, websocket_client):
    message = {
        'msg': 'authTokenVerification',
        'data': {'signedToken': 'aaaa', 'verifyKey': 'bbb',},
    }
    await websocket_client.send(json.dumps(message))
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        await websocket_client.recv()


async def test_verify_good_auth_but_user_deleted_fails(
    websocket_server, websocket_client, flask_client, logged_in_user
):
    u = logged_in_user()
    auth_info = flask_client.get('get_websocket_auth_token')
    message = {'msg': 'authTokenVerification', 'data': auth_info.json}
    websocket_server.redis.delete(Users(u.pk))
    await websocket_client.send(json.dumps(message))
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        await websocket_client.recv()


async def test_verify_good_auth_but_token_timed_out_fails(
    websocket_server, websocket_client, flask_client, logged_in_user
):
    logged_in_user()
    auth_info = flask_client.get('get_websocket_auth_token')
    message = {'msg': 'authTokenVerification', 'data': auth_info.json}
    for k in websocket_server.redis.keys():
        if k.startswith(b'Auth'):
            websocket_server.redis.delete(k)
    await websocket_client.send(json.dumps(message))
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        await websocket_client.recv()
