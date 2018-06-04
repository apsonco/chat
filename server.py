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

import utils
from config import *
from JIMResponse import JIMResponse

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


# Main cycle for query processing
def mainloop():

    port, server_address = parse_command_line()
    chat_server = ChatServer(server_address, port)
    sock = chat_server.connect()

    if __debug__:
        logging.info('Set port to {}'.format(port))
        logging.info('Set server address to {}'.format(server_address))

    while True:
        try:
            # Accept order for connection
            client, addr = sock.accept()
            chat_server.check_client_presence(client)

            if __debug__:
                logging.info('Received order for connection from {}'.format(str(addr)))
        except OSError as e:
            # if __debug__:
            #     logging.critical('[ {} ] Error in connection with client'.format(e))
            pass    # out from timeout
        else:
            if __debug__:
                logging.info('Received order for connection with {}'.format(addr))
            chat_server.add_client(client)
        finally:
            # Checking for input/output events that don't have timeout
            # if __debug__:
            #     logging.info('Checking for input/output events')
            w_list = []
            r_list = []
            try:
                # Taking all clients which are in listening, writing and error mode
                r_list, w_list, e_list = chat_server.select_clients()
            except Exception as e:
                # If client disconnects will rise exception
                if __debug__:
                    logging.critical('Exception in select.select')
                #  Do nothing if client disconnects
                pass
            requests = chat_server.read_requests(r_list)
            chat_server.write_responses(requests, w_list)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    mainloop()
