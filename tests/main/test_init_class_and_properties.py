import pytest

from fia.main import TvDataCollector
from fia.constants import Frame


########################################################################
# Test not a string values and empty values when the class is
# instantiated for username, password, exchange, ticker_sym, currency.
@pytest.fixture(
    scope="module",
    params=[
        123,
        0,
        0.123,
        [],
        None,
        "",
        " "
    ]
)
def value(request):
    """Create a set of args."""
    return request.param


def test_init_TvDataCollector_class_with_username(value):
    """Tests the raise when the username is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username=value,
                               password="StrongPSW123#",
                               exchange="NASDAQ",
                               ticker_sym="AAPL",
                               currency="USD",
                               frame=Frame.DAY,
                               bars=50)
    expected = "The username value has to be not an empty string."
    assert exc_info.value.args[0] == expected


def test_init_TvDataCollector_class_with_password(value):
    """Tests the raise when the password is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username="GoodName",
                               password=value,
                               exchange="NASDAQ",
                               ticker_sym="AAPL",
                               currency="USD",
                               frame=Frame.DAY,
                               bars=50)
    expected = "The password value has to be not an empty string."
    assert exc_info.value.args[0] == expected


def test_init_TvDataCollector_class_with_exchange(value):
    """Tests the raise when the exchange is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username="GoodName",
                               password="StrongPSW123#",
                               exchange=value,
                               ticker_sym="AAPL",
                               currency="USD",
                               frame=Frame.DAY,
                               bars=50)
    expected = "The exchange value has to be not an empty string."
    assert exc_info.value.args[0] == expected


def test_init_TvDataCollector_class_with_ticker_sym(value):
    """Tests the raise when the ticker_sym is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username="GoodName",
                               password="StrongPSW123#",
                               exchange="NASDAQ",
                               ticker_sym=value,
                               currency="USD",
                               frame=Frame.DAY,
                               bars=50)
    expected = "The ticker_sym value has to be not an empty string."
    assert exc_info.value.args[0] == expected


def test_init_TvDataCollector_class_with_currency(value):
    """Tests the raise when the currency is not a correct string."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username="GoodName",
                               password="StrongPSW123#",
                               exchange="NASDAQ",
                               ticker_sym="AAPL",
                               currency=value,
                               frame=Frame.DAY,
                               bars=50)
    expected = "The currency value has to be not an empty string."
    assert exc_info.value.args[0] == expected


# Add test_init_TvDataCollector_class_with_frame here.
# No tests for frame because it is a Frame object and Python
# interpretation checks the incorrect values by default when the
# TvDataCollector class is instantiated (when fia is used as package,
# think about argparse!). It is similar to the case when one of the
# arguments is missed.


@pytest.mark.parametrize(
    "bars_val",
    [
        "123",
        0,
        0.123,
        [],
        None,
        "",
        -10
    ]
)
def test_init_TvDataCollector_class_with_bars(bars_val):
    """Tests the raise when the bars is not a positive integer."""
    with pytest.raises(SystemExit) as exc_info:
        tvdc = TvDataCollector(username="GoodName",
                               password="StrongPSW123#",
                               exchange="NASDAQ",
                               ticker_sym="AAPL",
                               currency="USD",
                               frame=Frame.DAY,
                               bars=bars_val)
    expected = "Check your bars value. It has to be a positive integer."
    assert exc_info.value.args[0] == expected


########################################################################
# Test TvDataCollector properties (username, password, exchange,
# ticker_sym, currency, frame, bars, user_agent, remember).
@pytest.fixture(scope="module")
def tvdc():
    """Creates the TvDataCollector instance."""
    tvdc = TvDataCollector(username="GoodName",
                           password="StrongPSW123#",
                           exchange="NASDAQ",
                           ticker_sym="AAPL",
                           currency="USD",
                           frame=Frame.DAY,
                           bars=50)
    return tvdc


def test_username_value(tvdc):
    """Tests the username value."""
    assert tvdc.username == "GoodName"


def test_protected_username_value(tvdc):
    """Tests the protected username value."""
    assert tvdc._username == "GoodName"


def test_password_value(tvdc):
    """Tests the password value."""
    assert tvdc.password == "StrongPSW123#"


def test_protected_password_value(tvdc):
    """Tests the protected password value."""
    assert tvdc._password == "StrongPSW123#"


def test_exchange_value(tvdc):
    """Tests the exchange value."""
    assert tvdc.exchange == "NASDAQ"


def test_protected_exchange_value(tvdc):
    """Tests the protected exchange value."""
    assert tvdc._exchange == "NASDAQ"


def test_ticker_sym_value(tvdc):
    """Tests the ticker_sym value."""
    assert tvdc.ticker_sym == "AAPL"


def test_protected_ticker_sym_value(tvdc):
    """Tests the protected ticker_sym value."""
    assert tvdc._ticker_sym == "AAPL"


def test_currency_value(tvdc):
    """Tests the currency value."""
    assert tvdc.currency == "USD"


def test_protected_currency_value(tvdc):
    """Tests the protected currency value."""
    assert tvdc._currency == "USD"


@pytest.mark.parametrize(
    "frame_val, expected",
    [
        (Frame.MIN1, "1"),
        (Frame.MIN5, "5"),
        (Frame.MIN15, "15"),
        (Frame.MIN30, "30"),
        (Frame.MIN45, "45"),
        (Frame.HOUR1, "1H"),
        (Frame.HOUR2, "2H"),
        (Frame.HOUR3, "3H"),
        (Frame.HOUR4, "4H"),
        (Frame.DAY, "D"),
        (Frame.WEEK, "W"),
        (Frame.MONTH, "M")
    ]
)
def test_frame(frame_val, expected):
    """Tests the frame value and the protected frame value."""
    tvdc = TvDataCollector(username="GoodName",
                           password="StrongPSW123#",
                           exchange="NASDAQ",
                           ticker_sym="AAPL",
                           currency="USD",
                           frame=frame_val,
                           bars=50)
    assert (tvdc.frame == expected and tvdc._frame == expected)


def test_bars_value(tvdc):
    """Tests the bars value."""
    assert tvdc.bars == 50


def test_protected_bars_value(tvdc):
    """Tests the protected bars value."""
    assert tvdc._bars == 50


def test_user_agent_value(tvdc):
    """Tests the user_agen value."""
    expected = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/105.0.0.0" 
                "Safari/537.36")
    assert tvdc.user_agent == expected


def test_user_protected_agent_value(tvdc):
    """Tests the protected user agent value."""
    expected = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" 
                "AppleWebKit/537.36 (KHTML, like Gecko)" 
                "Chrome/105.0.0.0" 
                "Safari/537.36")
    assert tvdc._user_agent == expected


def test_remember_value(tvdc):
    """Tests the remember value."""
    assert tvdc.remember == "on"


def test_protected_remember_value(tvdc):
    """Tests the protected remember value."""
    assert tvdc._remember == "on"