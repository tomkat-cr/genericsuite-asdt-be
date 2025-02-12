"""
Application logger
"""
from typing import Any
import datetime


def formatted_message(message: Any) -> str:
    """
    Returns a formatted message with database name and date/time
    """
    return f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + \
           f" | {message}"


def log_general_message(message: Any, message_type: str) -> str:
    """
    Register a general log
    """
    fmt_msg = formatted_message(message)
    print(F"\n[{message_type}] {fmt_msg}")
    return fmt_msg


def log_debug(message: Any) -> str:
    """
    Register a Debug log
    """
    return log_general_message(message, "DEBUG")


def log_error(message: Any) -> str:
    """
    Register a Error log
    """
    return log_general_message(message, "ERROR")


def log_warning(message: Any) -> str:
    """
    Register a Warning log
    """
    return log_general_message(message, "WARNING")


def log_info(message: Any) -> str:
    """
    Register a Info log
    """
    return log_general_message(message, "INFO")
