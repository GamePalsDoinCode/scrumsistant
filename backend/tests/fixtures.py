import pytest
from ..server import Server


@pytest.fixture
def server(event_loop):
	server = Server({})
	task = server.get_server_task(server.router)
	event_loop.run_until_complete(task)
