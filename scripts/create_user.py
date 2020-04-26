import argparse
import os
import sys

import redis

sys.path.insert(0, os.path.abspath(".."))
__package__ = "scrumsistant"  # pylint: disable=redefined-builtin
from backend.structs import WebsocketInfo  # isort:skip

try:
    from local_settings import SERVER_NAME, REDIS_URL, REDIS_PASSWORD, REDIS_PORT
except ImportError:
    SERVER_NAME = "me"
    REDIS_URL = "localhost"
    REDIS_PASSWORD = ""
    REDIS_PORT = 6379
    REDIS_DB = 0


parser = argparse.ArgumentParser(description="Create a user in Redis!",)

parser.add_argument(
    "email", metavar="email", type=str,
)
parser.add_argument(
    "password", metavar="password", type=str,
)

args = parser.parse_args()

redis_client = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,)

user = WebsocketInfo(pk=WebsocketInfo.get_new_pk(redis_client), username=args.email,)
user.set_password(args.password)
user.save_new_user(redis_client)
