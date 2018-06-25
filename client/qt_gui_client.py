from PyQt5 import QtWidgets, uic, QtGui
import sys
from socket import socket, AF_INET, SOCK_STREAM
import logging

from chat_client import ChatClient


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, user_name=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('chat_gui.ui', self)
        self.pushButton.clicked.connect(QtWidgets.qApp.quit)
        self.setWindowTitle('Chat client: ' + user_name)

        self.pushButtonConnect.clicked.connect(self.on_button_connect_clicked)
        self.pushButtonSend.clicked.connect(self.on_button_send_clicked)

    def on_button_connect_clicked(self):
        client_name = self.userName.displayText()
        self.setWindowTitle('Chat client: ' + client_name)
        chat_client = ChatClient('localhost', 5335, client_name)
        # Create TCP socket
        with socket(AF_INET, SOCK_STREAM) as sock:
            # Create connection with server
            chat_client.connect(sock)
            if chat_client.check_presence() is True:
                contacts = chat_client.get_contacts()
                self.listWidgetContacts.addItems(contacts)

    def on_button_send_clicked(self):
        message_text = self.lineEditMessage.displayText()
        if message_text != '':
            client_name = self.userName.displayText()
            self.setWindowTitle('Chat client: ' + client_name)
            chat_client = ChatClient('localhost', 5335, client_name)
            # Create TCP socket
            with socket(AF_INET, SOCK_STREAM) as sock:
                # Create connection with server
                chat_client.connect(sock)
                if chat_client.check_presence() is True:
                    user_to = self.listWidgetContacts.currentItem().text()
                    message_time = chat_client.send_jim_message(msg=message_text, user_to=user_to)
                    # Receive server message
                    # logging.info('Try get message from '.format(chat_client.get_socket()))
                    # user_from, server_message = chat_client.get_jim_message()
            final_message = str(message_time) + ' ' + message_text
            self.listWidgetMessages.addItem(final_message)
            self.lineEditMessage.setText('')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(user_name='User1')
    window.show()
    sys.exit(app.exec_())