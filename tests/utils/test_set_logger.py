import logging
import pytest

from fia.utils.set_logger import set_logger


def test_default_logger_level():
    """Tests the default logger level."""
    set_logger()
    logger = logging.getLogger()
    assert logger.level == 20


@pytest.mark.parametrize(
    "level, int_level",
    [
        ("CRITICAL", 50),
        ("ERROR", 40),
        ("WARNING", 30),
        ("INFO", 20),
        ("DEBUG", 10),
        ("NOTSET", 0),
    ]
)
def test_custom_logger_level(level, int_level):
    """Tests the custom logger levels."""
    set_logger(level)
    logger = logging.getLogger()
    assert logger.level == int_level
