import asyncio
import atexit
import codecs
import json
import logging
from asyncio import Task
from typing import Dict, Iterable, List, cast

import nacl.encoding  # type: ignore
import nacl.signing  # type: ignore
import redis
import websockets

from .exceptions import RedisKeyNotFoundError
from .flask_utils import _load_user
from .local_settings import REDIS_CONNECTION_URL, SERVER_NAME
from .redis_schema import AuthToken, CurrentUsers, OwnsConnection, Users
from .scrum_types import WEBSOCKET_TEMP_TYPE, RedisClient
from .structs import UserInfo
from .utils import cleanup_redis_dict

LOGGER = logging.getLogger(__name__)


class Server:
    def __init__(self, redis_client: RedisClient = None) -> None:
        LOGGER.debug(f"Initializing Server")
        self.SERVER_NAME = SERVER_NAME
        self.websocket_info_dict: Dict[WEBSOCKET_TEMP_TYPE, int] = {}
        self.redis: RedisClient
        if redis_client:  # pragma: no cover
            self.redis = redis_client
        else:  # pragma: no cover
            self.redis = cast(RedisClient, redis.Redis.from_url(REDIS_CONNECTION_URL))
        redis_pubsub_instance = self.redis.pubsub(ignore_subscribe_messages=True,)
        redis_pubsub_instance.subscribe(
            **{"websocket-IPC": self.websocket_ipc_handler, "flask-IPC": self.flask_ipc_handler,}
        )
        self._redis_pubsub_thread = redis_pubsub_instance.run_in_thread(sleep_time=0.5,)

    async def _shutdown_helper(self, tasks: List[Task]) -> None:
        await asyncio.gather(*tasks)

    def shutdown_handler(self) -> None:
        print('shutting down')
        loop = asyncio.get_event_loop()
        tasks = []
        for websocket in self.websocket_info_dict:
            task = loop.create_task(self.unregister(websocket))
            tasks.append(task)
        loop.run_until_complete(self._shutdown_helper(tasks))
        self._redis_pubsub_thread.stop()

    async def register(self, websocket: WEBSOCKET_TEMP_TYPE, user: UserInfo) -> None:
        # existing_user = self.redis.hgetall(Users())

        self.websocket_info_dict[websocket] = user.pk
        print("registered", self.websocket_info_dict)
        self.redis.set(
            OwnsConnection(user.pk), self.SERVER_NAME,
        )
        self.redis.sadd(CurrentUsers(), user.pk)
        socket_message = {
            "type": "confirmJoined",
            "pk": user.pk,
        }
        await websocket.send(json.dumps(socket_message))

    async def unregister(self, websocket: WEBSOCKET_TEMP_TYPE) -> None:
        dropped_user_pk = self.websocket_info_dict.pop(websocket, None)
        print(dropped_user_pk, "socket deregistered")
        if dropped_user_pk:
            self.redis.delete(OwnsConnection(dropped_user_pk))
            self.redis.srem(CurrentUsers(), str(dropped_user_pk))
            message = {
                "type": "userLeft",
                "pk": dropped_user_pk,
                # "displayName": user_dict["display_name"],
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

    def verify_websocket_auth(self, auth_info: Dict[str, str]) -> UserInfo:
        signed_token = codecs.decode(auth_info['signedToken'], 'hex')
        verify_key = nacl.signing.VerifyKey(auth_info['verifyKey'].encode('utf8'), encoder=nacl.encoding.HexEncoder)
        token = verify_key.verify(signed_token)
        user_pk = self.redis.get(AuthToken(token))
        if not user_pk:
            raise RedisKeyNotFoundError
        user = _load_user(Users(user_pk), self.redis)  # will raise if not found
        self.redis.delete(AuthToken(token))
        return user

    async def router(self, websocket: WEBSOCKET_TEMP_TYPE, path: str) -> None:  # pylint: disable=unused-argument
        if websocket not in self.websocket_info_dict:
            init_message = json.loads(await websocket.recv())  # can throw error, will just hit the unregister
            print(init_message)
            if init_message.get('msg') == 'authTokenVerification':
                try:
                    user = self.verify_websocket_auth(init_message['data'])  # can throw error
                    await self.register(websocket, user)
                except Exception as e:
                    await websocket.close()
            else:
                await websocket.close()
        else:
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
            atexit.register(self.shutdown_handler)
        loop.run_until_complete(start_server)
        loop.run_forever()
