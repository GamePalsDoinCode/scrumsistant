import asyncio
import atexit
import json
import logging
from typing import Any, Callable, Dict, Iterable

import redis
import websockets

from .local_settings import REDIS_DB, REDIS_PORT, REDIS_URL, SERVER_NAME
from .scrum_types import WEBSOCKET_TEMP_TYPE
from .structs import WebsocketInfo
from .utils import cleanup_redis_dict

LOGGER = logging.getLogger(__name__)


class Server:
    def __init__(self) -> None:
        LOGGER.debug(f"Initializing Server")
        self.SERVER_NAME = SERVER_NAME
        self.websocket_info_dict: Dict[WEBSOCKET_TEMP_TYPE, int] = {}
        self.redis = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,)
        atexit.register(self.shutdown_handler)

        redis_pubsub_instance = self.redis.pubsub(ignore_subscribe_messages=True,)
        redis_pubsub_instance.subscribe(
            **{"websocket-IPC": self.websocket_ipc_handler, "flask-IPC": self.flask_ipc_handler,}
        )
        self._redis_pubsub_thread = redis_pubsub_instance.run_in_thread(sleep_time=0.5,)

    async def _shutdown_helper(self, tasks):
        await asyncio.gather(*tasks)

    def shutdown_handler(self):
        print('shutting down')
        loop = asyncio.get_event_loop()
        tasks = []
        for websocket in self.websocket_info_dict.keys():
            task = loop.create_task(self.unregister(websocket))
            tasks.append(task)
        loop.run_until_complete(self._shutdown_helper(tasks))

    async def register(self, websocket: WEBSOCKET_TEMP_TYPE) -> None:
        next_pk = self.redis.incr("WEBSOCKET_PK")
        new_user_obj = WebsocketInfo(pk=next_pk, username="Uninitialized",)
        self.websocket_info_dict[websocket] = new_user_obj.pk
        print("registered", self.websocket_info_dict)
        self.redis.set(
            f"owns-connection-{new_user_obj.pk}", self.SERVER_NAME,
        )
        self.redis.hmset(f"user_{new_user_obj.pk}", new_user_obj.serialize())
        self.redis.sadd("currentUserPKs", new_user_obj.pk)
        socket_message = {
            "type": "confirmJoined",
            "pk": new_user_obj.pk,
        }
        print("new pk registered", next_pk)
        await websocket.send(json.dumps(socket_message))

    async def unregister(self, websocket: WEBSOCKET_TEMP_TYPE) -> None:
        dropped_user_pk = self.websocket_info_dict.pop(websocket, None)
        print(dropped_user_pk, "socket deregistered")
        if dropped_user_pk:
            self.redis.delete(f"owns-connection-{dropped_user_pk}")
            user_dict = cleanup_redis_dict(self.redis.hgetall(f"user_{dropped_user_pk}"))
            self.redis.delete(f"user_{dropped_user_pk}")
            self.redis.srem("currentUserPKs", str(dropped_user_pk).encode("utf8"))
            message = {
                "type": "userLeft",
                "pk": dropped_user_pk,
                "name": user_dict["username"],
            }
            await self.broadcast(json.dumps(message))

    async def broadcast(
        self, message: str, to: Iterable[WEBSOCKET_TEMP_TYPE] = None, publish_to_redis: bool = True
    ) -> None:
        if not to:
            to = self.websocket_info_dict.keys()
        redis_message = {
            "messageType": "broadcast",
            "broadcastTo": "all",
            "sender": self.SERVER_NAME,
            "message": message,
        }
        if publish_to_redis:
            self.redis.publish(
                "websocket-IPC", json.dumps(redis_message),
            )
        print(to)
        if to:
            await asyncio.wait([socket.send(message) for socket in to])

    def websocket_ipc_handler(self, redis_message: Dict[str, bytes]) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = json.loads(redis_message["data"].decode("utf8"))

        if data["sender"] == self.SERVER_NAME:
            return

        if data["messageType"] == "broadcast":
            to = data["broadcastTo"]
            message = data["message"]
            if to == "all":
                task = loop.create_task(self.broadcast(message, publish_to_redis=False,))
                loop.run_until_complete(task)

    def flask_ipc_handler(self, redis_message: Dict[str, bytes]) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        data = json.loads(redis_message["data"].decode("utf8"))
        if data["messageType"] == "userUpdated":
            to = data["broadcastTo"]
            message = data["message"]
            if to == "all":
                print("sending flask message", message)
                task = loop.create_task(self.broadcast(message, publish_to_redis=False,))
                loop.run_until_complete(task)

    async def router(self, websocket: WEBSOCKET_TEMP_TYPE, path: str) -> None:  # pylint: disable=unused-argument
        if websocket not in self.websocket_info_dict:
            await self.register(websocket)
        try:
            async for message in websocket:
                data = json.loads(message)
                print(data)
                # if data['type'] == MessageType.USER_JOINED.value:
                #     await handle_new_user_joined(websocket, data)
                # elif data['type'] == 'getUsernames':
                #     await handle_get_usernames(websocket)
        finally:
            await self.unregister(websocket)

    def get_server_task(self, func, route="localhost", port=8000):  # pylint: disable=no-self-use
        start_server = websockets.serve(func, route, port)
        return start_server

    def run(self, loop: asyncio.AbstractEventLoop = None) -> None:
        start_server = self.get_server_task(self.router)
        if loop is None:
            loop = asyncio.get_event_loop()

        loop.run_until_complete(start_server)
        loop.run_forever()
