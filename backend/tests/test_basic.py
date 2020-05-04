import asyncio
import json

import pytest
import pytest_asyncio
import websockets

# from .fixtures import client, send_message, server

WEBSOCKET_URI = "ws://localhost:8000"

# @pytest.mark.asyncio
# async def test_socket(send_message):
# 	message = json.dumps({
# 		"type": "userJoined",
# 		"name": "piss",
# 	})
# 	resp = await send_message(message)
# 	assert resp


def test_truth():
    assert True
