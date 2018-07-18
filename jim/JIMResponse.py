# JIMResponse.py
# Class for responses messages which support jim protocol

import time

from libchat.chat_config import *
from libchat import log_config


class JIMResponse:

    def __init__(self, response_code=HTTP_CODE_OK, special_value=''):
        self.response_code = response_code
        self.special_value = special_value

    def get_jim_response(self):
        if self.response_code == HTTP_CODE_OK:
            result = self.response_ok()
        elif self.response_code == HTTP_CODE_ACCEPTED:
            result = self.response_quantity(self.special_value)
        else:
            # TODO: Write code for error response
            pass
        return result

    # Create response message
    @staticmethod
    def response_ok():
        """
            Creates JSON with server response message
            :return: JSON, should support jim protocol
        """
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_RESPONSE: HTTP_CODE_OK,
                  KEY_TIME: current_time}
                 # KEY_ALERT: STR_PRESENCE_RECEIVED}
        return result

    # Create contact list quantity message
    @staticmethod
    def response_quantity(quantity):
        """
            Creates JSON with contact list quanity message
            :return: JSON, should support jim protocol
        """
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_RESPONSE: HTTP_CODE_ACCEPTED,
                  KEY_TIME: current_time,
                  KEY_QUANTITY: quantity}
        return result

    # Create single contact message
    @staticmethod
    def response_contact(contact_id, name):
        """
            Creates JSON with one contact message
            :return: JSON, should support jim protocol
        """
        # Time in seconds since the epoch as a floating point number
        current_time = time.time()
        result = {KEY_ACTION: VALUE_CONTACT_LIST,
                  KEY_TIME: current_time,
                  contact_id: name}
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
