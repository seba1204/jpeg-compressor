import logging

from src.arguments import Arguments


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_log_level(args: Arguments) -> int:
    """Set the log level of the logger based on the arguments"""
    # if the debug mode is enabled, set the logger level to debug
    if args.debug:
        return logging.DEBUG
        # if the quiet mode is enabled, set the logger level to warning
    elif args.quiet:
        return logging.ERROR
    else:
        return logging.INFO


def set_logger(args: Arguments) -> logging.Logger:

    # set the logger
    logger = logging.getLogger()
    log_level = get_log_level(args)
    logger.setLevel(log_level)

    formatter = CustomFormatter("%(levelname)s - %(message)s")

    # create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
