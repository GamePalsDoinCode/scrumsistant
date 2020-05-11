import argparse
import os
import sys
from typing import cast

import redis

sys.path.insert(0, os.path.abspath(".."))
__package__ = "scrumsistant"  # pylint: disable=redefined-builtin
from backend.structs import UserInfo  # isort:skip
from backend.local_settings import REDIS_CONNECTION_URL  # isort:skip
from backend.scrum_types import RedisClient  # isort:skip


parser = argparse.ArgumentParser(description="Create a user in Redis!",)

parser.add_argument(
    "email", metavar="email", type=str,
)
parser.add_argument(
    "password", metavar="password", type=str,
)

args = parser.parse_args()

redis_client = cast(RedisClient, redis.Redis.from_url(REDIS_CONNECTION_URL))

user = UserInfo(pk=UserInfo.get_new_pk(redis_client), email=args.email, display_name="")
user.set_password(args.password)
user.save_new_user(redis_client)
