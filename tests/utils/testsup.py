# from fia.utils.create_property import create_property
#
#
# class TestProperty:
#     def __init__(self, username: str) -> None:
#         self.username = username
#     username = create_property("username")
#
#
# test_property = TestProperty("LogIn")
#
# print(TestProperty.__dict__, "\n")
# print(test_property.__dict__)

##############
# # The sample message for "resolve_symbol":
# print(
# '~m~140~m~{"m":"resolve_symbol","p":["cs_h2k...M0xq","sds_sym_1","={\"adjustment\":\"splits\",\"currency-id\":\"USD\",\"symbol\":\"NASDAQ:AAPL\"}"]}'
# )
# print("/n")
# print(
# r'~m~140~m~{"m":"resolve_symbol","p":["cs_h2k...M0xq","sds_sym_1","={\"adjustment\":\"splits\",\"currency-id\":\"USD\",\"symbol\":\"NASDAQ:AAPL\"}"]}'
# )
# print("/n")
# print(
# '~m~140~m~{"m":"resolve_symbol","p":["cs_h2k...M0xq","sds_sym_1","={"adjustment":"splits","currency-id":"USD","symbol":"NASDAQ:AAPL"}"]}'
# )

####
# currency = "USD"
# exchange = "NASDAQ"
# ticker_sym = "AAPL"
# new_str = (
#  "={"
#  + '"adjustment":"splits",'
#  + f'"currency-id":"{currency}",'
#  + f'"symbol":"{exchange}:{ticker_sym}"'
#  + "}"
# )
# print(
#     new_str
# )

###

# def good_func(el1, el2):
#     sum_els = el1 + el2
#     return sum_els
#
#
# sum1 = good_func(10, 15)
# print(sum1, "\n")
#
# el3 = 100
# el4 = 150
#
#
# def good_func_no_args():
#     sum_els = el3 + el4
#     return sum_els
#
#
# sum2 = good_func_no_args()
# print(sum2, "\n")

####
from enum import Enum


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

print("It is Frame:", Frame, "\n")
print("It is Frame.DAY:", Frame.DAY, "\n")
print("It is Frame.__members__:", Frame.__members__, "\n")
print("It is list(Frame):", list(Frame), "\n")
print("It is Frame[\"DAY\"]:", Frame["DAY"], "\n")

We input in CLI as DAY
argparse reads it as "DAY" and remembers that cli_args.FRAME returns "DAY"
So Frame[cli_args.FRAME] is equal Frame["DAY"] and returns Frame.DAY
TvDataCollector Class is waitino for Frame.DAY

CLI => DAY
cli_args.FRAME => "DAY"
Frame[cli_args.FRAME] = Frame["DAY"] => Frame.DAY
Frame.DAY goes into TvDataCollector class.