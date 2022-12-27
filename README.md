# FInancial Analyzer (fia)


## Overview
**fia** (FInancial Analyzer) is a package that gets the historical market
data from multiple resources such as TradingView, Alphavantage, etc. 

The package collects the data from TradingView over WebSocket. In the future,
other options and resources will be added.


## Installation
The source code is hosted on [GitHub](https://github.com/lexust1/fia).

Binary installers are available on [PyPI](https://pypi.org/project/) 
and [Conda](https://docs.conda.io/).

Before the package installation, it is recommended to create a new virtual
environment by conda, virtualenv, poetry, and so on.

The dependencies are listed in [pyproject.toml](https://github.com/lexust1) 
in the dependencies section.

To install the package use the following commands in Terminal:

- For PyPI:
    ```shell
    pip install fia
    ```
- For Conda:
    ```shell
    conda install fia
    ```

## The simplest working example
```python
from fia import Frame, set_logger, TvDataCollector  

# Set the logger to see the INFO messages.
set_logger("INFO")
# Create an instance of the TvDataCollector class.
tvdc = TvDataCollector(username="Red69", 
                       password="fhEnv@*re37",
                       exchange="NASDAQ",
                       ticker_sym="AAPL",
                       currency="USD",
                       frame=Frame.MIN15,
                       bars=50)
# Get the raw data including the historical market data.
raw_data = tvdc.get_data()
# Get the clean historical market data as DataFrame object.
df = tvdc.get_pandas_data(raw_data, tz="America/Chicago")
```
See the detailed explanation below in the Usage section.

## Usage
There are two ways how the package can be used:
1. Over command line interface.
2. As an imported package in Python (recommended method).

### The 1st method (command line interface):
The 1st method returns only a CSV file with the historical market 
data. This file can be used by a user in other software and apps 
to analyze the data. It is designed for people who are not going 
to use Python as the main tool and need only the file with the 
historical market data.

#### Method 1.1 (CLI + environment variables):
1. Go to the project directory and create setenv.sh
2. Add the following lines in the file:
    ```shell
    export TV_USERNAME="USERNAME"
    export TV_PASSWORD="PASSWORD"
    ```
    where:
    - "USERNAME" is a TradingView username (not to be confused with email).
    - "PASSWORD" is a TradingView password.
    
    For example:
    ```shell
    export TV_USERNAME="Red69"
    export TV_PASSWORD="fhEnv@*re37"
    ```
3. From Terminal export the environment variables:
    ``` shell
    . ./setenv.sh
    ```
 4. Type the command in Terminal:
    ```shell
    fia -e exchange -t ticker_sym -c currency -f frame -b bars
    ```    
    where:
    - exchange is an exchange (NYSE, CME, etc.).
    - ticker_sym is a ticker symbol (AAPL, BTC, etc.)
    - currency is a currency (USD, EUR, etc.).
    - frame is a bar timeframe. Use one of the following options: 
      - MIN1 - 1 min, 
      - MIN5 - 5 min, 
      - MIN15 - 15 min, 
      - MIN30 - 30 min, 
      - MIN45 - 45 min, 
      - HOUR1 - 1 hr, 
      - HOUR2 - 2 hr, 
      - HOUR3 - 3 hr, 
      - HOUR4 - 4 hr, 
      - DAY - day, 
      - WEEK - week,
      - MONTH - month.
    - bars is a number of bars (the limit depends on the Tradingview plan and 
      the ticker symbol).
    - user_agent is a user agent (optional), use the **-a** flag if you would like 
      to change the default value.
    - remember is a status (optional), "on" - remember the user, use the **-r** flag
      if you would like to change the default value.     
    
    For example:
    ```shell
    fia -e NASDAQ -t AAPL -c USD -f DAY -b 50
    ```
5.  It creates a CSV file that has the file name is similar to 
    "TICKER_SYM_FRAME_DATE_TIME" (for example, AAPL_NASDAQ_DAY_20221123_10_21_49) 
    and saves it in the fia_output folder.
    The fia_output folder is created in your home (~, $HOME, etc.) folder.
    
    An example of output CSV file:
    ```csv
    DateTime,Open,High,Low,Close,Volume
    2022-09-15 08:30:00-05:00,154.65,155.24,151.38,152.37,90481110.0
    2022-09-16 08:30:00-05:00,151.21,151.35,148.37,150.7,162278841.0
    .................................................................
    2022-11-22 08:30:00-06:00,148.13,150.42,146.925,150.18,51804132.0
    2022-11-23 08:30:00-06:00,149.45,151.83,149.34,151.07,58301395.0
    ```
      There are 6 values in every row separated by comma:
     - DateTime: date and time. The UTC timezone is used.
     - Open: the opening price of the chosen timeframe.
     - High: the highest price of the chosen timeframe.
     - Low: the lowest price of the chosen timeframe.
     - Close: the closing price of the chosen timeframe.
     - Volume: the market volume.     
     
    The values usually are in USD but check the currency and the unit of measure on 
     the exchange.

6. Add setenv.sh in the .gitignore file for security reasons if you are going to
   create a repository on a platform is similar to GitHub.

#### Method 1.2 (CLI + explicit username and password):
This method is not recommended because it is not secure. It is better to use
the environment variables to keep your username and password as it was described
above in Method 1.1.

Type the command in Terminal:
```shell
fia -u username -p password -e exchange -t ticker_sym -c currency -f frame -b bars
```    
where:
- username is a TradingView username (not to be confused with email).
- password is a TradingView password.
- exchange is an exchange (NYSE, CME, etc.).
- ticker_sym is a ticker symbol (AAPL, BTC, etc.)
- currency is a currency (USD, EUR, etc.).
- frame is a bar timeframe. Use one of the following options: 
  - MIN1 - 1 min, 
  - MIN5 - 5 min, 
  - MIN15 - 15 min, 
  - MIN30 - 30 min, 
  - MIN45 - 45 min, 
  - HOUR1 - 1 hr, 
  - HOUR2 - 2 hr, 
  - HOUR3 - 3 hr, 
  - HOUR4 - 4 hr, 
  - DAY - day, 
  - WEEK - week,
  - MONTH - month.
- bars is a number of bars (the limit depends on the Tradingview plan and the 
  ticker symbol).
- user_agent is a user agent (optional), use the **-a** flag if you would like 
  to change the default value.
- remember is a status (optional), "on" - remember the user, use the **-r** flag
  if you would like to change the default value.
    
For example:
  ```shell
  fia -u Red69 -p fhEnv@*re37 -e NASDAQ -t AAPL -c USD -f DAY -b 50
  ```


### The 2nd method (import as a Python package):
The 2nd method is a recommended usage because it is more flexible 
and can work with other Python libraries. 

It can return: 
- the raw market data received over WebSocket, 
- the market data in JSON format,
- the market data as a Pandas DataFrame object. 

It is designed for people who would like to use the package with Pandas, 
Matplotlib, JupyterLab, etc.

#### Method 2.1 (import + environment variables):
1. Go to the project directory and create setenv.sh
2. Add the following lines in the file:
    ```shell
    export TV_USERNAME="USERNAME"
    export TV_PASSWORD="PASSWORD"
    ```
    where:
    - "USERNAME" is a TradingView username (not to be confused with email).
    - "PASSWORD" is a TradingView password.
    
    For example:
    ```shell
    export TV_USERNAME="Red69"
    export TV_PASSWORD="fhEnv@*re37"
    ```
3. From Terminal export the environment variables:
    ``` shell
    . ./setenv.sh
    ```
4. Create a python file and get the historical market data:
    ```python
    import os
    # Import the fia package the TvDataCollector class and the Frame enum.
    from fia import Frame, TvDataCollector
    
      
    # Create an instance of the TvDataCollector class.
    tvdc = TvDataCollector(username=os.environ.get("TV_USERNAME"),
                           password=os.environ.get("TV_PASSWORD"),
                           exchange="NASDAQ", 
                           ticker_sym="AAPL",
                           currency="USD",
                           frame=Frame.MIN15,
                           bars=50)
    # Get the raw data including the historical market data.
    raw_data = tvdc.get_data()
    # Get the clean historical market data as DataFrame object.
    df = tvdc.get_pandas_data(raw_data)
    ```    
The TvDataCollector class gets the historical market data from TradingView and
has the following attributes:
- username is a TradingView username (not to be confused with email).
- password is a TradingView password.
- exchange is an exchange (NYSE, CME, etc.).
- ticker_sym is a ticker symbol (AAPL, BTC, etc.)
- currency is a currency (USD, EUR, etc.).
- frame is a bar timeframe as a member of enum Frame. Use one of the following 
  options: 
  - Frame.MIN1 - 1 min, 
  - Frame.MIN5 - 5 min, 
  - Frame.MIN15 - 15 min, 
  - Frame.MIN30 - 30 min, 
  - Frame.MIN45 - 45 min, 
  - Frame.HOUR1 - 1 hr, 
  - Frame.HOUR2 - 2 hr, 
  - Frame.HOUR3 - 3 hr, 
  - Frame.HOUR4 - 4 hr, 
  - Frame.DAY - day, 
  - Frame.WEEK - week,
  - Frame.MONTH - month.
- bars is a number of bars (the limit depends on the Tradingview plan and the 
  ticker symbol).
- user_agent is a user agent (optional), use the **-a** flag if you would like 
  to change the default value.
- remember is a status (optional), "on" - remember the user, use the **-r** flag
  if you would like to change the default value.

The TvDataCollector has the following public methods:
- get_auth_token(): Gets the authorization token.
    The following code
    ```python
    # tvdc is an instance of the TvDataCollector class.
    tvdc.get_auth_token()
    ```
    returns the authorization token generated for your username on TradingView 
    when you sign in.
- get_data(): Gets the raw data over Websocket.   
    The following code
    ```python
    # tvdc is an instance of the TvDataCollector class.
    tvdc.get_data()
    ```
    returns the raw data including the historical market data.
    
    It includes all sent and received messages over WebSocket. It can be useful
    if you would like to parse the raw data and use what you need for your goals. 
- get_pandas_data(raw_data, tz): Gets the market data as Pandas DataFrame from the raw 
  data. The tz argument is optional. The UTC time is used by default. Any time zone 
  from pytz.all_timezones (see the python library pytz) can be used. For  example, 
  "America/Chicago" is CME timezone.

  The following code
    ```python
    # tvdc is an instance of the TvDataCollector class.
    # raw_data is received by using tvdc.get_data().
    tvdc.get_pandas_data(raw_data)
    ```
    returns the DataFrame object:

| DateTime                  | Open    | High   | Low      | Close  | Volume     |
|---------------------------|---------|--------|----------|--------|------------|
| 2022-09-14 13:30:00+00:00 | 154.785 | 157.1  | 153.6106 | 155.31 | 87965409.0 |
| 2022-09-15 13:30:00+00:00 | 154.65  | 155.24 | 151.38   | 152.37 | 90481110.0 |
| …                         | …       | …      | …        | …      | …          |
| 2022-11-21 14:30:00+00:00 | 150.16  | 150.37 | 147.715  | 148.01 | 58724070.0 |
| 2022-11-22 14:30:00+00:00 | 148.13  | 150.42 | 146.925  | 150.18 | 51804132.0 |
   
  There are 6 columns:
  - DateTime: date and time. It depends on the tz argument value in get_pandas_data().
    The UTC time is used by default.
  - Open: the opening price of the chosen timeframe.
  - High: the highest price of the chosen timeframe.
  - Low: the lowest price of the chosen timeframe.
  - Close: the closing price of the chosen timeframe.
  - Volume: the market volume.     
  The values usually are in USD but check the currency and the unit of measure on 
  the exchange.
  If you would like to change the timezone see the following example:
    ```python
    # tvdc is an instance of the TvDataCollector class.
    # raw_data is received by using tvdc.get_data().
    # "America/Chicago" is a timezone. Any time zone from pytz.all_timezones 
    # (see the python library pytz) can be used.
    tvdc.get_pandas_data(raw_data, "America/Chicago")
    ```

- get_json_data(raw_data): Gets the market data in JSON format from the raw data.
    The following code
    ```python
    # tvdc is an instance of the TvDataCollector class.
    # raw_data is received by using tvdc.get_data().
    tvdc.get_json_data(raw_data)
    ```
    returns the data in JSON format.
   
5. Add setenv.sh in the .gitignore file for security reasons if you are going to
   create a repository on a platform is similar to GitHub.

#### Method 2.2 (import + explicit username and password):
This method is not recommended because it is not secure. It is better to use
the environment variables to keep your username and password as it was described
above in Method 2.1.

Create a python file and get the historical market data:
```python
# Import the fia package the TvDataCollector class and the Frame enum.
from fia import Frame, TvDataCollector
    
      
# Create an instance of the TvDataCollector class.
tvdc = TvDataCollector(username="Red69",
                       password="fhEnv@*re37",
                       exchange="NASDAQ", 
                       ticker_sym="AAPL",
                       currency="USD",
                       frame=Frame.MIN15,
                       bars=50)
# Get the raw data including the historical market data.
raw_data = tvdc.get_data()
# Get the clean historical market data as DataFrame object.
df = tvdc.get_pandas_data(raw_data)
```    
The attributes and methods are described in Method 2.1. The only difference is
that we assign the explicit username and password rather than using os.environ.get()
to get them from the environment variables.

## Logging

1. When the package is used over command line interface the root logger
   is set by default and shows the info messages.

2. When the package is imported the root logger is not set. It prevents
   collisions with the logging system of the program where the package
   was imported.
    
    There are several ways how to set the logger:
    - Use the set_logger() function that sets the root logger and helps to choose
      the level of log messages:
      ```python
      # import functions set_logger()
      from fia import set_logger
      
      
      # Set status: "INFO", "DEBUG", "WARNING", etc.
      set_logger("INFO")
      ```
    - Set the root logger manually.
      ```python
      import logging
      import sys
                              
      
      # Get the root logger.
      logger = logging.getLogger()
      # Set the level of messages for the logger.
      logger.setLevel(logging.DEBUG)
      # Set the log message style.
      formatter = logging.Formatter(
          "{asctime} | {name} | {levelname} | {message}", style="{"
      )
      # Set and attach the handler.
      handler = logging.StreamHandler(sys.stdout)
      handler.setLevel(logging.DEBUG)
      handler.setFormatter(formatter)
      logger.addHandler(handler) 
      ```
    - Set the package logger manually.
      ```python
      import logging
      import sys
      
                          
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
      handler.setLevel(logging.DEBUG)
      handler.setFormatter(formatter)
      logger.addHandler(handler) 
      ```
    Choose the most suitable method for your case.

## Important notes
You should treat the historical data accurately especially the last bar. 

For example, when you use the day timeframe, the last bar represents the actual prices
and volume for the current day. If the market is active the prices and volume keep 
changing.

A similar situation occurs when you try to retrieve the data in the middle of 
the week, month, etc. 

## License
[Apache 2.0](https://github.com/lexust1)

## Disclaimer
The fia package and any results received by using the fia package
are for informational and educational purposes only.
You should not construe any such information or other material as
legal, tax, investment, financial, or other advice.
There are risks associated with investing in any securities and
assets. Do your own research. Past performance is not a guarantee
of future return or performance. You may gain or lose money.