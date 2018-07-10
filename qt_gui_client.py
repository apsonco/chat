from PyQt5 import QtWidgets, uic
import sys
from socket import socket, AF_INET, SOCK_STREAM
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from chat_client import ChatClient


class SockHandler(QObject):
    """
    Input connection handler
    """
    gotData = pyqtSignal(str, str, str)
    finished = pyqtSignal(int)

    def __init__(self, chat_client):
        super().__init__()
        self.chat_client = chat_client
        self.is_Active = False

    def poll(self):
        self.is_Active = True
        while True:
            if not self.is_Active:
                break

            user_from, server_message, str_time = self.chat_client.get_jim_message()

            if server_message:
                self.gotData.emit(user_from, server_message, str_time)
            else:
                break
            #print('{}: {}'.format(user_from, server_message))

        self.finished.emit(0)

    def stop(self):
        self.is_Active = False


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, user_name=None):
        QtWidgets.QWidget.__init__(self, parent)
        uic.loadUi('chat_gui.ui', self)
        self.pushButton.clicked.connect(QtWidgets.qApp.quit)
        self.setWindowTitle('Chat client: ' + user_name)

        self.pushButtonConnect.clicked.connect(self.on_button_connect_clicked)
        self.pushButtonSend.clicked.connect(self.on_button_send_clicked)

        self.sock = None
        self.thread = None
        self.receiver = None
        self.is_active = False
        self.chat_client = None

        self.chats = {}

    def finished(self):
        self.is_active = False
        self.receiver.stop()
        self.sock.close()
        self.setGuiConnected(False)

    def on_button_connect_clicked(self):
        client_name = self.userName.displayText()
        self.setWindowTitle('Chat client: ' + client_name)
        self.chat_client = ChatClient('localhost', 5335, client_name)
        # Create TCP socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        # Create connection with server
        self.chat_client.connect(self.sock)
        if self.chat_client.check_presence() is True:
            contacts = self.chat_client.get_contacts()
            self.listWidgetContacts.addItems(contacts)

            self.receiver = SockHandler(self.chat_client)

            self.thread = QThread()
            self.receiver.moveToThread(self.thread)
            self.receiver.gotData.connect(self.message_received)
            self.thread.started.connect(self.receiver.poll)

            self.receiver.finished.connect(self.thread.quit)
            self.receiver.finished.connect(self.finished)

            self.thread.start()

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

    @pyqtSlot(str, str, str)
    def message_received(self, user_from, message, str_time):
        """
        Reveal messages
        :param message:
        :return:
        """
        # TODO: Should add message_id and storing to DB
        # in this sting we agreed that only one message per minutes
        if user_from in self.chats:
            self.chats[user_from].append({str_time: message})
        else:
            self.chats[user_from] = ({str_time: message},)
        self.listWidgetMessages.addItem(str_time + ' ' + user_from + ' >>' + message)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow(user_name='User1')
    window.show()
    sys.exit(app.exec_())