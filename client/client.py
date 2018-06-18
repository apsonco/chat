# client.py
#
# Client application. Program send presence message to server and receive response message using socket
# List functions:
# - create presence message
# - send message to server
# - receive response from server
# - parse response message
# Shell parameters client.py <address> [<port>]:
# - address - server IP address
# - port - server TCP port, 5335 by default

import sys
from socket import socket, AF_INET, SOCK_STREAM
import logging

from chat_client import ChatClient
import lib.config


TEST_USER_NAME = 'My_first'

logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def echo_client():
    # Should delete after checking
    user_name = input('Enter your nickname: ')
    user_friend = input('Enter your friend name: ')
    chat_client = ChatClient('localhost', 5335, user_name)
    # Create TCP socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # Create connection with server
        chat_client.connect(sock)

        if chat_client.check_presence() is True:
            if __debug__:
                logging.info('Sent presence message to server. Received HTTP_OK from server')
            while True:
                msg = input('Your message (exit, get_contacts): ')
                if msg == 'exit':
                    break
                elif msg == 'get_contacts':
                    chat_client.send_jim_message(lib.config.VALUE_GET_CONTACTS)
                    quantity = chat_client.get_jim_contacts()
                    for i in range(quantity):
                        contact_id, contact_name = chat_client.get_jim_message()
                        print('I have received: {} - contact id, {} - contact name'.format(contact_id, contact_name))
                        # TODO: Put contact_id and contact_name into data base
                else:
                    chat_client.send_jim_message(lib.config.VALUE_MESSAGE, msg, user_friend)
                # Receive server message
                logging.info('Try get message from '.format(chat_client.get_socket()))
                user_from, server_message = chat_client.get_jim_message()
                print('{}: {}'.format(user_from, server_message))


if __name__ == '__main__':
    echo_client()
