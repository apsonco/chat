# chat_server.py
# Server class for socket chat

import logging
from socket import socket, AF_INET, SOCK_STREAM
import select

from lib import utils
from lib.config import *
from lib import log_config

from jim.JIMResponse import JIMResponse

from client_manager import ClientManager


class ChatServer:

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.sock = None
        self.clients = []
        self.w_list = []
        self.r_list = []
        self.e_list = []
        self.clients_dict = {}

    def add_client(self, client, user_name):
        self.clients.append(client)
        self.clients_dict[user_name] = client

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

    def listen_for_good(self):
        while True:
            try:
                # Accept order for connection
                client, addr = self.sock.accept()
                result, client_name = self.check_client_presence(client)

                if __debug__:
                    logging.info('Received order for connection from {}'.format(addr))
            except OSError as e:
                # if __debug__:
                #     logging.critical('[ {} ] Error in connection with client'.format(e))
                pass  # out from timeout
            else:
                self.add_client(client, client_name)
            finally:
                # Checking for input/output events that don't have timeout
                # if __debug__:
                #     logging.info('Checking for input/output events')
                self.w_list = []
                self.r_list = []
                try:
                    # Taking all clients which are in listening, writing and error mode
                    self.r_list, self.w_list, self.e_list = self.select_clients()
                except Exception as e:
                    # If client disconnects will rise exception
                    if __debug__:
                        logging.critical('Exception in select.select')
                    #  Do nothing if client disconnects
                    pass
                requests = self.read_requests(self.r_list)
                self.write_responses(requests, self.w_list)

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
                logging.info('Have got message from {}'.format(data[KEY_FROM]))
                responses[sock] = data
            except:
                logging.info('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                read_clients.remove(sock)
        return responses

    def write_responses(self, requests, write_clients):
        """
        Send message between clients
        :param requests: list of request from clients
        :param write_clients: list of sockets
        :return:
        """
        for sock in requests:
            user_to = requests[sock][KEY_TO]
            logging.info('I have message to {}'.format(user_to))
            if user_to in self.clients_dict.keys():
                try:
                    logging.info('Try to send message to {}'.format(user_to))
                    utils.send_message(self.clients_dict[user_to], requests[sock])
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
            # Retrieving user name from presence message
            client_name = client_message[KEY_USER][KEY_ACCOUNT_NAME]
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

        # Storing user to data base
        cl_manager = ClientManager()
        cl_manager.add_client(client_message[KEY_USER][KEY_ACCOUNT_NAME])

        return result, client_name
