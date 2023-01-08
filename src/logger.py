from src.arguments import Arguments
import logging


def get_log_level(args: Arguments) -> int:
    """Set the log level of the logger based on the arguments"""
    # if the debug mode is enabled, set the logger level to debug
    if args.debug:
        return logging.DEBUG
        # if the quiet mode is enabled, set the logger level to warning
    elif args.quiet:
        return logging.WARNING
    else:
        return logging.INFO


def set_logger(args: Arguments) -> logging.Logger:

    # set the logger
    logger = logging.getLogger()
    log_level = get_log_level(args)
    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
