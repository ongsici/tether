import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "flight_microservice.log"
LOG_DIR.mkdir(exist_ok=True)  # create log directory if it doesn't exist

def configure_logging():
    """
    Configure logging to include console output and a rotating file handler.
    Log level can be set through the LOG_LEVEL environment variable.
    """

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if log_level_str not in valid_levels:
        print(f"Invalid LOG_LEVEL '{log_level_str}' specified. Falling back to 'INFO'.")
        log_level_str = "INFO"
    log_level = getattr(logging, log_level_str)

    logger = logging.getLogger("flight_microservice")
    logger.setLevel(log_level)

    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(log_level)
    logger.addHandler(console_handler)

    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(log_level)
    logger.addHandler(file_handler)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    logger.info(
        f"Logging is configured. Level={log_level_str}, "
        f"Log file='{LOG_FILE}', Rotating daily with up to 7 backups."
    )
