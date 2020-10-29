import logging
from datetime import datetime
from pathlib import Path


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        "[%(asctime)s: %(levelname)s/%(filename)s: funcName %(funcName)s - line %(lineno)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    ch.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(ch)
    return logger
