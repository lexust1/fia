import argparse
import importlib
import os
import pytest
import sys
from unittest import mock


# We do not have to set all args. Some args have the default values.
# The are 3 typical cases. For every case, we create fixtures.
# Create lif of args.
@pytest.fixture
def min_args_list():
    """Returns the minimal list of args."""
    return [
        "prog",  # for argparse, the first element is a program name
        "-e", "NASDAQ",
        "-t", "AAPL",
        "-c", "USD",
        "-f", "DAY",
        "-b", "50"
    ]


@pytest.fixture
def mid_args_list():
    """Returns the middle list of args."""
    return [
        "prog",
        "-u", "GoodName",
        "-p", "StrongPSW123#",
        "-e", "NASDAQ",
        "-t", "AAPL",
        "-c", "USD",
        "-f", "DAY",
        "-b", "50"
    ]


@pytest.fixture
def max_args_list():
    """Returns the maximal list of args."""
    return [
        "prog",
        "-u", "GoodName",
        "-p", "StrongPSW123#",
        "-e", "NASDAQ",
        "-t", "AAPL",
        "-c", "USD",
        "-f", "DAY",
        "-b", "50",
        "-a", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
              "AppleWebKit/537.36 (KHTML, like Gecko)"
              "Chrome/105.0.0.0"
              "Safari/537.36",
        "-r", "on"
    ]


# Create fixture for 3 cases (set environmental variables by using
# monkeypatch and mock sys.argv by using mock.patch.object.
@pytest.fixture
def cli_args_min(monkeypatch, min_args_list):
    """Returns argparse.Namespace for the minimal list of args."""
    monkeypatch.setenv("TV_USERNAME", "GoodName")
    monkeypatch.setenv("TV_PASSWORD", "StrongPSW123#")
    with mock.patch.object(sys, "argv", min_args_list):
        # print("Mock sys.argv:", sys.argv, "\n")
        from fia.cli_args import cli_args
        # print(cli_args)
    return cli_args


@pytest.fixture
def cli_args_mid(monkeypatch, mid_args_list):
    """Returns argparse.Namespace for the middle list of args."""
    with mock.patch.object(sys, "argv", mid_args_list):
        # print("Mock sys.argv:", sys.argv, "\n")
        # Force to reload fia.cli_args to set new Namespace
        importlib.reload(sys.modules["fia.cli_args"])
        from fia.cli_args import cli_args
        # print(cli_args)
    return cli_args


@pytest.fixture
def cli_args_max(monkeypatch, max_args_list):
    """Returns argparse.Namespace for the maximal list of args."""
    with mock.patch.object(sys, "argv", max_args_list):
        # print("Mock sys.argv:", sys.argv, "\n")
        importlib.reload(sys.modules["fia.cli_args"])
        from fia.cli_args import cli_args
        # print(cli_args)
    return cli_args


# Generate tests.
def pytest_generate_tests(metafunc):
    """Generates tests for all 3 fixtures (max, mid, min)."""
    if "cli_args" in metafunc.fixturenames:
        metafunc.parametrize(
            "cli_args",
            ["cli_args_min", "cli_args_mid", "cli_args_max"]
        )


def test_returned_type(cli_args, request):
    """Tests that the returned data is Namespace."""
    cli_args = request.getfixturevalue(cli_args)
    assert isinstance(cli_args, argparse.Namespace)


def test_arg_parse_values(cli_args, request):
    """Tests all argparse values."""
    cli_args = request.getfixturevalue(cli_args)
    actual = [cli_args.USERNAME,
              cli_args.PASSWORD,
              cli_args.EXCHANGE,
              cli_args.TICKER_SYM,
              cli_args.CURRENCY,
              cli_args.FRAME,
              cli_args.BARS,
              cli_args.USER_AGENT,
              cli_args.REMEMBER
              ]
    expected = ["GoodName",
                "StrongPSW123#",
                "NASDAQ",
                "AAPL",
                "USD",
                "DAY",
                50,
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                "AppleWebKit/537.36 (KHTML, like Gecko)"
                "Chrome/105.0.0.0"
                "Safari/537.36",
                "on"]
    assert actual == expected


@pytest.mark.parametrize(
    "args",
    [
        [
            "prog",
            "-u", "GoodName",
            "-e", "NASDAQ",
            "-t", "AAPL",
            "-c", "USD",
            "-f", "DAY",
            "-b", "50"
        ],
        [
            "prog",
            "-p", "StrongPSW123#",
            "-e", "NASDAQ",
            "-t", "AAPL",
            "-c", "USD",
            "-f", "DAY",
            "-b", "50"
        ],
        [
            "prog",
            "-e", "NASDAQ",
            "-t", "AAPL",
            "-c", "USD",
            "-f", "DAY",
            "-b", "50"
        ]
    ],
    ids=[
        "username_is_None",
        "password_is_None",
        "user_and_password_is_None"
    ]
)
def test_arg_parse_raises(monkeypatch, args):
    """Tests the raise when username or/and password is None."""
    monkeypatch.delenv("TV_USERNAME", raising=False)
    monkeypatch.delenv("TV_PASSWORD", raising=False)
    with mock.patch.object(sys, "argv", args):
        # print("Mock sys.argv:", sys.argv, "\n")
        expected = ("You have to set up USERNAME OR/AND PASSWORD over command "
                    "line interface or add environment variables.")
        with pytest.raises(SystemExit) as exc_info:
            importlib.reload(sys.modules["fia.cli_args"])
            from fia.cli_args import cli_args
            # print(cli_args)
        assert exc_info.value.args[0] == expected





