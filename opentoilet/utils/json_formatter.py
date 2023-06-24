import json
import logging

DEFAULT_FIELDS = [
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "message",
    "module",
    "msecs",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
]

RESERVED_FIELDS = ["message", "service", "environment"]


class JSONFormatter(logging.Formatter):
    def __init__(self, *args, **kwargs):
        self.service = kwargs.get("service", "unknown")
        self.environment = kwargs.get("environment", "unknown")
        super().__init__()

    def format(self, record):
        msg = {
            "message": record.getMessage(),
            "severity": record.levelname,
            "module": record.module,
            "component": record.module,
            "service": self.service,
            "environment": self.environment,
        }

        for key in record.__dict__.keys():
            if key in RESERVED_FIELDS:
                continue

            if key not in DEFAULT_FIELDS:
                msg[key] = str(getattr(record, key))

        return json.dumps(msg)
