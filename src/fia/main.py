#!/usr/bin/env python3
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
"""This module gets the market data from TradingView over Websocket.

The module gets the historical data from TradingView over Websocket in
different formats.

Functions:
    - main: The main function of the module.

Classes:
    - TvDataCollector: Gets the historical market data from TradingView.
"""
# Import the standard libraries.
import datetime
import json
import logging
import os
import random
import re
import string
from typing import Dict, List

# Import the third party libraries.
import pandas as pd
import requests
import websocket
from websocket import create_connection

# Import the local/project packages and modules.
from fia.constants import Frame, REMEMBER, USER_AGENT
from fia.utils.create_property import create_property


# Set the module logger.
logger = logging.getLogger(__name__)


class TvDataCollector:
    """Gets the historical market data from TradingView.

    TvDataCollector class:
        - Collects the historical market data over Websocket from
          TradingView.
        - Clears the raw data.
        - Can save the market data as json-file.
        - Saves the final data as Pandas DataFrame that includes the
          following columns:
            - DataTime
            - Open price
            - High Price
            - Low Price
            - Close Price
            - Volume.

    Attributes:
        username: A Trading View username (not to be confused with
            email).
        password: A Trading View password.
        exchange: An exchange (NYSE, CME, etc.).
        ticker_sym: A ticker symbol (AAPL, BTC, etc.)
        currency: A currency (USD, EUR, etc.).
        frame: A bar timeframe as a member of enum Frame (Frame.DAY -
            day, Frame.WEEK - week, etc.). See frame property for
            additional information.
        bars: A number of bars (the limit depends on the Tradingview
            plan and the ticker symbol).
        user_agent: A user agent (optional), see the default value in
            constants.py.
        remember: A status (optional): "on" - remember the user ("off"
        - the opposite one), see the default value in constants.py.

    Methods:
        get_auth_token(): Gets the authorization token.
        get_data(): Gets the raw data over Websocket.
        get_pandas_data(raw_data): Gets the market data as Pandas
            DataFrame from the raw data.
        get_json_data(raw_data): Gets the market data in JSON format
            from the raw data.
    """
    def __init__(self,
                 username: str,
                 password: str,
                 exchange: str,
                 ticker_sym: str,
                 currency: str,
                 frame: Frame,
                 bars: int,
                 user_agent: str = USER_AGENT,
                 remember: str = REMEMBER) -> None:
        """Class constructor.
        See attributes in the class level docstring.
        """
        self.username = username
        self.password = password
        self.exchange = exchange
        self.ticker_sym = ticker_sym
        self.currency = currency
        self.frame = frame  # type: ignore
        self.bars = bars
        self.user_agent = user_agent
        self.remember = remember

    # Set property for username, password, exchange, ticker_sym,
    # currency, user_agent(optional), remember(optional).
    username = create_property("username")
    password = create_property("password")
    exchange = create_property("exchange")
    ticker_sym = create_property("ticker_sym")
    currency = create_property("currency")
    user_agent = create_property("user_agent")
    remember = create_property("remember")

    # Set property for frame.
    @property
    def frame(self) -> str:
        """The getter and setter for timeframe property.

        The getter gets the value of bar timeframe. The setter gets the
        value of the member of Frame enum and sets the value of bar
        timeframe.

        Args:
            value: A member of enum Frame. The following values are
                acceptable:
                Frame.MIN1 - 1 min,
                Frame.MIN5 - 5 min,
                Frame.MIN15 - 15 min,
                Frame.MIN30 - 30 min,
                Frame.MIN45 - 45 min,
                Frame.HOUR1 - 1 hr,
                Frame.HOUR2 - 2 hr,
                Frame.HOUR3 - 3 hr,
                Frame.HOUR4 - 4 hr,
                Frame.DAY - day,
                Frame.WEEK - week,
                Frame.MONTH - month

        Returns:
            _frame: A value of bar timeframe returned by the setter.
        """
        return self._frame

    @frame.setter
    def frame(self, value: Frame) -> None:
        self._frame = value.value

    # Set property for bars.
    @property
    def bars(self) -> int:
        """The getter and setter for bars.

        The getter gets a number of bars. The setter checks that
        a number of bars is a positive integer and sets the value of a
        number of bars.

        Args:
            value: A number of bars.

        Returns:
            _bars: A number of bars returned by the setter.

        Raises:
            SystemExit: if a number of bars is not a positive integer.
        """
        return self._bars

    @bars.setter
    def bars(self, value: int) -> None:
        if isinstance(value, int) and value > 0:
            self._bars = value
        else:
            logger.error("Check your bars value. It has to be a positive "
                         "integer.",
                         exc_info=True,
                         stack_info=True)
            raise SystemExit("Check your bars value. It has to be a "
                             "positive integer.")

    def get_auth_token(self) -> str:
        """Gets the authorization token.

        Gets the authorization token generated for your username
        on TradingView when you sign in.

        Returns:
            auth_token: The authorization token

        Raises:
            SystemExit: if there is a problem with WebSocket connection.
        """
        # Sign in url and headers for authorization on TradingView.
        sign_in_url: str = "https://www.tradingview.com/accounts/signin/"
        sign_in_headers: Dict[str, str] = {
            "Referer": "https://www.tradingview.com",
            "User-Agent": self.user_agent
        }
        data: Dict[str, str] = {
            "username": self.username,
            "password": self.password,
            "remember": self.remember
        }
        try:
            response: requests.Response = requests.post(
                url=sign_in_url,
                data=data,
                headers=sign_in_headers,
                timeout=5
            )
        except requests.ConnectionError as e:
            logger.error(f"Problems with Websocket connection: {e}",
                         exc_info=True,
                         stack_info=True)
            raise SystemExit(f"Problems with Websocket connection: {e}") from e
        auth_token: str = response.json()["user"]["auth_token"]
        logger.debug(f"The authorization token was received: {auth_token}")
        return auth_token

    def get_data(self) -> str:
        """Gets the raw data.

        This function:
            - Creates the websocket connection.
            - Generates the session tokens.
            - Creates the websocket messages.
            - Send the messages.
            - Gets the raw data that includes all received messages in
              response to the output messages over the websocket
              connection.

        Returns:
            raw_data: The raw data.
        """
        # Create the websocket connection and generate session tokens.
        ws: websocket.WebSocket = self._create_ws_connection()
        cs_token = "cs_" + self._generate_random_token()
        qs_token = "qs_" + self._generate_random_token()
        # Send the messages to TV.
        # The sample message for "set_auth_token":
        # ~m~526~m~{"m":"set_auth_token","p":["eyJ...9U0"]}
        ws.send(
            self._create_message(
                m="set_auth_token",
                p=[self.get_auth_token()]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "chart_create_session":
        # ~m~55~m~{"m":"chart_create_session","p":["cs_h2k...0xq",""]}
        ws.send(
            self._create_message(
                m="chart_create_session",
                p=[cs_token, ""]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "quote_create_session":
        # ~m~52~m~{"m":"quote_create_session","p":["qs_mOM...p5Y"]}
        ws.send(self._create_message(m="quote_create_session", p=[qs_token]))
        logger.debug("The message was sent.")
        # The sample message for "quote_set_fields":
        # ~m~432~m~{"m":"quote_set_fields","p":["qs_uIk...Rqj",
        # "base-currency-logoid","ch", ..., "volume","value_unit_id"]}
        ws.send(
            self._create_message(
                m="quote_set_fields",
                p=[
                    qs_token,
                    "base-currency-logoid",
                    "ch",
                    "chp",
                    "currency-logoid",
                    "currency_code",
                    "currency_id",
                    "base_currency_id",
                    "current_session",
                    "description",
                    "exchange",
                    "format",
                    "fractional",
                    "is_tradable",
                    "language",
                    "local_description",
                    "listed_exchange",
                    "logoid",
                    "lp",
                    "lp_time",
                    "minmov",
                    "minmove2",
                    "original_name",
                    "pricescale",
                    "pro_name",
                    "short_name",
                    "type",
                    "typespecs",
                    "update_mode",
                    "volume",
                    "value_unit_id"
                ]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "quote_add_symbols":
        # ~m~63~m~{"m":"quote_add_symbols","p":["qs_mOM...p5Y",
        # "NASDAQ:AAPL"]}
        ws.send(
            self._create_message(
                m="quote_add_symbols",
                p=[qs_token, f"{self.exchange}:{self.ticker_sym}"]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "quote_add_symbols":
        # ~m~64~m~{"m":"quote_fast_symbols","p":["qs_uIk...Rqj",
        # "NASDAQ:AAPL"]}
        ws.send(
            self._create_message(
                m="quote_fast_symbols",
                p=[qs_token, f"{self.exchange}:{self.ticker_sym}"]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "resolve_symbol":
        # ~m~140~m~{"m":"resolve_symbol","p":["cs_h2k...M0xq",
        # "sds_sym_1","={\"adjustment\":\"splits\",
        # \"currency-id\":\"USD\",\"symbol\":\"NASDAQ:AAPL\"}"]}
        ws.send(
            self._create_message(
                m="resolve_symbol",
                p=[
                    cs_token,
                    "sds_sym_1",
                    ("={"
                     + '"adjustment":"splits",'
                     + f'"currency-id":"{self.currency}",'
                     + f'"symbol":"{self.exchange}:{self.ticker_sym}"'
                     + "}")
                ]
            )
        )
        logger.debug("The message was sent.")
        # The sample message for "create_series":
        # ~m~81~m~{"m":"create_series","p":["cs_h2k...0xq",
        # "sds_1","s1","sds_sym_1","D",300,""]}
        ws.send(
            self._create_message(
                m="create_series",
                p=[
                    cs_token,
                    "sds_1",
                    "s1",
                    "sds_sym_1",
                    self.frame,
                    self.bars,
                    ""
                ]
            )
        )
        logger.debug("The message was sent.")
        logger.info("All messages were created and sent. Wait...")
        # Collect all received messages in one string raw_data and stop
        # the connection when all data is received.
        logger.debug("Start to collect the raw data.")
        raw_data = ""
        while True:
            try:
                result = ws.recv()
                raw_data += result
                logger.debug(f"The message was received: {result}")
            except websocket.WebSocketConnectionClosedException:
                logger.warning("The remote host closed the Websocket "
                               "connection or a network error happened.")
                break
        logger.info(
            "The raw data is collected and the WebSocket connection is closed."
        )
        return raw_data

    def get_pandas_data(self, raw_data: str, tz: str = "UTC") -> pd.DataFrame:
        """Gets the market data as DataFrame object.

        Converts the raw market data to the clean Pandas DataFrame
        object that includes the following columns:
            - Data and Time
            - Open price
            - High Price
            - Low Price
            - Close Price
            - Volume

        Args:
            raw_data: The raw data collected over Websocket connection.
            tz: A timezone (optional). The UTC time is used by default.
                Any time zone from pytz.all_timezones can be used. For
                example, "America/Chicago" is CME timezone.

        Returns:
            df: The clean data in Pandas DataFrame format.
                There are 6 columns:
                    - DateTime: date and time. It depends on the tz
                      argument value. The UTC time is used by default.
                    - Open: the opening price of the chosen timeframe.
                    - High: the highest price of the chosen timeframe.
                    - Low: the lowest price of the chosen timeframe.
                    - Close: the closing price of the chosen timeframe.
                    - Volume: the market volume.
                There are n rows, where n is the number of chosen bars.
        """
        # Convert the raw data to json format.
        market_data_json = self.get_json_data(raw_data)
        # Create the DataFrame with market data.
        df = pd.read_json(market_data_json)
        data = df["v"].to_list()
        columns = ["DateTime", "Open", "High", "Low", "Close", "Volume"]
        df = pd.DataFrame(data=data, columns=columns)
        # Convert the local timezone to the exchange time zone.
        df["DateTime"] = (
            pd.to_datetime(df["DateTime"], unit="s")
            .dt.tz_localize("UTC")
            .dt.tz_convert(tz)
        )
        logger.info("The dataframe market data was created.")
        return df

    @staticmethod
    def get_json_data(raw_data: str) -> str:
        """Gets the market data in json format.

        Converts the raw market data to the clean JSON string market
        data.

        Args:
            raw_data: The raw data collected over Websocket connection.

        Returns:
            market_data: The market data in JSON format.

        Raises:
            SystemExit: If the raw data is empty or has no the correct
                format.
        """
        # Choose the useful data.
        # In the raw data, we have to find the following first group
        # and use a list of dictionaries that includes the historical
        # market data:
        #
        # "s":
        # [{"i": 0, "v": [1663106400.0, 2.01, 2.05, 1.95, 1.99, 76.2]},
        #  {"i": 1, "v": [1663192800.0, 2.01, 2.03, 1.94, 1.97, 70.4]},
        #  ...........................................................
        #  {"i": 48,"v": [1668985200.0, 1.61, 1.62, 1.53, 1.56, 110.0]},
        #  {"i": 49,"v": [1669071600.0, 1.56, 1.61, 1.55, 1.60, 34.5]}]
        #
        # If the market is active we will receive additional data for
        # the last row multiple times while WebConnection is alive:
        # "s":
        # [{"i":49,"v":[1668985200.0, 1.56, 1.63, 1.55, 1.60, 39.5]}]
        # "s":
        # [{"i":49,"v":[1668985200.0, 1.58, 1.63, 1.55, 1.61, 59.7]}]
        # "s":
        # [{"i":49,"v":[1668985200.0, 1.53, 1.63, 1.54, 1.61, 53.8]}]
        # We do not use this data and collect the data from the first
        # group because it continues to change. It is better to not use
        # the last bar at all when the market is not closed, or you
        # collect the data in the middle of the week, month, etc.
        selected_data = re.search(r'"s":(\[.+?}])', raw_data)
        # r'"s":\[(.+?)}]'
        # '"s":\[(.+?)\}\]'
        # Check the raw data includes the market data.
        if selected_data is None:
            logger.error("There is no match to the regex pattern in the raw "
                         "data. Check that the raw data is not empty and has "
                         "the correct format.",
                         stack_info=True,
                         exc_info=True)
            raise SystemExit("There is no match to the regex pattern in the "
                             "raw data. Check that the raw data is not empty "
                             "and has the correct format.")
        # Get the first group and build the JSON file.
        market_data_json = selected_data.group(1)
        logger.info("The json market data was created.")
        return market_data_json

    @staticmethod
    def _generate_random_token() -> str:
        """Generates random token.

        Generates random session tokens. They are used in many messages,
        that are sent over Websocket connection.

        Returns:
            rand_token: A random 12 symbol token that consists of
                letters and numbers.
        """
        rand_token = "".join(
            random.choices(string.ascii_letters + string.digits, k=12)
        )
        logger.debug(f"The random token was generated: {rand_token}")
        return rand_token

    @staticmethod
    def _create_ws_connection() -> websocket.WebSocket:
        """Creates the websocket connection with TradingView.

        Creates the websocket connection with TradingView using wss url,
        headers.

        Returns:
            ws: Connects to wss url and returns the websocket object
                that is able to send and receive the messages.

        Raises:
            SystemExit: If there is a problem with Websocket connection.
        """
        ws_url = "wss://data.tradingview.com/socket.io/websocket"
        headers = json.dumps({"Origin": "https://data.tradingview.com"})
        try:
            ws: websocket.WebSocket = create_connection(
                url=ws_url,
                headers=headers,
            )
        except websocket.WebSocketException as e:
            logger.error(f"Problems with Websocket connection: {e}",
                         exc_info=True,
                         stack_info=True)
            raise SystemExit(f"Problems with Websocket connection: {e}") from e
        logger.debug(f"The status of connection: {ws.connected}")
        logger.info("The Websocket connection was created.")
        return ws

    @staticmethod
    def _create_message(m: str, p: List[str | int]) -> str:
        """Creates the websocket message.

        Creates the message that can be sent over Websocket.

        An example of a message:
        ~m~52~m~{"m":"quote_create_session","p":["qs_mOM...p5Y"]}

        The function gets a message name and a list of parameters,
        creates a dictionary, converts it to compact JSON, and add
        prefix ~m~{n}~m~, where {n} is a number of symbols after
        ~m~{n}~m~ including the brackets.

        Args:
            m: The message name ("set_auth_token", "create_series",
                etc.)
            p: A list of parameters (["qs_58...9dsh", 50, "D", ...])
                for every message.

        Returns:
            mes: The message that can be sent over WebSocket.
        """
        mes = json.dumps({"m": m, "p": p}, separators=(",", ":"))
        mes = f"~m~{len(mes)}~m~{mes}"
        logger.debug(f"The message was created: {mes}")
        return mes


def main() -> pd.DataFrame:
    """ Returns the market data in CSV format.

    This function:
    - Creates an instance of TvDataCollector class by using CLI
      arguments.
    - Gets the raw data over Websocket connection, cleans and
      convert it to CSV file that has the file name is similar to
      "TICKER_SYM_EXCHANGE_FRAME_DATE_TIME" (for example,
      BTC1!_CME_DAY_20221115_13_03_20)
    - Creates the fia_output folder in base folder and saves the CSV
      file inside the folder.
    - Shows in CLI interface the market historical data in DataFrame
      format.

    Returns:
        df: The market data in Pandas DataFrame format.
    """
    # Import the logger.
    from fia.utils.set_logger import set_logger
    # Import the command line interface arguments.
    from fia.cli_args import cli_args

    # Set the logger. Use the root logger to see the log messages from
    # external libraries/package too.
    set_logger("DEBUG")

    # Create an instance of TvDataCollector class.
    tvdc = TvDataCollector(cli_args.USERNAME,
                           cli_args.PASSWORD,
                           cli_args.EXCHANGE,
                           cli_args.TICKER_SYM,
                           cli_args.CURRENCY,
                           Frame[cli_args.FRAME],
                           cli_args.BARS,
                           cli_args.USER_AGENT,
                           cli_args.REMEMBER)
    # Get raw_data
    raw_data: str = tvdc.get_data()
    logger.debug(f"The rawdata finally was received: {raw_data}")
    # Get the market data in Pandas DataFrame format.
    df: pd.DataFrame = tvdc.get_pandas_data(raw_data)
    # Create path and convert DataFrame to CSV file.
    path = os.path.join(os.path.expanduser("~"), "fia_output")
    file_name = (
        f'{cli_args.TICKER_SYM}'
        f'_{cli_args.EXCHANGE}'
        f'_{cli_args.FRAME}'
        f'_{datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")}'
        f'.{"csv"}'
    )
    # TODO: add exception when convert to csv
    os.makedirs(path, exist_ok=True)
    df.to_csv(os.path.join(path, file_name), index=False)
    logger.info(f"The CSV file {file_name} was created in {path}.")
    return df


if __name__ == "__main__":
    # It will only be executed when this module is run directly.
    main()
