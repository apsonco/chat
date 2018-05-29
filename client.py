# client.py
#
# Client application. Program send presence message to server and receive response message using socket
# List functions:
# - create presence message
# - send message to server
# - receive response from server
# - parse response message
# Shell parameters client.py <address> [<port>]:
# - address - server IP address
# - port - server TCP port, 5335 by default

import sys
from socket import socket, AF_INET, SOCK_STREAM
import logging

import utils
from config import *


TEST_USER_NAME = 'My_first'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def echo_client():
    # Create TCP socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # Create connection with server
        sock.connect(('localhost', 5335))

        while True:
            msg = input('Your message: ')
            if msg == 'exit':
                break

            utils.send_message(sock, msg)
            # Receive server message
            logging.info('Try get message from '.format(sock))
            server_message = utils.get_message(sock)
            print('Response: {}'.format(server_message))


if __name__ == '__main__':
    echo_client()
