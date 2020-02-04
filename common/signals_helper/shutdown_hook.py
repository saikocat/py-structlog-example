import signal
from types import FrameType
from typing import Callable, Iterable

SHUTDOWN_SIGNALS = [
    signal.SIGINT,
    signal.SIGQUIT,
    signal.SIGTERM,
]

SignalHandler = Iterable[Callable[[signal.Signals, FrameType], None]]


def register_shutdown_handler(handlers: SignalHandler):
    def final_handler(signum, frame):
        for handler in handlers:
            handler(signum, frame)
        raise(SystemExit)

    for signum in SHUTDOWN_SIGNALS:
        signal.signal(signum, final_handler)
