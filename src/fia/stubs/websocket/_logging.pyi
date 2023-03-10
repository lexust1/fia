import logging
from typing import Any

class NullHandler(logging.Handler):
    def emit(self, record: Any) -> None: ...

def enableTrace(traceable: Any, handler: Any = ..., level: str = ...) -> None: ...
def dump(title: Any, message: Any) -> None: ...
def error(msg: Any) -> None: ...
def warning(msg: Any) -> None: ...
def debug(msg: Any) -> None: ...
def trace(msg: Any) -> None: ...
def isEnabledForError(): ...
def isEnabledForDebug(): ...
def isEnabledForTrace(): ...
