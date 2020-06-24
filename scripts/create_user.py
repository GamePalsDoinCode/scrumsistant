import argparse
import os
import pdb
import sys
from typing import cast

from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(".."))
__package__ = "scrumsistant"  # pylint: disable=redefined-builtin
from backend.structs import UserInfo  # isort:skip
from backend.local_settings import POSTGRES_URL  # isort:skip

engine = create_engine(POSTGRES_URL)
conn = engine.connect()

parser = argparse.ArgumentParser(description="Create a user in Postgres!",)
parser.add_argument(
    "email", type=str,
)
parser.add_argument(
    "password", type=str,
)
parser.add_argument("is_PM", type=str)
args = parser.parse_args()

user = UserInfo(email=args.email, is_PM=args.is_PM == "True",)
user.set_password(args.password)

user.save(conn)
