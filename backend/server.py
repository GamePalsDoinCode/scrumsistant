import asyncio
import json
import functools

import websockets
import redis

from .handler_funcs import (
    handle_get_usernames,
    handle_new_user_joined,
)

from .structs import MessageType, WebsocketInfo

try:
    from .local_settings import SERVER_NAME, REDIS_URL, REDIS_PASSWORD, REDIS_PORT
except:
    SERVER_NAME = 'me'
    REDIS_URL = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 0


class Server:
    def __init__(self):
        self.SERVER_NAME = SERVER_NAME
        self.websocket_info_dict = {}
        self.redis = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,)
        redis_pubsub_instance = self.redis.pubsub(ignore_subscribe_messages=True,)

        websocket_handler = functools.partial(self.websocket_ipc_handler, self)
        flask_handler = functools.partial(self.flask_ipc_handler, self)
        redis_pubsub_instance.subscribe(
            **{'websocket-IPC': websocket_handler, 'flask-IPC': flask_handler,}
        )
        self._redis_pubsub_thread = redis_pubsub_instance.run_in_thread(sleep_time=0.5,)

    def register(self, websocket):
        next_pk = self.redis.incr('WEBSOCKET_PK')
        self.websocket_info_dict[websocket] = WebsocketInfo(pk=next_pk, username='Uninitalized',)
        self.redis.set(
            f'owns-connection-{next_pk}', self.SERVER_NAME,
        )

    async def unregister(self, websocket):
        dropped_user_info = self.websocket_info_dict.pop(websocket, None,)
        if dropped_user_info:
            self.redis.delete(f'owns-connection-{dropped_user_info.pk}')
            message = {
                'type': 'userLeft',
                'pk': dropped_user_info.pk,
            }
            await self.broadcast(json.dumps(message))

    async def broadcast(self, message, to=None, publish_to_redis=True):
        if not to:
            to = self.websocket_info_dict.keys()
        redis_message = {
            'messageType': 'broadcast',
            'broadcastTo': 'all',
            'sender': self.SERVER_NAME,
            'message': message,
        }
        if publish_to_redis:
            self.redis.publish(
                'websocket-IPC', json.dumps(redis_message),
            )
        await asyncio.wait([socket.send(message) for socket in to])

    def websocket_ipc_handler(self, redis_message):
        data = json.loads(redis_message['data'].decode('utf8'))

        if data['sender'] == self.SERVER_NAME:
            return

        if data['messageType'] == 'broadcast':
            to = data['broadcastTo']
            message = data['message']
            if to == 'all':
                self.broadcast(
                    message, publish_to_redis=False,
                )

    def flask_ipc_handler(self, redis_message):
        print(redis_message)

    async def router(self, websocket, path):
        if websocket not in self.websocket_info_dict:
            self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                print(data)
                if data['type'] == MessageType.USER_JOINED.value:
                    await handle_new_user_joined(websocket, data)
                elif data['type'] == 'getUsernames':
                    await handle_get_usernames(websocket)
        finally:
            await self.unregister(websocket)

    def get_server_task(self, func, route='localhost', port=8000):
        start_server = websockets.serve(func, route, port)
        return start_server

    def run(self, loop=None):
        start_server = self.get_server_task(self.router)
        if loop is None:
            loop = asyncio.get_event_loop()

        loop.run_until_complete(start_server)
        loop.run_forever()
