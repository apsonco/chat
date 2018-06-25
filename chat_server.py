# chat_server.py
# Server class for socket chat

import logging
from socket import socket, AF_INET, SOCK_STREAM
import select

from lib import utils
from lib.config import *
from lib import log_config

from jim.JIMResponse import JIMResponse

from server_db_manager import ServerDbManager


class ChatServer:

    def __init__(self, server_address, port):
        self.server_address = server_address
        self.port = port
        self.sock = None
        self.clients = []
        self.w_list = []
        self.r_list = []
        self.e_list = []
        # TODO: Rewrite code that dosen't need use clients_dict
        self.clients_dict = {} # Has format {'client_name': WebSocket}
        self.clients_names = {} # Has forma {WebSocket: 'client_name'}

    def add_client(self, client, user_name):
        self.clients.append(client)
        self.clients_dict[user_name] = client
        self.clients_names[client] = user_name

    # Creates socket, sets connection number, sets timeout
    def connect(self):
        # Create socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.bind((self.server_address, self.port))
        # Switching to listening mode, can serve 5 connections
        self.sock.listen(5)
        # Set timeout for socket operations
        self.sock.settimeout(0.25)
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

    @log_config.logging_dec
    def parse_request(self, data, sock):
        """
        Parse type of input service message and call equivalent function
        :param data: Input JSON message
        :param sock: Client socket
        :return: nothing
        """
        if data[KEY_ACTION] == VALUE_GET_CONTACTS:
            logging.info('Have got _{}_ message from {}'.format(VALUE_GET_CONTACTS, data[KEY_FROM]))
            self.send_contacts(data[KEY_FROM], sock)
        elif data[KEY_ACTION] == VALUE_ADD_CONTACT:
            logging.info('Have got _{}_ message from {}'.format(VALUE_ADD_CONTACT, self.clients_names[sock]))
            self.add_contact(data[KEY_USER_ID], sock)

    @log_config.logging_dec
    def send_contacts(self, client_name, sock):
        """
        Extract client_name contact list from database and send it to client_name
        :param client_name: Client name
        :param sock: Client socket
        :return:
        """
        db_manager = ServerDbManager()
        contact_list = db_manager.get_contacts(client_name)
        logging.info('contact_list is {}'.format(contact_list))
        response = JIMResponse(HTTP_CODE_ACCEPTED, len(contact_list))

        # First step - return quantity of contacts
        server_message = response.get_jim_response()
        logging.info('response contact list JSON: {}'.format(server_message))
        utils.send_message(sock, server_message)

        # Second step - return contacts list
        for key, value in contact_list.items():
            server_message = response.response_contact(key, value)
            utils.send_message(sock, server_message)
            logging.info('Sent contact message JSON: {}'.format(server_message))
        print('{} has next contacts: {}'.format(client_name, contact_list))

    @log_config.logging_dec
    def add_contact(self, contact_name, sock):
        """
        Store new contact to database and send message to client
        :param contact_name:
        :param sock:
        :return:
        """
        db_manager = ServerDbManager()
        res = db_manager.add_contact(self.clients_names[sock], contact_name)
        if res is True:
            response = JIMResponse()
            server_message = response.get_jim_response()
        else:
            # if contact doesn't exist or other issues with data base
            response = JIMResponse()
            server_message = response.response_error(HTTP_CODE_NOT_FOUND,
                                                     'contact doesnt exist or other issues with data base')
        logging.info('response contact list JSON: {}'.format(server_message))
        utils.send_message(sock, server_message)

    def read_requests(self, read_clients):
        """
        Reads requests from clients list and returns dictionary of messages {socket: message}
        :param read_clients: list of sockets
        :return: dictionary of messages
        """
        # Dictionary server responses in form {socket: order}
        responses = {}
        for sock in read_clients:
            try:
                logging.info('RR function Try to get message from {} {}'.format(sock.fileno(), sock.getpeername()))
                data = utils.get_message(sock)
                logging.info('RR funсtion JSON message is: {}'.format(data))
                responses[sock] = data
                # function for parse service messages
                self.parse_request(data, sock)
            except:
                # TODO: uncomment it and solve connection problem
                pass
                # logging.info('Client {} {} has disconnected'.format(sock.fileno(), sock.getpeername()))
                # read_clients.remove(sock)
        return responses

    def write_responses(self, requests, write_clients):
        """
        Send message between clients
        :param requests: list of request from clients
        :param write_clients: list of sockets
        :return:
        """
        for sock in requests:
            if requests[sock][KEY_ACTION] == VALUE_GET_CONTACTS or requests[sock][KEY_ACTION] == VALUE_ADD_CONTACT:
                pass
            else:
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
        cl_manager = ServerDbManager()
        cl_manager.add_client(client_message[KEY_USER][KEY_ACCOUNT_NAME])

        return result, client_name
