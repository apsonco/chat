# log_config.py
# Only decorator works in this file
# TODO: See lesson 02 and do it working

import logging
import sys


def logging_dec(old_func):
    def new_func(*args, **kwargs):
        logging.info('Call {} function'.format(old_func.__name__))
        result = old_func(*args, **kwargs)
        return result
    return new_func


# # Define messages format
# format_log = logging.Formatter('%(levelname)-10s %(asctime)s %(message)s')
#
# # Create log for receiving messages with CRITICAL level
# info_handler = logging.StreamHandler(sys.stdout)
# info_handler.setLevel(logging.INFO)
# info_handler.setFormatter(format_log)
#
# # Create log for writing messages in file
# app_log_file = logging.FileHandler('app.log')
# app_log_file.setFormatter(format_log)
#
# app_log = logging.getLogger('application_log')
# # Uncomment for writing log in file
# # app_log.addHandler(app_log_file)
# # app_log.addHandler(critical_handler)
# app_log.addHandler(info_handler)

