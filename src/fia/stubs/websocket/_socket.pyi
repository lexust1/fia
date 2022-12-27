from ._exceptions import *
from ._ssl_compat import *
from ._utils import *
from typing import Any

DEFAULT_SOCKET_OPTION: Any

class sock_opt:
    sockopt: Any = ...
    sslopt: Any = ...
    timeout: Any = ...
    def __init__(self, sockopt: Any, sslopt: Any) -> None: ...

def setdefaulttimeout(timeout: Any) -> None: ...
def getdefaulttimeout(): ...
def recv(sock: Any, bufsize: Any): ...
def recv_line(sock: Any): ...
def send(sock: Any, data: Any): ...