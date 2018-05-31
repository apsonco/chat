# JIMResponse.py
# Class for responses messages which support JIM protocol

import time

from config import *


class JIMResponse:
    # Create response message
    @staticmethod
    def response_presence():
        """
            Creates JSON with server response message
            :return: JSON, should support JIM protocol
        """
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_RESPONSE: HTTP_CODE_OK,
                  KEY_TIME: current_time,
                  KEY_ALERT: STR_PRESENCE_RECEIVED}
        return result

    # Create error message
    @staticmethod
    def response_error(code, alert):
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_RESPONSE: code,
                  KEY_TIME: current_time,
                  KEY_ALERT: alert}
        return result
