import argparse
import os.path as path
import sys
from inspect import getsourcefile

import redis
from structs import WebsocketInfo

current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[: current_dir.rfind(path.sep)])

try:
    from local_settings import SERVER_NAME, REDIS_URL, REDIS_PASSWORD, REDIS_PORT
except:
    SERVER_NAME = 'me'
    REDIS_URL = 'localhost'
    REDIS_PASSWORD = ''
    REDIS_PORT = 6379
    REDIS_DB = 0
sys.path.pop(0)


parser = argparse.ArgumentParser(description='Create a user in Redis!',)

parser.add_argument(
    'email', metavar='email', type=str,
)
parser.add_argument(
    'password', metavar='password', type=str,
)

args = parser.parse_args()

redis_client = redis.Redis(host=REDIS_URL, port=REDIS_PORT, db=REDIS_DB,)

user = WebsocketInfo(pk=WebsocketInfo.get_new_pk(redis_client), username=args.email,)
user.set_password(args.password)
user.save_new_user(redis_client)
