# chat_client.py
# Client class for socket chat

import logging

from lib import utils
from lib.config import *
from lib import log_config

from jim.JIMMessage import JIMMessage


class ChatClient:

    def __init__(self, server_address, port, user_name):
        self.server_address = server_address
        self.port = port
        self.sock = None
        self.user_name = user_name
        self.contact_list = {}

    def connect(self, sock):
        sock.connect((self.server_address, self.port))
        self.sock = sock

    def send_message(self, msg):
        utils.send_message(self.sock, msg)

    def get_message(self):
        server_message = utils.get_message(self.sock)
        return server_message

    def get_socket(self):
        return self.sock

    @log_config.logging_dec
    def get_jim_message(self):
        jim_message = self.get_message()
        if __debug__:
            logging.info('Client: Get message from server - {}'.format(jim_message))
        if jim_message[KEY_ACTION] == VALUE_MESSAGE:
            message = jim_message[KEY_MESSAGE]
            user_from = jim_message[KEY_FROM]
        elif jim_message[KEY_ACTION] == VALUE_CONTACT_LIST:
            res = list(jim_message)
            friend_id = res[2]
            friend_name = jim_message[friend_id]
            return friend_id, friend_name
        return user_from, message

    def get_jim_contacts(self):
        """
        Receive contacts list quantity
        :return: Quantity of contacts
        """
        jim_message = self.get_message()
        if __debug__:
            logging.info('Client: Get message from server - {}'.format(jim_message))
        if jim_message[KEY_RESPONSE] == HTTP_CODE_ACCEPTED:
            quantity = jim_message[KEY_QUANTITY]
        return quantity

    def send_jim_message(self, value_msg, msg='', user_to=''):
        message = JIMMessage(value_msg, self.user_name, user_to)
        jim_message = message.create_jim_message(msg)
        self.send_message(jim_message)

    def check_presence(self):
        """
        Send presence message.
        Check response from server.
        :return True if server receive answer 200. False otherwise.
        """
        message = JIMMessage(VALUE_PRESENCE, self.user_name)
        jim_message = message.create_jim_message()
        if __debug__:
            logging.info('Client: Create presence message - {}'.format(jim_message))

        # Send message to server
        self.send_message(jim_message)

        # Receive server message
        server_message = self.get_message()

        result = False
        # Parse response message
        code = server_message[KEY_RESPONSE]
        if code == HTTP_CODE_OK:
            result = True
        # elif code == HTTP_CODE_WRONG_ORDER:
        #     print(STR_ORDER_WITHOUT_PRESENCE)
        return result
