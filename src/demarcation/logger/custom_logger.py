import sys
import logging

DEFAULT_FORMAT = "%(asctime)s | %(levelname)s | %(message)s"


class AppLogger:
    __slots__ = ("format_str", "level", "name", "console_logger",
                 "console_formatter", "logger")

    def __init__(self, name: str, format_str: str = DEFAULT_FORMAT,
                 level: int = logging.INFO) -> None:
        self.format_str = format_str
        self.level = level
        self.name = name

        self.console_formatter = logging.Formatter(self.format_str)
        self.console_logger = logging.StreamHandler(sys.stdout)
        self.console_logger.setFormatter(self.console_formatter)

        self.logger = logging.getLogger()
        self.logger.setLevel(self.level)
        self.logger.addHandler(self.console_logger)

    def info(self, msg: str, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg: str, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg: str, extra=None):
        self.logger.debug(msg, extra=extra)

    def warn(self, msg: str, extra=None):
        self.logger.warn(msg, extra=extra)

    def critical(self, msg: str, extra=None):
        self.logger.critical(msg, extra=extra)
