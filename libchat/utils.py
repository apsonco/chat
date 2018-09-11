# utils.py
#
# Utils for serve date transmission via socket

import json
import time

from libchat.chat_config import *
from libchat.log_config import log


def dict_to_bytes(dict_message):
    result = json.dumps(dict_message).encode(CHARACTER_ENCODING)
    return result


def dict_from_bytes(byte_str):
    result = byte_str.decode(CHARACTER_ENCODING)
    result = json.loads(result)
    return result


@log
def send_message(web_socket, dict_message):
    """
        Sends binary socket message
        :param web_socket: socket - Socket object
        :param dict_message: JSON supported jim protocol
    """
    # TODO: uncomment on Lesson 03
    # if not isinstance(dict_message, dict):
    #     raise TypeError
    result = dict_to_bytes(dict_message)
    web_socket.send(result)


@log
def get_message(web_socket):
    """
        Gets binary socket message and returns dictionary
        :param web_socket: socket - Socket object
        :return: Message converted to JSON, should support jim protocol
    """
    byte_str = web_socket.recv(1024)
    result = dict_from_bytes(byte_str)
    return result


def light_time(str_time):
    """
        Converts sting which value is current time in seconds since the Epoch to HH:MM string
        :param str_time: result of time.time()
        :return: string with time in format HH:MM
    """
    message_time = time.gmtime(float(str_time))
    return '{:02}'.format(message_time.tm_hour) + ':' + '{:02}'.format(message_time.tm_min)


