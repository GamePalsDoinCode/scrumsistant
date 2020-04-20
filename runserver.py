import logging
from backend.structs import get_info_dict
WEBSOCKET_INFO_DICT = get_info_dict()

from backend.server import Server
from backend.settings import init_logging

init_logging()
logger = logging.getLogger(__name__)

logger.info("Starting up")
s = Server(WEBSOCKET_INFO_DICT)
s.run()
