import asyncio
import websockets
import json

from utils import register, unregister
from structs import MessageType, get_info_dict

WEBSOCKET_INFO_DICT = get_info_dict()
from handler_funcs import (
	handle_get_usernames,
	handle_new_user_joined,
)

class Server:
	def __init__(self, info_dict):
		self.info_dict = info_dict

	async def setup(self, websocket, path):
		if websocket not in self.info_dict:
			await register(websocket)
		try:
			print(self.info_dict)
			async for message in websocket:
				data = json.loads(message)
				print(data)
				if data['type'] == MessageType.USER_JOINED.value:
					await handle_new_user_joined(websocket, data)
				elif data['type'] == 'getUsernames':
					await handle_get_usernames(websocket)
		finally:
			await unregister(websocket)

	def run(self):
		start_server = websockets.serve(self.setup, 'localhost', 8000)
		asyncio.get_event_loop().run_until_complete(start_server)
		asyncio.get_event_loop().run_forever()


s = Server(WEBSOCKET_INFO_DICT)
s.run()
