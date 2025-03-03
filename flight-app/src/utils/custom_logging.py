import logging
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "flight_microservice.log"
LOG_DIR.mkdir(exist_ok=True) # create log directory if it doesn't exist

def configure_logging():
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format) # include: timestamp, logger name, log level, message

    logger = logging.getLogger("flight_microservice")
    logger.setLevel(logging.INFO)  # include: DEBUG, INFO, WARNING, ERROR, CRITICAL

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # limit verbose logs from external libraries
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)