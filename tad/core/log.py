import copy
import logging
import logging.config
from typing import Any

from tad.core.types import LoggingLevelType

LOGGING_SIZE = 10 * 1024 * 1024
LOGGING_BACKUP_COUNT = 5

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "generic": {
            "()": "logging.Formatter",
            "style": "{",
            "fmt": "{asctime}({levelname},{name}): {message}",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
        }
    },
    "handlers": {
        "console": {"formatter": "generic", "class": "logging.StreamHandler", "stream": "ext://sys.stdout"},
        "file": {
            "formatter": "generic",
            "()": "logging.handlers.RotatingFileHandler",
            "filename": "tad.log",
            "maxBytes": LOGGING_SIZE,
            "backupCount": LOGGING_BACKUP_COUNT,
        },
    },
    "loggers": {
        "tad": {"handlers": ["console", "file"], "level": "DEBUG", "propagate": True},
    },
}


def configure_logging(level: LoggingLevelType = "INFO", config: dict[str, Any] | None = None) -> None:
    log_config = copy.deepcopy(LOGGING_CONFIG)

    if config:
        log_config.update(config)

    logging.config.dictConfig(log_config)

    logger = logging.getLogger("tad")

    logger.setLevel(level)
