# chat_server.py
# Server class for socket chat

import logging
from socket import socket, AF_INET, SOCK_STREAM
import select

import utils
from config import *

from JIMResponse import JIMResponse


class ChatServer:

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.sock = None
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    # Creates socket, sets connection number, sets timeout
    def connect(self):
        # Create socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.server_address, self.port))
        # Switching to listening mode, can serve 5 connections
        self.sock.listen(5)
        # Set timeout for socket operations
        self.sock.settimeout(1)
        return self.sock

    # Taking all clients which are in listening, writing and error mode
    def select_clients(self):
        r_list, w_list, e_list = select.select(self.clients, self.clients, [], 0)
        return r_list, w_list, e_list

    @staticmethod
    def read_requests(read_clients):
        """
        Reads requests from clients list and returns dictionary of messages {socket: message}
        :param read_clients: list of sockets
        :return: dictionary of messages
        """
        # Dictionary server responses in form {socket: order}
        responses = {}
        for sock in read_clients:
            try:
                logging.info('Try to get message from {} {}'.format(sock.fileno(), sock.getpeername()))
                data = utils.get_message(sock)
                logging.info('Have got message from {}'.format(data))
                responses[sock] = data
            except:
                logging.info('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                read_clients.remove(sock)
        return responses

    @staticmethod
    def write_responses(requests, write_clients):
        """
        Echo response from server to clients (clients which received orders)
        :param requests: list of request from clients
        :param write_clients: list of sockets
        :return:
        """
        for sock in write_clients:
            if sock in requests:
                try:
                    logging.info('Try to send message to {} {}'.format(sock.fileno(), sock.getpeername()))
                    utils.send_message(sock, requests[sock])
                    logging.info('Have sent message {}'.format(requests[sock]))
                except:
                    logging.critical('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                    sock.close()
                    write_clients.remove(sock)

    @staticmethod
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
