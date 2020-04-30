import json
from dataclasses import asdict as dataclass_serialize
from dataclasses import dataclass
from dataclasses import replace as dataclass_replace
from enum import Enum
from typing import List, Optional

from flask_login import AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .exceptions import *
from .redis_schema import *
from .utils import transform_to_redis_safe_dict


class AnonymousUserWrapper(AnonymousUserMixin):
    # current user will either be this or a WebSocketInfo
    # the flask builtin has is_authenticated as a property
    # but WebSocketInfo needs it to be a method.
    # To maintain ducktyping, we need this shell of a class
    # to expose a method for is_authenticated
    # it always returns False by definition (because this is a representation of a user prior to logging in)
    def is_authenticated(self, _):  # pylint: disable=arguments-differ,invalid-overridden-method
        return False


@dataclass
class WebsocketInfo:
    pk: int
    username: str = "Uninitialized"  # TODO this should either be email, or we should have email separate and this should be display name
    password: Optional[str] = None

    def serialize(
        self, skip_list: List[str] = None, serialize_method=transform_to_redis_safe_dict,
    ):
        if skip_list is None:
            skip_list = []
        serialized_form = dataclass_serialize(self)
        reduced_serialized_form = {k: v for k, v in serialized_form.items() if not k in skip_list}
        return serialize_method(reduced_serialized_form)

    @staticmethod
    def redis_transformers(field_name):
        def _string_transformer(byte_string):
            return byte_string.decode("utf8")

        def _int_transformer(num_as_byte_string):
            return int(num_as_byte_string)

        def _pk_transformer(pk_byte_string):
            return _int_transformer(pk_byte_string)

        def _username_transformer(name_byte_string):
            return _string_transformer(name_byte_string)

        def _password_transformer(password_byte_string):
            password_or_null = _string_transformer(password_byte_string)
            if password_or_null == "null":
                return None
            return password_or_null

        return locals()[f"_{field_name}_transformer"]

    @staticmethod
    def deserialize(serialized_obj, from_redis=True):
        new_obj = WebsocketInfo(pk=-1,)

        if from_redis:
            ser = {}
            for k, v in serialized_obj.items():
                key_str = k.decode("utf8")
                ser[key_str] = WebsocketInfo.redis_transformers(key_str)(v)
            serialized_obj = ser

        return dataclass_replace(new_obj, **serialized_obj)

    # methods required by flask-login
    def is_authenticated(self, session):
        return session.get("_user_id") == Users(self.pk)

    def is_active(
        self,
    ):  # pylint: disable=no-self-use  # This method is required by the flask-login library, but we don't really have this concept
        return True

    def is_anonymous(self):
        return self.username == "Uninitialized"

    def get_id(self):
        return Users(self.pk)

    # end login required methods

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        if not self.password:
            return False
        return check_password_hash(self.password, password)

    def save_new_user(self, redis_client):
        self._check_not_overwriting(redis_client)
        redis_client.set(PKByEmail(self.username), self.pk)
        redis_client.hmset(Users(self.pk), self.serialize(skip_list=["_is_authenticated"]))

    def _check_not_overwriting(self, redis_client):
        pk_associated_with_my_username_dirty = redis_client.get(
            PKByEmail(self.username)
        )  # by dirty I mean, its bytes atm
        if not pk_associated_with_my_username_dirty:
            return
        pk = int(pk_associated_with_my_username_dirty)
        if self.pk != pk:
            raise UserNameTakenError

    @staticmethod
    def get_new_pk(redis_client):
        return redis_client.incr("WEBSOCKET_PK")


class MessageType(Enum):
    USER_JOINED = "userJoined"


class HTTP_STATUS_CODE(Enum):
    HTTP_200_OK = 200
    HTTP_401_UNAUTHORIZED = 401
