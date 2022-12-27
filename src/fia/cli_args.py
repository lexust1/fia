# Copyright 2022 Aleksey Ustinov.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.
"""This module parses the command line arguments.

The module parses the command line interface arguments, checks that
username and password is not None, sets the module logger.

This module is a part of the fia package and should not be used
separately.

Functions:
    - _cli_args: Parses CLI arguments
"""
# Import the standard libraries.
import argparse
import logging
import os

# Import the local/project packages and modules.
from fia.constants import Frame, REMEMBER, USER_AGENT


# Set the module logger.
logger = logging.getLogger(__name__)


def _cli_args() -> argparse.Namespace:
    """Parses CLI arguments

    Parses CLI arguments: username, password, exchange, ticker_sym,
    currency, frame, bars, user_agent, remember.

    Returns:
        Namespace
    """
    parser = argparse.ArgumentParser(
        description="The data collector from TradingView"
    )
    parser.add_argument(
        "-u", "--username",
        dest="USERNAME",
        default=os.environ.get("TV_USERNAME"),
        type=str,
        help="The TradingView USERNAME."
    )
    parser.add_argument(
        "-p", "--password",
        dest="PASSWORD",
        default=os.environ.get("TV_PASSWORD"),
        type=str,
        help="The TradingView PASSWORD."
    )
    parser.add_argument(
        "-e", "--exchange",
        dest="EXCHANGE",
        required=True,
        type=str,
        help="Exchange (NYSE, CME, etc.)"
    )
    parser.add_argument(
        "-t", "--ticker_sym",
        dest="TICKER_SYM",
        required=True,
        type=str,
        help="Ticker symbol (AAPL, BTC, etc.)"
    )
    parser.add_argument(
        "-c", "--currency",
        dest="CURRENCY",
        required=True,
        type=str,
        help="Currency (USD, EUR, etc.)"
    )
    parser.add_argument(
        "-f", "--frame",
        dest="FRAME",
        required=True,
        choices=Frame.__members__,
        help="Timeframe for every bar (MIN1 - 1 min, MIN5 - 5 min, "
             "MIN15 - 15 min, MIN30 - 30 min, MIN45 - 45 min, HOUR1 - 1 hr, "
             "HOUR2 - 2 hr, HOUR3 - 3 hr, HOUR4 - 4 hr, DAY - day, "
             "WEEK - week, MONTH - month)"
    )
    parser.add_argument(
        "-b", "--bars",
        dest="BARS",
        required=True,
        type=int,
        help="The number of bars"
    )
    parser.add_argument(
        "-a", "--user_agent",
        dest="USER_AGENT",
        default=USER_AGENT,
        type=str,
        help="The user_agent value. See the default value in constants.py."
    )
    parser.add_argument(
        "-r", "--remember",
        dest="REMEMBER",
        default=REMEMBER,
        type=str,
        help="Remember the use (default: on)"
    )
    return parser.parse_args()


cli_args = _cli_args()
logger.debug(f"Command line arguments: {cli_args}")
# Check that username and password is not None.
if cli_args.USERNAME is None or cli_args.PASSWORD is None:
    logger.error("You have to set up USERNAME OR/AND PASSWORD over command "
                 "line interface or add environment variables.")
    raise SystemExit("You have to set up USERNAME OR/AND PASSWORD over "
                     "command line interface or add environment variables.")
