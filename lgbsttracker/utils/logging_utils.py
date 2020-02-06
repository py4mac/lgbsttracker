from __future__ import print_function

import logging
import logging.config

# Logging format example:
# 2018/11/20 12:36:37 INFO lgbsttracker.event.kafka: Creating Kafka Event
LOGGING_LINE_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"
LOGGING_DATETIME_FORMAT = "%Y/%m/%d %H:%M:%S"


def _configure_lgbsttracker_loggers(root_module_name, debug_level="INFO", app_name="app"):
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "lgbsttracker_formatter": {"format": LOGGING_LINE_FORMAT, "datefmt": LOGGING_DATETIME_FORMAT}
            },
            "handlers": {
                "console_handler": {
                    "level": "DEBUG",
                    "formatter": "lgbsttracker_formatter",
                    "class": "logging.StreamHandler",
                },
                "log_file_handler": {
                    "level": "DEBUG",
                    "formatter": "lgbsttracker_formatter",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": f"{app_name}.log",
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8",
                },
                "error_file_handler": {
                    "level": "ERROR",
                    "formatter": "lgbsttracker_formatter",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": f"{app_name}-error.log",
                    "maxBytes": 10485760,
                    "backupCount": 20,
                    "encoding": "utf8",
                },
            },
            "loggers": {
                root_module_name: {
                    "handlers": ["console_handler", "log_file_handler", "error_file_handler"],
                    "level": debug_level,
                    "propagate": False,
                }
            },
        }
    )
