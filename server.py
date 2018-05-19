# server.py
#
# Server application for clients which uses socket.
# List functions:
# - receive client message;
# - create response for client;
# - send message to client;
# Shell parameters server.py -p <port> -a <address>
# -p ​​<port> ​- ​​​TCP port, 7777 by default;
# -a ​​<address>​ -​ ​I​P listening address, listen all addresses by default

import sys
from socket import *
import logging

import utils
from config import *


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

# Create socket
sock = socket(AF_INET, SOCK_STREAM)

# TODO: Edit code for working with console keys -address, -port

# Set port to 5335
sock.bind(('', 5335))
# Switching to listening mode, can serve 5 connections
sock.listen(5)

while True:
    # Accept order for connection
    client, address = sock.accept()
    logging.info('Received order for connection from {}'.format(str(address)))

    # Getting client message
    clientMessage = utils.get_message(client)
    logging.info('Message from client in JSON {}'.format(clientMessage))

    # Parse client message
    if clientMessage[KEY_ACTION] == VALUE_PRESENCE:
        logging.info('Server received {} action.'.format(VALUE_PRESENCE))
        # Create response for client
        serverMessage = utils.response_presence()

    elif KEY_ACTION in clientMessage is False:
        print('Server received wrong order')
        logging.info('Server received wrong order')
        serverMessage = utils.response_error(HTTP_CODE_WRONG_ORDER, STR_ORDER_WITHOUT_PRESENCE)

    else:
        print('Server error')
        serverMessage = utils.response_error(HTTP_CODE_SERVER_ERROR, '')

    # Send response to client
    utils.send_message(client, serverMessage)
    client.close()
