import logging
import logging.handlers
import platform


def init_logging() -> None:
    logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_filename = "/var/log/scrumsistant/scrum.log"
    if platform.system() == "Windows":
        # For us ghouls that are running on Windows, won't have a /var, so log locally
        log_filename = "scrum.log"

    logging.basicConfig(level=logging.INFO, filename=log_filename, format=logging_format)
