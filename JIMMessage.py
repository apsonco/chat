# JIMMessage.py
# Class for message which support JIM protocol

import time

from config import *
import utils


class JIMMessage:
    # Create presence message
    @staticmethod
    def presence_message(user_name=VALUE_DEFAULT_USER):
        """
            Creates client presence message and returns it in JSON
            :param user_name: str - user name, should be less than 25 characters
            :return: Message converted to JSON, should support JIM protocol
        """
        if not isinstance(user_name, str):
            raise TypeError
        if len(user_name) > 25:
            raise utils.UsernameTooLongError(user_name)
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_ACTION: VALUE_PRESENCE,
                  KEY_TIME: current_time,
                  KEY_TYPE: VALUE_STATUS_DEFAULT,
                  KEY_USER: {
                      KEY_ACCOUNT_NAME: user_name,
                      KEY_STATUS: STR_ONLINE
                  }}
        return result

    # Create test message
    @staticmethod
    def test_message(message, user_to=VALUE_DEFAULT_USER, user_from=VALUE_DEFAULT_USER):
        current_time = time.time()
        result = {KEY_ACTION: VALUE_MESSAGE,
                  KEY_TIME: current_time,
                  KEY_TO: user_to,
                  KEY_FROM: user_from,
                  KEY_ENCODING: CHARACTER_ENCODING,
                  KEY_MESSAGE: message
                  }
        return result

    # Create quit message
    @staticmethod
    def quit_message(user_name):
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_ACTION: VALUE_QUIT,
                  KEY_TIME: current_time,
                  KEY_TYPE: VALUE_STATUS_DEFAULT,
                  KEY_USER: {
                      KEY_ACCOUNT_NAME: user_name,
                      KEY_STATUS: STR_QUIT
                  }}
        return result
