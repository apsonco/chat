import sys
import logging

from PyQt5 import QtWidgets, uic
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from client.chat_client import ChatClient
from libchat.chat_config import *
from libchat.log_config import log
from libchat import utils


class GetMessagesThread(Thread):
    def __init__(self, chat_client):
        super().__init__()
        self.daemon = False # False by default
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
                user_from = jim_message[KEY_FROM]
                str_time = jim_message[KEY_TIME]
                message = jim_message[KEY_MESSAGE]
                print('{} {}: {}'.format(jim_message[KEY_TIME], jim_message[KEY_FROM], jim_message[KEY_MESSAGE]))
                if user_from in window.chats:
                    logging.info('Have found user {} in contacts '.format(user_from))
                    window.chats[user_from].append({str_time: message})
                else:
                    # Received first message from user_from
                    window.chats[user_from] = ({str_time: message},)
                window.listWidgetMessages.addItem(utils.light_time(str_time) + ' ' + user_from + ' > ' + message)
            else:
                window.chat_client.request_queue.put(jim_message)
                window.chat_client.request_queue.task_done()

        logging.info('Finish GetMessageThread')
        return

    @log
    def stop(self):
        self.chat_client.request_queue.put(None)
        self.is_close = True
        return


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, user_name=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('chat_gui.ui', self)
        self.pushButton.clicked.connect(QtWidgets.qApp.quit)
        self.setWindowTitle('Chat client: ' + user_name)

        self.pushButtonConnect.clicked.connect(self.on_button_connect_clicked)
        self.pushButtonSend.clicked.connect(self.on_button_send_clicked)

        self.listWidgetContacts.currentItemChanged.connect(self.contacts_current_item_changed)

        self.sock = None
        self.get_thread = None
        self.chat_client = None

        self.chats = {}

    def finished(self):
        self.get_thread.stop()
        self.sock.close()
        self.setGuiConnected(False)

    def on_button_connect_clicked(self):
        client_name = self.userName.displayText()
        self.setWindowTitle('Chat client: ' + client_name)

        # TODO: Rewrite - user must enter password
        user_password = 'king'

        self.chat_client = ChatClient('localhost', 5335, client_name)
        # Create TCP socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Create connection with server
        self.chat_client.connect(self.sock)
        self.get_thread = GetMessagesThread(self.chat_client)
        if self.chat_client.check_presence() is True and self.chat_client.authenticate(user_password) is True:
            self.get_thread.start()
            contacts = self.chat_client.get_contacts()
            self.listWidgetContacts.addItems(contacts)
            for item in contacts:
                self.chats[item] = [{0: ''}]

    def on_button_send_clicked(self):
        message_text = self.lineEditMessage.displayText()
        if message_text != '':
            user_to = self.listWidgetContacts.currentItem().text()
            message_time = self.chat_client.send_jim_message(msg=message_text, user_to=user_to)
            final_message = str(message_time) + ' ' + message_text
            self.listWidgetMessages.addItem(final_message)
            self.lineEditMessage.setText('')

    def contacts_current_item_changed(self):
        user_to = self.listWidgetContacts.currentItem().text()
        print('current item: {}'.format(user_to))
        for item in self.chats[user_to]:
            print(item)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(user_name='User1')
    window.show()
    sys.exit(app.exec_())
