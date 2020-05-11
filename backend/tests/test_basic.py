import json

import pytest
import websockets

from .app_fixtures import *

WEBSOCKET_URI = "ws://localhost:8000"


@pytest.mark.asyncio
async def test_connection_closed_if_missing_auth(send_message):
    message = json.dumps({"type": "userJoined", "name": "piss",})
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        resp = await send_message(message)
