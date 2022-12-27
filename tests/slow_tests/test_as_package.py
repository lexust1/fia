# Use . ./setenv.sh before testing.
import sys

import pandas as pd
import os
import pytest

from fia import Frame, set_logger, TvDataCollector


@pytest.mark.slow
def test_as_package():
    """Tests as the imported package."""
    # Set the logger to see status.
    # set_logger("DEBUG")

    import logging
    # Get the logger.
    logger = logging.getLogger("fia")
    # Set the level of messages for the logger.
    logger.setLevel(logging.DEBUG)
    # Set the log message style.
    formatter = logging.Formatter(
        "{asctime} | {name} | {levelname} | {message}", style="{"
    )
    # Set and attach the handler.
    handler = logging.StreamHandler(sys.stdout)
    # handler = logging.FileHandler('file.log')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    tvdc = TvDataCollector(username=os.environ.get("TV_USERNAME"),
                           password=os.environ.get("TV_PASSWORD"),
                           exchange="NASDAQ", #CME
                           ticker_sym="AAPL", #BTC1!
                           currency="USD",
                           # frame="D",
                           frame=Frame.DAY,
                           bars=50)

    raw_data = tvdc.get_data()
    df = tvdc.get_pandas_data(raw_data, tz="America/Chicago")
    assert isinstance(df, pd.DataFrame)



