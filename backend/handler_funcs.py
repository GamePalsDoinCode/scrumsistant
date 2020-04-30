import json


async def handle_get_usernames(websocket):
    # TODO move to flask
    await websocket.send(json.dumps({'type': 'getUsernames', 'usernames': ['SUPER PUNK']}))


async def handle_new_user_joined(websocket, data):
    # TODO move to flask
    return
