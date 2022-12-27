from ._exceptions import *
from ._logging import *
from ._socket import *
from ._ssl_compat import *
from ._url import *
from python_socks._errors import *  # type: ignore
from typing import Any

class ProxyError(Exception): ...
class ProxyTimeoutError(Exception): ...
class ProxyConnectionError(Exception): ...

class proxy_info:
    proxy_host: Any = ...
    proxy_port: Any = ...
    auth: Any = ...
    no_proxy: Any = ...
    proxy_protocol: Any = ...
    proxy_timeout: Any = ...
    def __init__(self, **options: Any) -> None: ...

def connect(url: Any, options: Any, proxy: Any, socket: Any): ...
def read_headers(sock: Any): ...