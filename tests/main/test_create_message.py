import pytest
import random
import re
import string

from fia.main import TvDataCollector


@pytest.fixture(
    scope="module",
    params=[
        (
            "set_auth_token",
            ["eyJ...9U0"],
            '~m~40~m~{"m":"set_auth_token","p":["eyJ...9U0"]}'
        ),
        (
            "chart_create_session",
            ["cs_Lms...eEc", ""],
            '~m~52~m~{"m":"chart_create_session","p":["cs_Lms...eEc",""]}'
        ),
        (
            "quote_create_session",
            ["qs_uiL...eMb", ""],
            '~m~52~m~{"m":"quote_create_session","p":["qs_uiL...eMb",""]}'
        ),
        (
            "quote_set_fields",
            ["qs_Lms...eEc", "ch", "...", "chp"],
            '~m~62~m~{"m":"quote_set_fields","p":["qs_Lms...eEc","ch","...","chp"]}'
        ),
        (
            "quote_add_symbols",
            ["qs_Lms...eEc", "NASDAQ:AAPL"],
            '~m~60~m~{"m":"quote_add_symbols","p":["qs_Lms...eEc","NASDAQ:AAPL"]}'
        ),
        (
            "quote_fast_symbols",
            ["qs_Lms...eEc", "NASDAQ:AAPL"],
            '~m~61~m~{"m":"quote_fast_symbols","p":["qs_Lms...eEc","NASDAQ:AAPL"]}'
        ),
        (
            "resolve_symbol",
            ["cs_Lms...eEc", "sds_sym_1", '={"adj...AAPL"}'],
            r'~m~75~m~{"m":"resolve_symbol","p":["cs_Lms...eEc","sds_sym_1","={\"adj...AAPL\"}"]}'
        ),
        (
            "create_series",
            ["cs_Lms...eEc", "sds_1", "...", 50],
            '~m~59~m~{"m":"create_series","p":["cs_Lms...eEc","sds_1","...",50]}'
        )
    ]
)
def values(request):
    """Creates a set of args for the function."""
    return request.param


def test_message_returned_value(values):
    """Tests the values of the returned message."""
    mes = TvDataCollector._create_message(values[0], values[1])
    expected = values[2]
    assert mes == expected


def test_message_type():
    """Tests the type of the returned message."""
    mes = TvDataCollector._create_message(
        "message",
        ["param1", "param2"]
    )
    assert isinstance(mes, str)


@pytest.mark.parametrize("k", [0, 10, 100, 1000])
def test_message_prefix(k):
    """Tests the prefix of the message."""
    mes = TvDataCollector._create_message(
        "".join(random.choices(string.ascii_letters + string.digits, k=k)),
        ["".join(random.choices(string.ascii_letters + string.digits, k=k))]
    )
    assert re.match("^~m~[0-9]*~m~", mes) is not None

