from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class WebsocketInfo:
	pk: int
	username: str


class MessageType(Enum):
	USER_JOINED = 'userJoined'
