import logging

from backend.server import Server
from backend.settings import init_logging

init_logging()
logger = logging.getLogger(__name__)

s = Server(host="localhost")
logger.info("Starting up")
s.run()
