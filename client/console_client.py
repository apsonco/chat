# console_client.py
#
# Client application. Program send presence message to server and receive response message using socket
# List functions:
# - create presence message
# - send message to server
# - receive response from server
# - parse response message
# Shell parameters console_client.py <address> [<port>]:
# - address - server IP address
# - port - server TCP port, 5335 by default

import sys
from socket import socket, AF_INET, SOCK_STREAM
import logging
from threading import Thread

from chat_client import ChatClient
from lib.config import *


class GetMessagesThread(Thread):
    def __init__(self, chat_client):
        super().__init__()
        self.daemon = False # False by default
        self.chat_client = chat_client

    def run(self):
        while True:
            jim_message = self.chat_client.get_message()
            if KEY_ACTION in jim_message and jim_message[KEY_ACTION] == VALUE_MESSAGE:
                # user_from, server_message, str_time = self.chat_client.get_jim_message()
                print('{} {}: {}'.format(jim_message[KEY_TIME], jim_message[KEY_FROM], jim_message[KEY_MESSAGE]))
            else:
                self.chat_client.request_queue.put(jim_message)
                self.chat_client.request_queue.task_done()

    def close(self):
        self.chat_client.request_queue.put(None)
        #self.chat_client.request_queue.join()


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
        get_thread = GetMessagesThread(chat_client)

        if chat_client.check_presence() is True:
            if __debug__:
                logging.info('Sent presence message to server. Received HTTP_OK from server')

            get_thread.start()

            while True:
                msg = input('Your message (exit, get_contacts, add_contact, del_contact): ')
                if msg == 'exit':
                    get_thread.close()
                    break
                elif msg == 'get_contacts':
                    print(chat_client.get_contacts())
                elif msg == 'add_contact':
                    contact = input('Enter contact: ')
                    chat_client.add_contact(contact)
                elif msg == 'del_contact':
                    contact = input('Enter contact for deleting: ')
                    chat_client.del_contact(contact)
                else:
                    chat_client.send_jim_message(VALUE_MESSAGE, msg, user_friend)

            chat_client.disconnect()


if __name__ == '__main__':
    echo_client()
