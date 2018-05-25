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


# Creates socket, sets connection number, sets timeout
def new_listen_socket(address):
    # Create socket
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    # Switching to listening mode, can serve 5 connections
    sock.listen(5)
    # Set timeout for socket operations
    sock.settimeout(1)
    return sock


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


def read_requests(clients):
    """
    Reads requests from clients list and returns dictionary of messages {socket: message}
    :param clients: list of sockets
    :return: dictionary of messages
    """
    # Dictionary server responses in form {socket: order}
    responses = {}
    for sock in clients:
        try:
            logging.info('Try to get message from {} {}'.format(sock.fileno(), sock.getpeername()))
            data = utils.get_message(sock)
            logging.info('Have got message from {}'.format(data))
            responses[sock] = data
        except:
            logging.info('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
            clients.remove(sock)
    return responses


def write_responses(requests, clients):
    """
    Echo response from server to clients (clients which received orders)
    :param requests: list of request from clients
    :param clients: list of sockets
    :return:
    """
    for sock in clients:
        if sock in requests:
            try:
                logging.info('Try to send message to {} {}'.format(sock.fileno(), sock.getpeername()))
                utils.send_message(sock, requests[sock])
                logging.info('Have sent message {}'.format(requests[sock]))
            except:
                logging.info('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                clients.remove(sock)


# Main cycle for query processing
def mainloop():

    port, server_address = parse_command_line()

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
                # Taking all clients which are in listening, writing and error mode
                r_list, w_list, e_list = select.select(clients, clients, [], 0)
                logging.info('r_list: '.format(r_list))
                logging.info('w_list: '.format(w_list))
            except Exception as e:
                # If client disconnects will rise exception
                logging.info('Exception in select.select')
                #  Do nothing if client disconnects
                pass
            requests = read_requests(r_list)
            write_responses(requests, w_list)


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
