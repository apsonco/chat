# JIMMessage.py
# Class for message which support jim protocol
# JSON should has length less than 600 characters
# final message should be less than 500 characters

import time

from libchat.chat_config import *


class JIMMessage:

    def __init__(self, action, user=VALUE_DEFAULT_USER, user_to=VALUE_DEFAULT_USER):
        self.action = action
        self.user_from = user
        self.user_to = user_to
        self.message = ''

    def create_jim_message(self, message=''):
        """
        Fabric method which chose action type and return appropriate JSON
        :return: Message converted to JSON, should support jim protocol
        """
        if self.action is VALUE_PRESENCE:
            result = self.presence_message(self.user_from)
        elif self.action is VALUE_MESSAGE:
            result = self.test_message(message, self.user_from, self.user_to)
        elif self.action is VALUE_GET_CONTACTS:
            result = self.get_contacts(self.user_from)
        elif self.action is VALUE_ADD_CONTACT:
            result = self.get_add_del_contact(VALUE_ADD_CONTACT, message)
        elif self.action is VALUE_DEL_CONTACT:
            result = self.get_add_del_contact(VALUE_DEL_CONTACT, message)
        elif self.action is VALUE_QUIT:
            result = self.quit_message(self.user_from)

        return result

    # Create presence message
    @staticmethod
    def presence_message(user_name=VALUE_DEFAULT_USER):
        """
            Creates client presence message and returns it in JSON
            :param user_name: str - user name, should be less than 25 characters
            :return: Message converted to JSON, should support jim protocol
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
    @staticmethod
    def test_message(message, user_from=VALUE_DEFAULT_USER, user_to=VALUE_DEFAULT_USER):
        current_time = time.time()
        result = {KEY_ACTION: VALUE_MESSAGE,
                  KEY_TIME: current_time,
                  KEY_TO: user_to,
                  KEY_FROM: user_from,
                  KEY_ENCODING: CHARACTER_ENCODING,
                  KEY_MESSAGE: message
                  }
        return result

    # Create test message
    @staticmethod
    def get_contacts(user_from=VALUE_DEFAULT_USER):
        current_time = time.time()
        result = {KEY_ACTION: VALUE_GET_CONTACTS,
                  KEY_TIME: current_time,
                  KEY_FROM: user_from,
                  KEY_ENCODING: CHARACTER_ENCODING,
                  }
        return result

    # Create add contact message
    @staticmethod
    def get_add_del_contact(value, client):
        current_time = time.time()
        result = {KEY_ACTION: value,
                  KEY_USER_ID: client,
                  KEY_TIME: current_time
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

# Messages


# Error type for checking string length
class UsernameTooLongError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

    def __str__(self, username):
        return 'User name {} must be less than 26 characters'.format(username)