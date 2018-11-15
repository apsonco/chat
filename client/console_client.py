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
import getpass
import logging
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from client.chat_client import ChatClient
from libchat.chat_config import *
from libchat.log_config import log
from libchat import utils


class GetMessagesThread(Thread):
    def __init__(self, chat_client):
        super().__init__()
        self.daemon = False  # False by default
        self.chat_client = chat_client
        self.is_close = False

    def run(self):
        while True:
            if self.is_close is True:
                break
            try:
                jim_message = self.chat_client.get_message()
            except OSError:
                if self.is_close is True:
                    break
            if KEY_ACTION in jim_message and jim_message[KEY_ACTION] == VALUE_MESSAGE:
                print('{} {}: {}'.format(utils.light_time(jim_message[KEY_TIME]),
                                         jim_message[KEY_FROM],
                                         jim_message[KEY_MESSAGE]))
            else:
                self.chat_client.request_queue.put(jim_message)
                self.chat_client.request_queue.task_done()

        logging.info('Finish GetMessageThread')
        return

    @log
    def stop(self):
        self.chat_client.request_queue.put(None)
        self.is_close = True
        return


TEST_USER_NAME = 'My_first'
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO)


def change_receiver():
    return input('Enter receiver name: ')


def echo_client():
    print('Hello. This is chat app. Please use next command:')
    print('1. ch_receiver - for changing interlocutor name')
    print('2. add_contact - for adding new existing contact to contact list')
    print('3. get_contacts - for printing contact list')
    print('4. del_contact - for deleting certain contact from contact list')
    print('5. exit - for closing app')
    print('Start your conversation:')

    user_name = input('Enter your nickname: ')
    user_password = input('Enter your password: ')
    user_friend = change_receiver()

    chat_client = ChatClient('localhost', 5335, user_name)
    # Create TCP socket
    with socket(AF_INET, SOCK_STREAM) as sock:
        # Create connection with server
        chat_client.connect(sock)
        get_thread = GetMessagesThread(chat_client)

        # TODO: Rewrite - add registration for user
        if chat_client.check_presence() is True and chat_client.authenticate(user_password) is True:
            get_thread.start()
            while True:
                msg = input()
                if msg == 'exit':
                    break
                elif msg == 'ch_receiver':
                    user_friend = change_receiver()
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
            get_thread.stop()
            chat_client.disconnect()


if __name__ == '__main__':
    echo_client()
