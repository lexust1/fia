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
"""The module includes constants and enums for TvDataCollector class.

This module is a part of the fia package and should not be used
separately.
"""
from enum import Enum
from typing import Final


# Enum of acceptable bar timeframes of TvDataCollector class.
class Frame(Enum):
    """Enum class for timeframes."""
    MIN1 = "1"
    MIN5 = "5"
    MIN15 = "15"
    MIN30 = "30"
    MIN45 = "45"
    HOUR1 = "1H"
    HOUR2 = "2H"
    HOUR3 = "3H"
    HOUR4 = "4H"
    DAY = "D"
    WEEK = "W"
    MONTH = "M"


# User agent used during authorization on TradingView.
USER_AGENT: Final[str] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                          "AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/105.0.0.0"
                          "Safari/537.36")
# Remember the user or not ("on"/"off")
REMEMBER: Final[str] = "on"
