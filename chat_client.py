# chat_client.py
# Client class for socket chat

import sys
from socket import socket, AF_INET, SOCK_STREAM
import logging

import socketserver

import utils
from config import *

from JIMMessage import JIMMessage


class ChatClient:

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.sock = None

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

    def check_presence(self):
        """
            Send presence message.
            Check response from server.
            :return True if server receive answer 200. False otherwise.
            """
        message = JIMMessage.presence_message()
        if __debug__:
            logging.info('Client: Create presence message - {}'.format(message))

        # Send message to server
        self.send_message(message)

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
