# encoding: utf-8
import logging


def init_logger(logfile: str, level: int = logging.DEBUG):
    """Initialize the root logger and standard log handlers."""
    log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(log_formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


def get_logger(name: str = None):
    """Provide the root logger or initialize new."""
    return logging.getLogger(name)
