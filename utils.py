# utils.py
#
# Utils for serve date transmission via socket

import time
import json

from config import *


def dict_to_bytes(dict):
    result = json.dumps(dict).encode(CHARACTER_ENCODING)
    return result


def send_message(web_socket, dict_message):
    result = dict_to_bytes(dict_message)
    web_socket.send(result)


def get_message(web_socket):
    str = web_socket.recv(1024).decode(CHARACTER_ENCODING)
    result = json.loads(str)
    return result


# Messages

# Create response message
def response_presence():
    # Time in seconds since the epoch as a floating point number
    current_time = time.time()
    result = {KEY_RESPONSE: HTTP_CODE_OK,
              KEY_TIME: current_time,
              KEY_ALERT: STR_PRESENCE_RECEIVED}
    return result


# Create presence message
def presence_message(user_name):
    # Time in seconds since the epoch as a floating point number
    current_time = time.time()
    result = {KEY_ACTION: VALUE_PRESENCE,
              KEY_TIME: current_time,
              KEY_TYPE: 'status',       # TODO: Should define and carry to config.py
              KEY_USER: {
                  KEY_ACCOUNT_NAME: user_name,
                  KEY_STATUS: STR_ONLINE
              }}
    return result


# Create quit message
def quit_message(user_name):
    # Time in seconds since the epoch as a floating point number
    current_time = time.time()
    result = {KEY_ACTION: VALUE_QUIT,
              KEY_TIME: current_time,
              KEY_TYPE: 'status',       # TODO: Should define and carry to config.py
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
