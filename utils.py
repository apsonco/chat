# utils.py
#
# Utils for serve date transmission via socket

import time
import json

from config import *
import log_config


def dict_to_bytes(dict_message):
    result = json.dumps(dict_message).encode(CHARACTER_ENCODING)
    return result


def dict_from_bytes(byte_str):
    result = byte_str.decode(CHARACTER_ENCODING)
    result = json.loads(result)
    return result


@log_config.logging_dec
def send_message(web_socket, dict_message):
    """
        Sends binary socket message
        :param web_socket: socket - Socket object
        :param dict_message: JSON supported JIM protocol
    """
    # TODO: uncomment on Lesson 03
    # if not isinstance(dict_message, dict):
    #     raise TypeError
    result = dict_to_bytes(dict_message)
    web_socket.send(result)


def get_message(web_socket):
    """
        Gets binary socket message and returns dictionary
        :param web_socket: socket - Socket object
        :return: Message converted to JSON, should support JIM protocol
    """
    byte_str = web_socket.recv(1024)
    result = dict_from_bytes(byte_str)
    return result


# Messages


# Error type for checking string length
class UsernameTooLongError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def __str__(self, username):
        return 'User name {} must be less than 26 characters'.format(username)


# Create response message
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


# Create presence message
def presence_message(user_name=VALUE_DEFAULT_USER):
    """
        Creates client presence message and returns it in JSON
        :param user_name: str - user name, should be less than 25 characters
        :return: Message converted to JSON, should support JIM protocol
    """
    if not isinstance(user_name, str):
        raise TypeError
    if len(user_name) > 25:
        raise UsernameTooLongError(user_name)
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


# Create error message
def response_error(code, alert):
    # Time in seconds since the epoch as a floating point number
    current_time = time.time()
    result = {KEY_RESPONSE: code,
              KEY_TIME: current_time,
              KEY_ALERT: alert}
    return result
