from dataclasses import asdict as dataclass_serialize
from dataclasses import dataclass
from dataclasses import replace as dataclass_replace
from enum import Enum
from typing import Any, Callable, Dict, Literal, Mapping, Optional, Union

from flask_login import AnonymousUserMixin
from sqlalchemy.dialects.postgresql import insert
from werkzeug.security import check_password_hash, generate_password_hash

from .db_schema import Users
from .exceptions import UserNameTakenError
from .scrum_types import RedisClient
from .utils import transform_to_redis_safe_dict


class AnonymousUserWrapper(AnonymousUserMixin):
    # current user will either be this or a UserInfo
    # the flask builtin has is_authenticated as a property
    # but UserInfo needs it to be a method.
    # To maintain ducktyping, we need this shell of a class
    # to expose a method for is_authenticated
    # it always returns False by definition (because this is a representation of a user prior to logging in)
    def is_authenticated(self, _) -> Literal[False]:  # pylint: disable=arguments-differ,invalid-overridden-method
        return False


@dataclass
class UserInfo:
    id: Optional[int] = None  # when making a new user, wait for postgres to assign the pk
    display_name: str = ''
    email: str = ''
    password: Optional[str] = None
    is_PM: bool = False

    def serialize(
        self, skip_list=None, serialize_method=transform_to_redis_safe_dict,
    ):
        # typed in stub file!
        if skip_list is None:
            skip_list = []
        serialized_form = dataclass_serialize(self)
        reduced_serialized_form = {k: v for k, v in serialized_form.items() if not k in skip_list}
        return serialize_method(reduced_serialized_form)

    @staticmethod
    def redis_transformers(field_name: str) -> Callable[[bytes], Union[str, int, Union[None, str]]]:
        def _string_transformer(byte_string: bytes) -> str:
            return byte_string.decode("utf8")

        def _int_transformer(num_as_byte_string: bytes) -> int:
            return int(num_as_byte_string)

        def _bool_transformer(bool_as_byte_string: bytes) -> bool:
            return bool_as_byte_string.lower() == b'true'

        def _pk_transformer(pk_byte_string: bytes) -> int:
            return _int_transformer(pk_byte_string)

        def _email_transformer(name_byte_string: bytes) -> str:
            return _string_transformer(name_byte_string)

        def _display_name_transformer(display_name_byte_string: bytes) -> str:
            return _string_transformer(display_name_byte_string)

        def _password_transformer(password_byte_string: bytes) -> Union[None, str]:
            password_or_null = _string_transformer(password_byte_string)
            if password_or_null == "null":
                return None
            return password_or_null

        def _is_PM_transformer(is_pm_byte_string: bytes) -> bool:
            return _bool_transformer(is_pm_byte_string)

        return locals()[f"_{field_name}_transformer"]

    @staticmethod
    def deserialize(serialized_obj, from_redis=True) -> 'UserInfo':
        new_obj = UserInfo(pk=-1,)

        if from_redis:
            ser = {}
            for k, v in serialized_obj.items():
                key_str = k.decode("utf8")
                ser[key_str] = UserInfo.redis_transformers(key_str)(v)
        else:
            ser = serialized_obj
        return dataclass_replace(new_obj, **ser)

    # methods required by flask-login
    def is_authenticated(self, session: Mapping[str, Dict[str, Any]]) -> bool:
        return session.get("_user_id") == Users(self.pk)

    def is_active(self) -> Literal[True]:  # pylint: disable=no-self-use # pragma: no cover
        # This method is required by the flask-login library, but we don't really have this concept
        return True

    def is_anonymous(self) -> bool:
        return self.email == ''

    def get_id(self) -> str:
        return Users(self.pk)

    # end login required methods

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if self.password is None:
            return False
        return check_password_hash(self.password, password)

    def save(self, conn) -> None:
        serialized_user = self.serialize(serialize_method=dict)
        if serialized_user['id'] is None:
            serialized_user.pop('id')
            # if this is a new user, the id in python will be None
            # if you leave it lke that, pg will try to insert null
            # rather than assigning a new pk [which we want]
        save_statement = insert(Users).values(serialized_user,)
        update_on_conflict = save_statement.on_conflict_do_update(
            index_elements=['id'], set_=self.serialize(skip_list=['id'], serialize_method=dict),
        )
        conn.execute(update_on_conflict)

    def _check_not_overwriting(self, redis_client: RedisClient) -> None:
        pk_associated_with_my_username_dirty = redis_client.get(PKByEmail(self.email))  # by dirty I mean, its bytes atm
        if not pk_associated_with_my_username_dirty:
            return
        pk = int(pk_associated_with_my_username_dirty)
        if self.pk != pk:
            raise UserNameTakenError

    @staticmethod
    def get_new_pk(redis_client: RedisClient) -> int:
        return int(redis_client.incr(CurrentPKTable()))


class MessageType(Enum):
    USER_JOINED = "userJoined"


class HTTP_STATUS_CODE(Enum):
    HTTP_200_OK = 200
    HTTP_401_UNAUTHORIZED = 401
    HTTP_404_NOT_FOUND = 404
