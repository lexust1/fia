""" This module helps to set the logging system for the package.

This module helps to set the logging system for the package.

1. When the package is used over command line interface the root logger
   is set by default and shows the info messages.

2. When the package is imported the root logger is not set. It prevents
   collisions with the logging system of the program where the package
   was imported.

The child loggers are set in every module:
logger = logging.getLogger(__name__)

Functions:
    - set_logger: Helps to set the root logger.
"""
import logging
import sys


def set_logger(level: str = "INFO") -> None:
    """ Sets the root_logger.

    This function sets the root logger and configures the log level.

    Args:
        level: The log level ("INFO", "DEBUG", etc).
    """
    logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "{asctime} | {name} | {levelname} | {message}", style="{"
    )
    handler = logging.StreamHandler(sys.stdout)
    # handler = logging.FileHandler('file.log')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
