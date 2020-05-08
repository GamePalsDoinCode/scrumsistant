from contextlib import contextmanager

import fakeredis
import pytest
import websockets

from ..flask_main import create_app as create_flask_server
from ..server import Server

WEBSOCKET_URI = "ws://localhost:8000"


@contextmanager
def hypothesis_safe_redis(redis):
    yield redis
    redis.flushall()


@pytest.fixture
def redis(event_loop):
    yield fakeredis.FakeRedis()


@pytest.fixture
def flask_client(event_loop, redis):
    test_config = {'TESTING': True, 'redis': redis}
    app = create_flask_server(test_config=test_config)
    with app.test_client() as flask_client_obj:
        yield flask_client_obj


@pytest.fixture
def flask_app(event_loop, redis):
    test_config = {'TESTING': True, 'redis': redis}
    app = create_flask_server(test_config=test_config)
    with app.app_context() as app_:
        yield


@pytest.fixture
async def websocket_server(event_loop, redis):
    server_ = Server(redis_client=redis)
    task = server_.get_server_task(server_.router)
    server = await task
    yield server_
    try:
        # sometimes this throws an exception, trying to close the thread twice
        # not 100000000% sure wtf that's about, but this seems ok
        server_._redis_pubsub_thread.stop()
    except ValueError:
        # the exception is
        # ValueError: Invalid file descriptor: -1
        pass
    server.close()
    await server.wait_closed()


@pytest.fixture
async def websocket_client(event_loop):
    async with websockets.connect(WEBSOCKET_URI) as websocket:
        yield websocket


@pytest.fixture
async def send_message(websocket_server, websocket_client, event_loop):
    async def _send_message(message):
        await websocket_client.send(message)
        greeting = await websocket_client.recv()
        return greeting

    return _send_message
