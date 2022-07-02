import logging
from typing import Type


def log_and_raise(
    logger: logging.Logger,
    message: str,
    level: int = logging.ERROR,
    exception: Type[BaseException] = ValueError,
) -> None:
    logger.log(level, message)
    raise exception(message)


def log_and_print(
    logger: logging.Logger,
    message: str,
    level: int = logging.DEBUG,
) -> None:
    logger.log(level, message)
    print(message)
