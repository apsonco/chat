# JIMResponse.py
# Class for responses messages which support jim protocol

import time

from lib.config import *


class JIMResponse:

    def __init__(self, response_code=HTTP_CODE_OK):
        self.response_code = response_code

    def get_jim_response(self):
        if self.response_code == HTTP_CODE_OK:
            result = self.response_presence()
        else:
            # TODO: Write code for error response
            pass
        return result

    # Create response message
    @staticmethod
    def response_presence():
        """
            Creates JSON with server response message
            :return: JSON, should support jim protocol
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
