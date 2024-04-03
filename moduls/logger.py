import logging
from functools import wraps


def info_log(message: str):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w")
            logger.info(message)
            return func(*args, **kwargs)

        return wrapped

    return wrapper


def error_log(message: str):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            logger = logging.getLogger(func.__name__)
            logger.error(message)
            return func(*args, **kwargs)

        return wrapped

    return wrapper
