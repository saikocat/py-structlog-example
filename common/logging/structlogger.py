import logging
from typing import Iterable

import common.logging.processors
import rapidjson
import structlog
from common.logging.api import Logger


def new_logger(logger=None, processors=None, disabled_loggers=None) -> Logger:
    logger = logger if logger else default_logger()
    processors_chain = processors if processors else default_processors_chain()
    if disabled_loggers:
        disable_loggers(disabled_loggers)

    wrapped_logger = structlog.wrap_logger(
        logger=logger,
        processors=processors_chain,
        context_class=dict,
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return wrapped_logger.new()


def default_processors_chain():
    return [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        common.logging.processors.ShowModuleInfo(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(serializer=rapidjson.dumps),
    ]


def default_logger():
    import sys
    import uuid

    logger_name = "std_structlogger"
    # TODO: fix hardcode
    output_path = f"/tmp/{logger_name}-{str(uuid.uuid4())}.log"

    # Format must be empty like so for json format
    logging.basicConfig(
        format="%(message)s", level=logging.INFO, stream=sys.stdout,
    )
    logger = logging.getLogger(logger_name)
    logger.addHandler(logging.FileHandler(output_path))
    return logger


def disable_loggers(disabled: Iterable[str]):
    for logger in disabled:
        log = logging.getLogger(logger)
        log.setLevel(logging.ERROR)
        log.disabled = True
