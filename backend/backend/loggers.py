import logging

# Stolen from here:
# https://stackoverflow.com/questions/56559971/show-extra-fields-when-logging-to-console-in-python


class ExtraContextFormatter(logging.Formatter):
    def_keys = [
        "name",
        "msg",
        "args",
        "levelname",
        "levelno",
        "pathname",
        "filename",
        "module",
        "exc_info",
        "exc_text",
        "stack_info",
        "lineno",
        "funcName",
        "created",
        "msecs",
        "relativeCreated",
        "thread",
        "threadName",
        "processName",
        "process",
        "message",
        "asctime",
    ]

    def format(self, record):
        string = super().format(record)
        extra = {k: v for k, v in record.__dict__.items() if k not in self.def_keys}
        if len(extra) > 0:
            string += "\033[0;32m - extra: " + str(extra) + "\033[0m"
        return string
