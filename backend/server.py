import asyncio
import websockets
import json
from enum import Enum


class MessageType(Enum):
	USER_JOINED = 'userJoined'


current_users = set()

async def notify_users(payload, users = None):
	if users is None:
		users = current_users

	await asyncio.wait([user.send(payload) for user in users])


async def register(websocket):
	current_users.add(websocket)

async def unregister(websocket):
	current_users.remove(websocket)


async def main(websocket, path):
	print(path)
	await register(websocket)
	try:
		async for message in websocket:
			data = json.loads(message)
			print(data)
			if data['type'] == MessageType.USER_JOINED.value:
				name = data['name']
				print(f'{name} just joined up!')
				payload = {'type': MessageType.USER_JOINED.value, 'name': name}
				await notify_users(json.dumps(payload))
	finally:
		await unregister(websocket)



start_server = websockets.serve(main, 'localhost', 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
