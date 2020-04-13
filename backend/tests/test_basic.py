import pytest
import asyncio
import pytest_asyncio
import websockets
import server
import multiprocessing

WEBSOCKET_URI = "ws://localhost:8000"


def test_truth():
	assert True


@pytest.fixture(autouse=True)
def setup_server():
	s = server.Server()
	p = multiprocessing.Process(s.run())
	p.start()
	# t = threading.Thread(s.run())
	# t.start
	# yield
	# p.terminate()


@pytest.mark.asyncio
async def test_socket():
	message = "{\"type\": \"userJoined\", \"name\":\"piss\"}"

	resp = await send_message(message)
	assert resp
	# loop = asyncio.get_event_loop()
	# loop.run_until_complete(send_message(message))


async def send_message(message):
	async with websockets.connect(WEBSOCKET_URI) as websocket:
		await websocket.send(message)
		greeting = await websocket.recv()
		return greeting
