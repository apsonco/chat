import sys
import logging

from PyQt5 import QtWidgets, QtGui, uic, QtCore
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread

from client.chat_client import ChatClient
from libchat.chat_config import *
from libchat.log_config import log
from libchat import utils

UNREAD_COLOR = '#fdc086'


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
                str_time = utils.light_time(jim_message[KEY_TIME])
                message = jim_message[KEY_MESSAGE]
                print('{} {}: {}'.format(jim_message[KEY_TIME], jim_message[KEY_FROM], jim_message[KEY_MESSAGE]))
                # write message to history list, first parameter 1 point on user_from, 0 - local user
                if user_from in window.chats:
                    logging.info('Have found user {} in contacts '.format(user_from))
                    window.chats[user_from].append((1, str_time, message))
                else:
                    # Received first message from user_from
                    # TODO: Should change to .append
                    window.chats[user_from] = [(1, str_time, message)]
                # if we have received message from current contact item
                if user_from == window.listWidgetContacts.currentItem().text():
                    window.listWidgetMessages.addItem(str_time + ' ' + user_from + ' > ' + message)
                else:
                    items = window.listWidgetContacts.findItems(user_from, QtCore.Qt.MatchExactly)
                    if len(items) > 0:
                        for item in items:
                            item.setBackground(QtGui.QColor(UNREAD_COLOR))
                    #window.highlight_contact(user_from)
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

        self.sock = None
        self.get_thread = None
        self.chat_client = None

        self.chats = {}
        self.previous_contact_item = None

        self.pushButtonConnect.clicked.connect(self.on_button_connect_clicked)
        self.pushButtonSend.clicked.connect(self.on_button_send_clicked)
        self.pushButtonAddContact.clicked.connect(self.on_button_add_contact_clicked)
        self.pushButtonDeleteContact.clicked.connect(self.on_button_delete_contact_clicked)

        self.listWidgetContacts.currentItemChanged.connect(self.contacts_current_item_changed)

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
                # first item should be 2 for skipping first item in contacts_current_item_changed function
                self.chats[item] = [(2, 0, '')]

    def on_button_send_clicked(self):
        message_text = self.lineEditMessage.displayText()
        if message_text != '':
            user_to = self.listWidgetContacts.currentItem().text()
            message_time = self.chat_client.send_jim_message(msg=message_text, user_to=user_to)
            final_message = str(message_time) + ' ' + message_text
            self.listWidgetMessages.addItem(final_message)
            self.lineEditMessage.setText('')
            # write message to history list, first parameter 0 - local user, 1 - user_to
            if user_to in window.chats:
                logging.info('Message {} wrote to {} '.format(message_text, user_to))
                window.chats[user_to].append((0, message_time, message_text))
            else:
                # Received first message from user_from
                window.chats[user_to] = ((0, message_time, message_text),)

    def on_button_add_contact_clicked(self):
        contact_name = self.addContactName.displayText()
        if contact_name != '':
            result = self.chat_client.add_contact(contact_name)
            if result is True:
                self.listWidgetContacts.addItem(contact_name)
                # create history for this contact
                self.chats[contact_name] = [(2, 0, '')]
            else:
                logging.info('Add contact return False')
            self.addContactName.clear()

    def on_button_delete_contact_clicked(self):
        contact_name = self.listWidgetContacts.currentItem().text()
        if contact_name != '':
            result = self.chat_client.del_contact(contact_name)
            if result is True:
                self.listWidgetContacts.takeItem(self.listWidgetContacts.row(self.listWidgetContacts.currentItem()))
            else:
                logging.info('Delete contact return False')
        pass

    def contacts_current_item_changed(self):
        user_to = self.listWidgetContacts.currentItem().text()
        logging.info('current item: {}'.format(user_to))
        if self.previous_contact_item and self.previous_contact_item != user_to:
            self.listWidgetMessages.clear()
            for item in self.chats[user_to]:
                if item[0] is 0:
                    final_message = str(item[1]) + ' ' + item[2]
                else:
                    final_message = str(item[1]) + ' ' + user_to + ' > ' + item[2]
                if item[0] != 2:
                        self.listWidgetMessages.addItem(final_message)
                logging.info(item)

        self.previous_contact_item = user_to

    def highlight_contact(self, user_from):
        """
        Finds item by name in contact list and highlights it.
        Use this method for new messages.
        :param user_from: Contact name
        :return:
        """
        logging.info('change background in list')
        items = self.listWidgetContacts.findItems(user_from, QtCore.Qt.MatchExactly)
        if len(items) > 0:
            for item in items:
                item.setBackground(QtGui.QColor(UNREAD_COLOR))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(user_name='User1')
    window.show()
    sys.exit(app.exec_())
