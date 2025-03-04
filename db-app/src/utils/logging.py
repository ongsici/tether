import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "db_microservice.log"
LOG_DIR.mkdir(exist_ok=True) # create log directory if it doesn't exist

def configure_logging():
    """
    Configure logging to include both stdout/stderr output and rotating file handler
    Log level can be set through the LOG_LEVEL environment variable
    """

    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if log_level_str not in valid_levels:
        print(f"Invalid LOG_LEVEL '{log_level_str}', defaulting to 'INFO'")
        log_level_str = "INFO"
    log_level = getattr(logging, log_level_str)

    logger = logging.getLogger("db_microservice")
    
    if not logger.hasHandlers(): # prevent adding handlers multiple times
        logger.setLevel(log_level)

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format) # include: timestamp, logger name, log level, message

        # Console handler for lower-level logs (DEBUG, INFO) -> stdout
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_handler.addFilter(lambda record: record.levelno < logging.WARNING)  
        stdout_handler.setFormatter(formatter)
        logger.addHandler(stdout_handler)

        # Console handler for WARNING and above -> stderr
        stderr_handler = logging.StreamHandler(sys.stderr)
        stderr_handler.setLevel(logging.WARNING)
        stderr_handler.setFormatter(formatter)
        logger.addHandler(stderr_handler)

        # TimedRotatingFileHandler for file-based logs (all levels)
        file_handler = TimedRotatingFileHandler(
            LOG_FILE,
            when="midnight",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # limit verbose logs from external libraries
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        logger.info(
            f"Logging configuration: level={log_level_str}, "
            f"log file='{LOG_FILE}', rotating daily with up to 7 backups"
        )