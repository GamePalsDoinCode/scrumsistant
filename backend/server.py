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
from sqlalchemy import create_engine

from .exceptions import RedisKeyNotFoundError
from .flask_utils import _load_user
from .local_settings import POSTGRES_URL, REDIS_CONNECTION_URL, SERVER_NAME
from .redis_schema import AuthToken, CurrentUsers, OwnsConnection
from .scrum_types import WEBSOCKET_TEMP_TYPE, AuthInfoPacket, RedisClient
from .structs import UserInfo

LOGGER = logging.getLogger(__name__)


class Server:
    def __init__(self, host=None, redis_client: RedisClient = None, db=None) -> None:
        self.SERVER_NAME = SERVER_NAME
        self.websocket_info_dict: Dict[WEBSOCKET_TEMP_TYPE, int] = {}
        self.redis: RedisClient
        self.host = host or '0.0.0.0'
        if redis_client:  # pragma: no cover
            self.redis = redis_client
        else:  # pragma: no cover
            self.redis = cast(RedisClient, redis.Redis.from_url(REDIS_CONNECTION_URL))
        if db:  # pragma: no cover
            self.db = db
        else:  # pragma: no cover
            engine = create_engine(POSTGRES_URL)
            self.db = engine.connect()
        redis_pubsub_instance = self.redis.pubsub(ignore_subscribe_messages=True,)
        redis_pubsub_instance.subscribe(
            **{"websocket-IPC": self.websocket_ipc_handler, "flask-IPC": self.flask_ipc_handler,}
        )
        self._redis_pubsub_thread = redis_pubsub_instance.run_in_thread(sleep_time=0.5,)
        LOGGER.info(f'Initialized Server at {self.host}')

    async def _shutdown_helper(self, tasks: List[Task]) -> None:
        await asyncio.gather(*tasks)

    def shutdown_handler(self) -> None:
        LOGGER.info(f'Shutting Down Server - closing {len(self.websocket_info_dict)} sockets')
        loop = asyncio.get_event_loop()
        tasks = []
        for websocket in self.websocket_info_dict:
            task = loop.create_task(self.unregister(websocket))
            tasks.append(task)
        loop.run_until_complete(self._shutdown_helper(tasks))
        self._redis_pubsub_thread.stop()

    async def register(self, websocket: WEBSOCKET_TEMP_TYPE, user: UserInfo) -> None:
        assert user.id is not None  # mostly to convince mypy that its an int at this point
        LOGGER.info(f'Attempting to register socket for user:{user.email}')
        existing_sockets = [ws for ws, user_id in self.websocket_info_dict.items() if user_id == user.id]
        for sock in existing_sockets:
            LOGGER.info(f'Removing stale socket for user:{user.email}')
            await self.unregister(sock)

        self.websocket_info_dict[websocket] = user.id
        self.redis.set(
            OwnsConnection(user.id), self.SERVER_NAME,
        )
        self.redis.sadd(CurrentUsers(), user.id)

        auth_confirm_message = {
            'channel': 'auth',
            'message': 'authOK',
        }
        LOGGER.debug(f'Sending auth ok packet: {auth_confirm_message}')
        LOGGER.info(f'Socket {id(websocket)} registered as user {user.email} (id: {user.id})')
        await websocket.send(json.dumps(auth_confirm_message))

    async def unregister(self, websocket: WEBSOCKET_TEMP_TYPE) -> None:
        dropped_user_pk = self.websocket_info_dict.pop(websocket, None)
        LOGGER.info(f"Deregistering socket {id(websocket)} for user {dropped_user_pk}")
        if dropped_user_pk:
            self.redis.delete(OwnsConnection(dropped_user_pk))
            self.redis.srem(CurrentUsers(), str(dropped_user_pk))
            message = {
                "type": "userLeft",
                "pk": dropped_user_pk,
                # "displayName": user_dict["display_name"],
            }
            LOGGER.debug(f'Sending user left packet {message}')
            await self.broadcast(json.dumps(message))
        LOGGER.debug(f'Closing socket {id(websocket)} in unregister function')
        await websocket.close()

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
        if to:
            LOGGER.debug(f'Sending broadcast packet {message} to {[id(ws) for ws in to]}')
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

    def verify_websocket_auth(self, auth_info: AuthInfoPacket) -> UserInfo:
        signed_token = codecs.decode(auth_info['signedToken'], 'hex')
        verify_key = nacl.signing.VerifyKey(auth_info['verifyKey'].encode('utf8'), encoder=nacl.encoding.HexEncoder)
        token = verify_key.verify(signed_token)
        user_pk = self.redis.get(AuthToken(token))
        if not user_pk:
            raise RedisKeyNotFoundError
        user = _load_user(user_pk.decode('utf8'), self.db)  # will raise if not found
        self.redis.delete(AuthToken(token))
        LOGGER.info(f'Auth Verification Succeeded for {user.email}')
        return user

    async def router(self, websocket: WEBSOCKET_TEMP_TYPE, path: str) -> None:  # pylint: disable=unused-argument
        LOGGER.debug(f'new connection: {id(websocket)}')
        while not websocket.closed:
            if websocket not in self.websocket_info_dict:
                raw_message = await websocket.recv()
                LOGGER.debug(f'[unauthed] raw message: {raw_message[:10]}...')
                init_message = json.loads(raw_message)  # can throw error, will just hit the unregister
                LOGGER.debug(f'[unauthed] json loaded message: {init_message.keys()}')
                if init_message.get('msg') == 'authTokenVerification':
                    try:
                        user = self.verify_websocket_auth(init_message['data'])  # can throw error
                        await self.register(websocket, user)

                    except Exception as e:
                        import traceback

                        traceback.print_exc()
                        LOGGER.debug('calling close: exception in unauthed')
                        await websocket.close()
                        break
                elif init_message.get('multiplexChannelVerb') not in ['open', 'close']:
                    LOGGER.debug('calling close, unrecognized message in unauthed')
                    await websocket.close()
            else:
                try:
                    async for message in websocket:
                        LOGGER.debug(f'[authed] raw message: {message}')
                        data = json.loads(message)
                        LOGGER.debug(f'[authed] json loaded message: {data}')
                except Exception as e:
                    import traceback
                    traceback.print_exc()
                    break
                finally:
                    LOGGER.debug('unregistering in authed path')
                    await self.unregister(websocket)


    def get_server_task(self, func, port=8000):
        start_server = websockets.serve(func, host=self.host, port=port)
        return start_server

    def run(self, loop: asyncio.AbstractEventLoop = None) -> None:
        start_server = self.get_server_task(self.router)
        if loop is None:
            loop = asyncio.get_event_loop()
            atexit.register(self.shutdown_handler)
        loop.run_until_complete(start_server)
        loop.run_forever()
