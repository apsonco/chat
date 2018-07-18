# chat_client.py
# Client class for socket chat

import logging
import time
from queue import Queue
import hmac

from libchat import utils
from libchat.chat_config import *
from libchat.log_config import log

from jim.JIMMessage import JIMMessage


class ChatClient:

    def __init__(self, server_address, port, user_name):
        self.server_address = server_address
        self.port = port
        self.sock = None
        self.user_name = user_name
        self.contact_list = {}
        self.request_queue = Queue()

    def connect(self, sock):
        sock.connect((self.server_address, self.port))
        self.sock = sock

    def disconnect(self):
        self.sock.close()

    def send_message(self, msg):
        utils.send_message(self.sock, msg)
        logging.info('chat_client.py sent message to server: {}'.format(msg))

    def get_message(self):
        server_message = utils.get_message(self.sock)
        logging.info('chat_client.py got message from server: {}'.format(server_message))
        return server_message

    def get_socket(self):
        return self.sock

    def authenticate(self, secret_key):
        """
        Authenticate user on server using password as a secret_key
        :param secret_key:
        :return: True if server has user with such password or else otherwise
        """
        result = False
        message = self.sock.recv(32)
        if __debug__:
            logging.info('Authentication. Server random message {}'.format(message.decode))

        pair = self.user_name + secret_key
        client_hash = hmac.new(pair.encode(CHARACTER_ENCODING), message)
        digest = client_hash.digest()
        self.sock.send(digest)
        if __debug__:
            logging.info('Authentication. Client digest {}'.format(digest.decode))

        response = self.sock.recv(2)
        if __debug__:
            logging.info('Authentication. Server response {}'.format(response.decode))

        if response == b'Ok':
            result = True
        return result


    @log
    def get_jim_message(self):
        # TODO: Should rewrite because we use threads in client for receiving messages
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

    def send_add_del_contact(self, value, client):
        message = JIMMessage(value)
        jim_message = message.create_jim_message(client)
        self.send_message(jim_message)

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
            if __debug__:
                logging.info('Sent presence message to server. Received HTTP_OK from server')
        # elif code == HTTP_CODE_WRONG_ORDER:
        #     print(STR_ORDER_WITHOUT_PRESENCE)
        return result

    @log
    def get_contacts(self):
        self.send_jim_message(VALUE_GET_CONTACTS)
        message = self.request_queue.get()
        quantity = message[KEY_QUANTITY]
        logging.info('f get_contact, receive {} quantity'.format(quantity))
        # when we works without threads
        # quantity = self.get_jim_response()
        result = []
        for i in range(quantity):
            message = self.request_queue.get()
            res = list(message)
            contact_id = res[2]
            contact_name = message[contact_id]
            logging.info('I have received: {} - contact id, {} - contact name'.format(contact_id, contact_name))
            result.append(contact_name)
            # TODO: Put contact_id and contact_name into data base
        return result

    def add_contact(self, contact):
        self.send_add_del_contact(VALUE_ADD_CONTACT, contact)
        message = self.request_queue.get()
        response_code = message[KEY_RESPONSE]
        if response_code == HTTP_CODE_OK:
            result = True
            logging.info('Server added contact {}'.format(contact))
        else:
            result = False
            logging.info(response_code)
        return result

    @log
    def del_contact(self, contact):
        self.send_add_del_contact(VALUE_DEL_CONTACT, contact)
        message = self.request_queue.get()
        response_code = message[KEY_RESPONSE]
        if response_code == HTTP_CODE_OK:
            result = True
            logging.info('Contact {} was successfully deleted from server'.format(contact))
        else:
            result = False
            logging.info(response_code)
        return result
