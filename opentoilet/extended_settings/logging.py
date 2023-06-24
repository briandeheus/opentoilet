import os

LOG_HANDLER = os.environ.get("LOG_HANDLER", "console")
LOG_FORMATTER = os.environ.get("LOG_FORMATTER", "verbose")
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "opentoilet.utils.json_formatter.JSONFormatter",
            "service": os.environ.get("SERVICE_NAME", "opentoilet"),
            "environment": os.environ.get("ENV", "opentoilet"),
        },
        "verbose": {"format": "[%(asctime)s] %(levelname)s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": LOG_FORMATTER},
    },
    "loggers": {
        "": {
            "handlers": [LOG_HANDLER],
            "level": LOG_LEVEL,
            "propagate": True,
        },
    },
    "root": {
        "handlers": [LOG_HANDLER],
        "level": LOG_LEVEL,
        "propagate": True,
    },
}
