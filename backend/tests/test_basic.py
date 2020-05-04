import json

import pytest

from .fixtures import send_message

WEBSOCKET_URI = "ws://localhost:8000"


@pytest.mark.asyncio
async def test_socket(send_message):
    message = json.dumps({"type": "userJoined", "name": "piss",})
    resp = await send_message(message)
    assert resp
