# Use . ./setenv.sh before testing.
import pytest
import subprocess


@pytest.mark.slow
def test_as_cli_app():
    """Tests the package as command line interface app."""
    df = subprocess.run(
        [
            "fia",
            "-e", "NASDAQ",
            "-t", "AAPL",
            "-c", "USD",
            "-f", "DAY",
            "-b", "50"
        ],
        text=True,
        capture_output=True
        # stderr=subprocess.STDOUT,
        # stdout=subprocess.PIPE
    )
    # print(df.stdout)
    assert ".csv was created in" in df.stdout
