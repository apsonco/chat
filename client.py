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

# Create TCP socket
sock = socket(AF_INET, SOCK_STREAM)

# TODO: Edit code for working with console keys -address, -port

# Create connection with server
sock.connect(('localhost', 5335))

while True:
    # Receive server message
    logging.info('Try get message from '.format(sock))
    server_message = utils.get_message(sock)
    message_type = server_message[KEY_ACTION]
    if message_type == VALUE_MESSAGE:
        print(server_message[KEY_MESSAGE])

# # Create presence message
# message = utils.presence_message(TEST_USER_NAME)
# # Send message to server
# utils.send_message(sock, message)
# # Receive server message
# serverMessage = utils.get_message(sock)
#
# # Parse response message
# code = serverMessage[KEY_RESPONSE]
# if code == HTTP_CODE_OK:
#     print(STR_PRESENCE_RECEIVED)
# elif code == HTTP_CODE_WRONG_ORDER:
#     print(STR_ORDER_WITHOUT_PRESENCE)

logging.info('Server response JSON : {}'.format(serverMessage))

sock.close()
