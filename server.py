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

import logging
import sys

from lib.config import *

from chat_server import ChatServer


# Parses command line keys and setups values for socket port and server_address
def parse_command_line():
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
    return port, server_address


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

port, server_address = parse_command_line()
chat_server = ChatServer(server_address, port)
sock = chat_server.connect()
if __debug__:
    logging.info('Set port to {}'.format(port))
chat_server.listen_for_good()
