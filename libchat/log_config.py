# log_config.py
# Only decorator works in this file

import logging


def log(old_func):
    def new_func(*args, **kwargs):
        logging.info('Call {} function'.format(old_func.__name__))
        result = old_func(*args, **kwargs)
        return result
    return new_func
