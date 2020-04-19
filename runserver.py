from backend.structs import get_info_dict
WEBSOCKET_INFO_DICT = get_info_dict()

from backend.server import Server

s = Server(WEBSOCKET_INFO_DICT)
s.run()
