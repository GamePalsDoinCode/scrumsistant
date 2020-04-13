import asyncio
import json

import pytest
import pytest_asyncio
import websockets

from server import Server

WEBSOCKET_URI = "ws://localhost:8000"

@pytest.fixture
def async_get_server(event_loop):
	server = Server({})
	task = server.get_server_task(server.router)
	return event_loop.run_until_complete(task)

async def send_message(message):
	async with websockets.connect(WEBSOCKET_URI) as websocket:
		await websocket.send(message)
		greeting = await websocket.recv()
		return greeting


@pytest.mark.asyncio
async def test_socket(async_get_server):
	message = json.dumps({
		"type": "userJoined",
		"name": "piss",
	})
	resp = await send_message(message)
	assert resp


