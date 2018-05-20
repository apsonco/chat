# server.py
#
# Server application for clients which uses socket.
# List functions:
# - receive client message;
# - create response for client;
# - send message to client;
# Shell parameters server.py -p <port> -a <address>
# -p ​​<port> ​- ​​​TCP port, 5335 by default;
# -a ​​<address>​ -​ ​I​P listening address, listen all addresses by default


from socket import *
import logging
import sys

import utils
from config import *


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

port = DEFAULT_PORT
server_address = DEFAULT_SERVER_IP_LISTENING_ADDRESS

# TODO: Edit code for working with console keys -address, -port
# or find out library

if len(sys.argv) > 1:
    # TODO: Create a function with code from 'else'
    key1 = sys.argv[1]
    if key1 == '-p':
        try:
            port = int(sys.argv[2])
        except ValueError:
            print('Port should be integer number')
            sys.exit(0)
    elif key1 == '-a':
        try:
            server_address = sys.argv[2]
        except ValueError:
            print('Value error in server address')
            sys.exit(0)

logging.info('Set port to {}'.format(port))
logging.info('Set server address to {}'.format(server_address))

# Create socket
sock = socket(AF_INET, SOCK_STREAM)

# Bind socket
sock.bind((server_address, port))
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
