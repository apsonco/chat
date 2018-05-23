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
from socket import socket, AF_INET, SOCK_STREAM
import select
import time

import utils
from config import *


def new_listen_socket(address):
    # Create socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    # Switching to listening mode, can serve 5 connections
    sock.listen(5)
    # Set timeout for socket operations
    sock.settimeout(1)
    return sock


# Main cycle for query processing
def mainloop():
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

    address = (server_address, port)
    clients = []
    sock = new_listen_socket(address)

    logging.info('Set port to {}'.format(port))
    logging.info('Set server address to {}'.format(server_address))

    while True:
        try:
            # Accept order for connection
            client, addr = sock.accept()
            logging.info('Received order for connection from {}'.format(str(address)))
        except OSError as e:
            # TODO: add to logger
            pass    # out from timeout
        else:
            logging.info('Received order for connection with {}'.format(addr))
            clients.append(client)
        finally:
            # Checking for input/output events that don't have timeout
            logging.info('Checking for input/output events')
            w_list = []
            r_list = []
            try:
                r_list, w_list, e_list = select.select(clients, clients, [], 0)
                logging.info('w_list: '.format(w_list))
            except Exception as e:
                # If client disconnects will rise exception
                logging.info('Exception in select.select')
                pass   #  Do nothing if client disconnects
            for s_client in w_list:
                time_str = time.ctime(time.time()) + '\n'
                try:
                    server_message = utils.test_message(time_str + 'Hello it server')
                    logging.info('Try send message to {}'.format(s_client))
                    utils.send_message(s_client, server_message)
                except:
                    # Remove clients with disconnected
                    clients.remove(s_client)
                finally:
                    logging.info('Server send message: {}'.format(server_message))

            # # Getting client message
            # client_message = utils.get_message(client)
            # logging.info('Message from client in JSON {}'.format(client_message))
            #
            # # Parse client message
            # if client_message[KEY_ACTION] == VALUE_PRESENCE:
            #     logging.info('Server received {} action.'.format(VALUE_PRESENCE))
            #     # Create response for client
            #     server_message = utils.response_presence()
            # elif KEY_ACTION in client_message is False:
            #     print('Server received wrong order')
            #     logging.info('Server received wrong order')
            #     server_message = utils.response_error(HTTP_CODE_WRONG_ORDER, STR_ORDER_WITHOUT_PRESENCE)
            # else:
            #     print('Server error')
            #     server_message = utils.response_error(HTTP_CODE_SERVER_ERROR, '')
            #
            # # Send response to client
            # utils.send_message(client, server_message)
            # client.close()


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

mainloop()
