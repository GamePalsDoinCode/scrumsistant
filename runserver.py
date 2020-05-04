import logging

from backend.server import Server
from backend.settings import init_logging

init_logging()
logger = logging.getLogger(__name__)

s = Server()
logger.info("Starting up")
print("Starting Server...")
s.run()
