# test_utils.py
# Python tests for utils.py

import json
import socket

from libchat import utils, chat_config

import pytest


# Test for dict_to_bytes function

origin_json = {'action': 'presence',
               'time': 1526794194.570375,
               'type': 'status',
               'user': {'account_name': 'My_first',
                        'status': 'Hey! I am online'}}
origin_bytes = b'{"action": "presence",' \
               b' "time": 1526794194.570375,' \
               b' "type": "status",' \
               b' "user": {"account_name": "My_first",' \
                        b' "status": "Hey! I am online"}}'


class TestCoding:

    # Test for encoded result type
    def test_encoded_type(self):
        result_message = utils.dict_to_bytes(origin_json)
        assert isinstance(result_message, bytes)

    # Test for correctness
    def test_dict_to_bytes(self):
        result_message = utils.dict_to_bytes(origin_json)
        decoded_message = result_message.decode(chat_config.CHARACTER_ENCODING)
        test_message = json.loads(decoded_message)
        assert origin_json == test_message

    # Test for decoded result type
    def test_decoded_type(self):
        result_message = utils.dict_from_bytes(origin_bytes)
        assert isinstance(result_message, dict)


class TestMessages:

    def test_response_presence(self):
        mess = utils.response_presence()
        assert chat_config.KEY_RESPONSE in mess and chat_config.KEY_TIME in mess and chat_config.KEY_ALERT in mess

    def test_presence_message(self):
        mess = utils.presence_message('test_user')
        assert chat_config.KEY_ACTION in mess and chat_config.KEY_TIME in mess and chat_config.KEY_TYPE in mess \
               and chat_config.KEY_USER in mess

    def test_presence_message_key_action(self):
        mess = utils.presence_message()
        assert mess[chat_config.KEY_ACTION] == chat_config.VALUE_PRESENCE

    def test_presence_message_default_user(self):
        mess = utils.presence_message()
        assert mess[chat_config.KEY_USER][chat_config.KEY_ACCOUNT_NAME] == chat_config.VALUE_DEFAULT_USER

    def test_presence_message_type(self):
        with pytest.raises(TypeError):
            utils.presence_message(123)

    def test_presence_message_long_user_name(self):
        with pytest.raises(utils.UsernameTooLongError):
            utils.presence_message('123456789012345678901234567')


# Integration tests
# Class stub for socket operations
class ClientSocket():
    """Class-stub for socket operations"""

    def __init__(self, sock_type=socket.AF_INET, sock_family=socket.SOCK_STREAM):
        pass

    def recv(self, n):
        #   Will send the same answer for socket
        message = {chat_config.KEY_RESPONSE: chat_config.HTTP_CODE_OK}
        jmessage = json.dumps(message)
        bmessage = jmessage.encode(chat_config.CHARACTER_ENCODING)
        return bmessage

    def send(self, bmessage):
        #   You may redefine send method
        pass


def test_get_message(monkeypatch):
    # Change original socket for our stub class
    monkeypatch.setattr("socket.socket", ClientSocket)
    # Create socket that changed already
    sock = socket.socket()
    assert utils.get_message(sock) == {chat_config.KEY_RESPONSE: chat_config.HTTP_CODE_OK}


def test_send_message(monkeypatch):
    # Change original socket for our stub class
    monkeypatch.setattr("socket.socket", ClientSocket)
    # Create socket that changed already
    sock = socket.socket()
    # Should check that method work, because it dosn't have return
    assert utils.send_message(sock, {'test': 'test'}) is None
    # And check for dictionary in parameter
    with pytest.raises(TypeError):
        utils.send_message(sock, 'test')
