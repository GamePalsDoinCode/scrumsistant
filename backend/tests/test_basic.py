import asyncio
import json

import pytest
import pytest_asyncio
import websockets

from .fixtures import server

WEBSOCKET_URI = "ws://localhost:8000"


async def send_message(message):
    async with websockets.connect(WEBSOCKET_URI) as websocket:
        await websocket.send(message)
        greeting = await websocket.recv()
        return greeting


@pytest.mark.asyncio
async def test_socket(server):
    message = json.dumps({"type": "userJoined", "name": "piss",})
    resp = await send_message(message)
    assert resp
