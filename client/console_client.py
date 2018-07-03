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
import time
from threading import Thread
from queue import Queue

from chat_client import ChatClient
import lib.config


class GetMessagesThread(Thread):
    def __init__(self, interval):
        super().__init__()
        self.daemon = False # False by default
        self.interval = interval
        self.chat_client = None

    def run(self):
        while True:
            user_from, server_message, str_time = self.chat_client.get_jim_message()
            print('{} {}: {}'.format(str_time, user_from, server_message))
            time.sleep(self.interval)

    def set_client(self, chat_client):
        self.chat_client = chat_client


class WorkerThread(Thread):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_queue = Queue()

    def send(self, item):
        self.input_queue.put(item)

    def close(self):
        self.input_queue.put(None)
        self.input_queue.join()

    def run(self):
        logging.info('start queue...')
        self.input_queue.get()
        self.input_queue.task_done()
        logging.info('end queue...')
        return


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
        get_thread = GetMessagesThread(1)

        if chat_client.check_presence() is True:
            if __debug__:
                logging.info('Sent presence message to server. Received HTTP_OK from server')

            get_thread.set_client(chat_client)
            get_thread.start()

            working_thread = WorkerThread()
            working_thread.start()

            while True:
                msg = input('Your message (exit, get_contacts, add_contact): ')
                if msg == 'exit':
                    break
                elif msg == 'get_contacts':
                    print(chat_client.get_contacts())
                elif msg == 'add_contact':
                    contact = input('Enter contact: ')

                    working_thread.send(chat_client.add_contact(contact))
                    #working_thread.close()

                else:
                    chat_client.send_jim_message(lib.config.VALUE_MESSAGE, msg, user_friend)


if __name__ == '__main__':
    echo_client()
