"""
Logging utilities
"""

from typing import Any
import os
import sys
import logging
import logging.config
import datetime

from genericsuite.config.config import Config, is_local_service

settings = Config()


def log_config() -> logging:
    """ Logging configuration """
    logger = logging.getLogger(settings.APP_NAME)
    logger.propagate = False
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)s-%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


app_logs = log_config()


def db_stamp() -> str:
    db_engine = os.environ['APP_DB_ENGINE']
    if db_engine == 'DYNAMO_DB':
        response = f"{db_engine}|" + \
                   f"{os.environ.get('DYNAMDB_PREFIX', 'No-Prefix')}"
    else:
        response = f"{db_engine}|{os.environ['APP_DB_NAME']}"
    if is_local_service():
        response += "|LOCAL"
    else:
        response += "|CLOUD"
    return response


def formatted_message(message: Any) -> str:
    """ Returns a formatted message with database name and date/time """
    return f"[{db_stamp()}]" + \
           f" {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + \
           f" | {message}"


def log_debug(message: Any) -> str:
    """Register a Debug log"""
    fmt_msg = formatted_message(message)
    app_logs.debug("%s", fmt_msg)
    return fmt_msg


def log_info(message: Any) -> str:
    """Register a Warning log"""
    fmt_msg = formatted_message(message)
    app_logs.info("%s", fmt_msg)
    return fmt_msg


def log_warning(message: Any) -> str:
    """Register a Warning log"""
    fmt_msg = formatted_message(message)
    app_logs.warning("%s", fmt_msg)
    return fmt_msg


def log_error(message: Any) -> str:
    """Register a Warning log"""
    fmt_msg = formatted_message(message)
    app_logs.error("%s", fmt_msg)
    return fmt_msg
