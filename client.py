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


def check_presence(sock):
    """
    Send presence message.
    Check response from server.
    :param sock - socket.
    :return True if server receive answer 200. False otherwise.
    """
    message = utils.presence_message()
    if __debug__:
        logging.info('Client: Create presence message - {}'.format(message))
    # Send message to server
    utils.send_message(sock, message)

    # Receive server message
    server_message = utils.get_message(sock)

    result = False
    # Parse response message
    code = server_message[KEY_RESPONSE]
    if code == HTTP_CODE_OK:
        result = True
    # elif code == HTTP_CODE_WRONG_ORDER:
    #     print(STR_ORDER_WITHOUT_PRESENCE)
    return result


def echo_client():
    # Create TCP socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # Create connection with server
        sock.connect(('localhost', 5335))

        if check_presence(sock) is True:
            if __debug__:
                logging.info('Sent presence message to server. Received HTTP_OK from server')
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
