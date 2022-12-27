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

# DISCLAIMER
# The fia package and any results received by using the fia package
# are for informational and educational purposes only.
# You should not construe any such information or other material as
# legal, tax, investment, financial, or other advice.
# There are risks associated with investing in any securities and
# assets. Do your own research. Past performance is not a guarantee
# of future return or performance. You may gain or lose money.

""" fia (financial analyzer) package for Python.

fia (FInancial Analyzer) is a package that gets the historical market
data from TradingView over Websocket.

There are two ways how the package can be used:
    1. Over command line interface.
    2. As an imported package in Python.

The 1st method (command line interface):
    The 1st method returns only a CSV file with the historical market
    data. This file can be used by a user in other software and apps
    to analyze the data. It is designed for people who are not going
    to use Python as the main tool and need only the file with the
    historical market data.

The 2nd method (import as a Python package):
    The 2nd method is a recommended usage because it is more flexible
    and can work with other Python libraries. It can return the raw
    market data received over WebSocket, the market data in JSON
    format, and the market data as a Pandas DataFrame object. It is
    designed for people who would like to use the package with Pandas,
    Matplotlib, Numpy, and so on.

The package includes the following modules:
    - main.py: The main module of the package.
    - cli-args.py: Parses the command line interface arguments.
    - constants.py: Includes all constants and enums.

Examples:
    See a detailed explanation with examples on:
    # TODO: add link to README with documentation on Github.
"""
import logging
from logging import NullHandler

from fia.utils.set_logger import set_logger
from fia.main import TvDataCollector
from fia.constants import Frame


# The logging package recommendation to avoid "No handler found" and
# not to show the logging messages by default.
logging.getLogger(__name__).addHandler(NullHandler())
