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
        self, skip_list=None, serialize_method=dict,
    ):
        # typed in stub file!
        if skip_list is None:
            skip_list = []
        serialized_form = dataclass_serialize(self)
        reduced_serialized_form = {k: v for k, v in serialized_form.items() if not k in skip_list}
        return serialize_method(reduced_serialized_form)

    @staticmethod
    def deserialize(serialized_obj) -> 'UserInfo':
        new_obj = UserInfo(id=-1,)
        return dataclass_replace(new_obj, **serialized_obj)

    # methods required by flask-login
    def is_authenticated(self, session: Mapping[str, Dict[str, Any]]) -> bool:
        return session.get("_user_id") == str(self.id)

    def is_active(self) -> Literal[True]:  # pylint: disable=no-self-use # pragma: no cover
        # This method is required by the flask-login library, but we don't really have this concept
        return True

    def is_anonymous(self) -> bool:
        return self.email == ''

    def get_id(self) -> str:
        return str(self.id)  # per docs, this method _must_ return string

    # end flask-login required methods

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
            index_elements=['id'], set_=self.serialize(skip_list=['id']),
        )
        conn.execute(update_on_conflict)


class MessageType(Enum):
    USER_JOINED = "userJoined"


class HTTP_STATUS_CODE(Enum):
    HTTP_200_OK = 200
    HTTP_401_UNAUTHORIZED = 401
    HTTP_404_NOT_FOUND = 404
