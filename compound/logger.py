import logging


def get_logger(
    name: str = __name__,
    filename: str = 'compound.log',
    log_level: int = logging.DEBUG,
    log_format: str = '%(asctime)s [%(levelname)s] {%(name)s}: %(message)s',
) -> logging.Logger:
    logger = logging.getLogger(name)
    formatter = logging.Formatter(log_format)
    handler = logging.FileHandler(filename)

    logger.setLevel(log_level)
    handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(handler)

    return logger
