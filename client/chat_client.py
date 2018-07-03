# chat_client.py
# Client class for socket chat

import logging
import time

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
        message_time = time.gmtime(float(jim_message[KEY_TIME]))
        str_time = str(message_time.tm_hour) + ':' + str(message_time.tm_min)
        return user_from, message, str_time

    @log_config.logging_dec
    def get_jim_response(self):
        """
        Receive server response
        :return: Quantity of contacts or KEY_RESPONSE
        """
        jim_message = self.get_message()
        if __debug__:
            logging.info('Client: Get message from server - {}'.format(jim_message))
        if jim_message[KEY_RESPONSE] == HTTP_CODE_ACCEPTED:
            quantity = jim_message[KEY_QUANTITY]
        elif jim_message[KEY_RESPONSE] == HTTP_CODE_OK:
            return HTTP_CODE_OK
        elif jim_message[KEY_RESPONSE] == HTTP_CODE_NOT_FOUND:
            return jim_message[KEY_ALERT]
        return quantity

    @log_config.logging_dec
    def send_add_contact(self, client):
        message = JIMMessage(VALUE_ADD_CONTACT)
        jim_message = message.create_jim_message(client)
        self.send_message(jim_message)
        logging.info('chat_client.py - sent message to server: {}'.format(jim_message))

    def send_jim_message(self, value_msg=VALUE_MESSAGE, msg='', user_to=''):
        message = JIMMessage(value_msg, self.user_name, user_to)
        jim_message = message.create_jim_message(msg)
        self.send_message(jim_message)
        message_time = time.gmtime(float(jim_message[KEY_TIME]))
        return str(message_time.tm_hour) + ':' + str(message_time.tm_min)

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

    def get_contacts(self):
        self.send_jim_message(VALUE_GET_CONTACTS)
        quantity = self.get_jim_response()
        result = []
        for i in range(quantity):
            contact_id, contact_name = self.get_jim_message()
            logging.info('I have received: {} - contact id, {} - contact name'.format(contact_id, contact_name))
            result.append(contact_name)
            # TODO: Put contact_id and contact_name into data base
        return result

    def add_contact(self, contact):
        self.send_add_contact(contact)
        response_code = self.get_jim_response()
        if response_code == HTTP_CODE_OK:
            result = True
            logging.info('Server added contact {}'.format(contact))
        else:
            result = False
            logging.info(response_code)
        return result
