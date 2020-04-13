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

async def main(websocket, path):
	if not websocket in WEBSOCKET_INFO_DICT:
		await register(websocket)
	try:
		print(WEBSOCKET_INFO_DICT)
		async for message in websocket:
			data = json.loads(message)
			print(data)
			if data['type'] == MessageType.USER_JOINED.value:
				await handle_new_user_joined(websocket, data)
			elif data['type'] == 'getUsernames':
				await handle_get_usernames(websocket)
	finally:
		await unregister(websocket)


start_server = websockets.serve(main, 'localhost', 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
