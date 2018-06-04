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

import utils
from config import *
from JIMResponse import JIMResponse


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
                logging.critical('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                sock.close()
                clients.remove(sock)


def check_client_presence(client):
    """
    Check for presence message from client. And send correct answer.
    :param client: socket
    :return: True if client send presence message. False otherwise.
    """
    # Getting client message
    client_message = utils.get_message(client)
    result = False
    if __debug__:
        logging.info('Message from client in JSON {}'.format(client_message))

    # Parse client message
    if client_message[KEY_ACTION] == VALUE_PRESENCE:
        if __debug__:
            logging.info('Server received {} action.'.format(VALUE_PRESENCE))
        # Create response for client
        response = JIMResponse()
        server_message = response.get_jim_response()
        result = True

    elif KEY_ACTION in clientMessage is False:
        if __debug__:
            logging.info('Server received wrong order')
        # TODO: rewrite using new JIMResponce method get_gim_response
        server_message = JIMResponse.response_error(HTTP_CODE_WRONG_ORDER, STR_ORDER_WITHOUT_PRESENCE)

    else:
        if __debug__:
            logging.info('Server couldnt decode message from client')
        # TODO: rewrite using new JIMResponce method get_gim_response
        server_message = JIMResponse.response_error(HTTP_CODE_SERVER_ERROR, '')

    # Send response to client
    utils.send_message(client, server_message)
    return result


# Main cycle for query processing
def mainloop():

    port, server_address = parse_command_line()

    address = (server_address, port)
    clients = []
    sock = new_listen_socket(address)

    if __debug__:
        logging.info('Set port to {}'.format(port))
        logging.info('Set server address to {}'.format(server_address))

    while True:
        try:
            # Accept order for connection
            client, addr = sock.accept()
            check_client_presence(client)

            if __debug__:
                logging.info('Received order for connection from {}'.format(str(addr)))
        except OSError as e:
            # if __debug__:
            #     logging.critical('[ {} ] Error in connection with client'.format(e))
            pass    # out from timeout
        else:
            if __debug__:
                logging.info('Received order for connection with {}'.format(addr))
            clients.append(client)
        finally:
            # Checking for input/output events that don't have timeout
            # if __debug__:
            #     logging.info('Checking for input/output events')
            w_list = []
            r_list = []
            try:
                # Taking all clients which are in listening, writing and error mode
                r_list, w_list, e_list = select.select(clients, clients, [], 0)
            except Exception as e:
                # If client disconnects will rise exception
                if __debug__:
                    logging.critical('Exception in select.select')
                #  Do nothing if client disconnects
                pass
            requests = read_requests(r_list)
            write_responses(requests, w_list)


logging.basicConfig(stream=sys.stdout, level=logging.INFO)

if __name__ == '__main__':
    mainloop()
