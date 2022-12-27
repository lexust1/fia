# pip install pytest-repeat for using @pytest.mark_repeat(10)
import pytest
import re

from fia.main import TvDataCollector


@pytest.fixture(scope="module")
def rand_token():
    """Generates a random token."""
    rand_token = TvDataCollector._generate_random_token()
    return rand_token


def test_rand_token_length(rand_token):
    """Tests the length of the random token."""
    assert len(rand_token) == 12


def test_rand_token_type(rand_token):
    """Tests the type of the random token."""
    assert isinstance(rand_token, str)


@pytest.mark.repeat(10)
def test_rand_token_from_letters_and_digits(rand_token):
    """Tests that the random token includes letters and digits only."""
    res = re.match(r"^[A-Za-z0-9]*$", rand_token).span()[1]
    assert res == 12
