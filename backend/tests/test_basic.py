import json

import pytest

from .app_fixtures import send_message, websocket_client, websocket_server

WEBSOCKET_URI = "ws://localhost:8000"


@pytest.mark.asyncio
async def test_socket(send_message):
    message = json.dumps({"type": "userJoined", "name": "piss",})
    resp = await send_message(message)
    assert resp
