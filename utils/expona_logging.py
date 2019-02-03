"""
expona_logging.py
"""

import logging

def logger_factory(name, logging_level=logging.DEBUG, logging_handler=logging.StreamHandler, logging_formatter=None):

    logger = logging.getLogger(name)
    logger.setLevel(logging_level)

    handler = logging_handler()
    handler.setLevel(logging_level)

    if not logging_formatter:
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
