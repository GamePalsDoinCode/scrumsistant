import logging
import logging.handlers
import platform


def init_logging():
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_filename = "/var/log/scrumsistant/scrum.log"
    if platform.system() == "Windows":
        # For us ghouls that are running on Windows, won't have a /var, so log locally
        log_filename = "scrum.log"
    # I would imagine that in production that we would just have a long running service that would log over
    # a long period, so we might have a size determined rotation, but during development I find it helpful
    # to restart the logs every run, seeing as different runs are common
    dev_handler = logging.handlers.RotatingFileHandler(log_filename, backupCount=10)
    dev_handler.doRollover()
    logging.basicConfig(level=logging.DEBUG, handlers=[dev_handler], format=logging_format)