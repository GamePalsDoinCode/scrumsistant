from dataclasses import dataclass
from enum import Enum
from typing import Optional

import redis
from dataclasses_serialization.json import JSONSerializer
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class WebsocketInfo:
    pk: int
    username: str = 'Uninitialized'
    password: Optional[str] = None
    _is_authenticated: bool = False

    # methods required by flask-login
    def is_authenticated(self):
        return _is_authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return self.username == 'Uninitialized'

    def get_id(self):
        return f'user_{self.pk}'

    # end login required methods

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(password):
        if not self.password:
            return False
        return check_password_hash(self.password, password)

    def save_new_user(self, redis_client):
        redis_client.hmset(f'user_{self.pk}', JSONSerializer.serialize(self))
        self._check_not_overwriting()
        redis_client.set(self.username, self.pk)
        return

    def _check_not_overwriting():
        pk_associated_with_my_username_dirty = redis.get(self.username)
        if not pk_associated_with_my_username_dirty:
            redis.set(self.username, self.pk)
            return
        pk = int(pk_associated_with_my_username_dirty)
        if self.pk != pk:
            raise TypeError  # TODO implement custom error

    @staticmethod
    def get_new_pk(redis_client):
        return redis_client.incr('WEBSOCKET_PK')


class MessageType(Enum):
    USER_JOINED = 'userJoined'
