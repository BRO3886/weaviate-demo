import logging
from typing import Dict

from app.config import get_config

_loggers: Dict[str, logging.Logger] = {}


def get_logger(
    name: str = "app",
) -> logging.Logger:
    global _loggers

    config = get_config()
    level: int = config.get("logging.level", logging.DEBUG)
    log_format: str = config.get(
        "logging.format", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    date_format: str = config.get("logging.datefmt", "%Y-%m-%d %H:%M:%S")

    if name in _loggers:
        return _loggers[name]
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(log_format, datefmt=date_format)

    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    _loggers[name] = logger
    return logger
