# test_jimmessage.py
# Python tests for JIMMessage.py

import pytest

from jim.JIMMessage import *
from libchat import chat_config


class TestMessages:

    def test_presence_message(self):
        mess = JIMMessage.presence_message('test_user')
        assert KEY_ACTION in mess and KEY_TIME in mess and KEY_TYPE in mess and KEY_USER in mess

    def test_presence_message_key_action(self):
        mess = JIMMessage.presence_message('test_user')
        assert mess[KEY_ACTION] == chat_config.VALUE_PRESENCE

    def test_presence_message_default_user(self):
        mess = JIMMessage.presence_message()
        assert mess[chat_config.KEY_USER][chat_config.KEY_ACCOUNT_NAME] == chat_config.VALUE_DEFAULT_USER

    def test_presence_message_type(self):
        with pytest.raises(TypeError):
            JIMMessage.presence_message(123)

    def test_presence_message_long_user_name(self):
        with pytest.raises(UsernameTooLongError):
            JIMMessage.presence_message('123456789012345678901234567')