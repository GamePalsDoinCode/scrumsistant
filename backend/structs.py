from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class WebsocketInfo:
    username: str


class MessageType(Enum):
    USER_JOINED = "userJoined"


# This should pretty much be replaced with redis
_WEBSOCKET_INFO_DICT: Dict[Any, WebsocketInfo] = {}


def get_info_dict():
    return _WEBSOCKET_INFO_DICT
