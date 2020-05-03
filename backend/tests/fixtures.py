import pytest
import websockets

from ..server import Server

WEBSOCKET_URI = "ws://localhost:8000"


@pytest.fixture
def server(event_loop):
    server_ = Server()
    task = server_.get_server_task(server_.router)
    event_loop.run_until_complete(task)


@pytest.fixture
async def client():
    async with websockets.connect(WEBSOCKET_URI) as websocket:
        yield websocket


@pytest.fixture
async def send_message(server, client):
    async def _send_message(message):
        await client.send(message)
        greeting = await client.recv()
        return greeting

    return _send_message
