import websocket

from ._abnf import *
from ._exceptions import *
from ._handshake import *
from ._http import *
from ._logging import *
from ._socket import *
from ._ssl_compat import *
from ._utils import *
from typing import Any, Optional

class WebSocket:
    sock_opt: Any = ...
    handshake_response: Any = ...
    sock: Any = ...
    connected: bool = ...
    get_mask_key: Any = ...
    frame_buffer: Any = ...
    cont_frame: Any = ...
    lock: Any = ...
    readlock: Any = ...
    def __init__(self, get_mask_key: Optional[Any] = ..., sockopt: Optional[Any] = ..., sslopt: Optional[Any] = ..., fire_cont_frame: bool = ..., enable_multithread: bool = ..., skip_utf8_validation: bool = ..., **_: Any) -> None: ...
    def __iter__(self) -> Any: ...
    def __next__(self): ...
    def next(self): ...
    def fileno(self): ...
    def set_mask_key(self, func: Any) -> None: ...
    def gettimeout(self): ...
    def settimeout(self, timeout: Any) -> None: ...
    timeout: Any = ...
    def getsubprotocol(self): ...
    subprotocol: Any = ...
    def getstatus(self): ...
    status: Any = ...
    def getheaders(self): ...
    def is_ssl(self): ...
    headers: Any = ...
    def connect(self, url: Any, **options: Any) -> None: ...
    def send(self, payload: Any, opcode: Any = ...): ...
    def send_frame(self, frame: Any): ...
    def send_binary(self, payload: Any): ...
    def ping(self, payload: str = ...) -> None: ...
    def pong(self, payload: str = ...) -> None: ...
    def recv(self): ...
    def recv_data(self, control_frame: bool = ...): ...
    def recv_data_frame(self, control_frame: bool = ...): ...
    def recv_frame(self): ...
    def send_close(self, status: Any = ..., reason: bytes = ...) -> None: ...
    def close(self, status: Any = ..., reason: bytes = ..., timeout: int = ...) -> None: ...
    def abort(self) -> None: ...
    def shutdown(self) -> None: ...

def create_connection(url: str, timeout: Optional[Any] = ..., class_: Any = ..., **options: Any) -> websocket.WebSocket: ...
