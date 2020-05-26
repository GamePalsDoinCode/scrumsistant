import json

import pytest
import websockets
from sqlalchemy.sql import select

from ..db_schema import Users
from ..structs import UserInfo
from .app_fixtures import *
from .pg_fixtures import *

WEBSOCKET_URI = "ws://localhost:8000"


async def test_connection_closed_if_missing_auth(send_message):
    message = json.dumps({"type": "userJoined", "name": "piss",})
    with pytest.raises(websockets.exceptions.ConnectionClosedOK):
        resp = await send_message(message)


def test_pg_fixture(db_engine):
    query = select([Users], Users.c.id == 3)
    r = db_engine.execute(query)
    print(r.fetchone())
    user = UserInfo(email='deena@deena.com', is_PM=True,)
    user.set_password('good password')
    user.save(db_engine)
