# test_utils.py
# Pytests for utils.py

import json

import utils
import config


# Test for dict_to_bytes function

origin_json = {'action': 'presence',
               'time': 1526794194.570375,
               'type': 'status',
               'user': {'account_name': 'My_first',
                        'status': 'Hey! I am online'}}


class TestCoding:

    # Test for result encoded type
    def test_encoded_type(self):
        result_message = utils.dict_to_bytes(origin_json)
        assert isinstance(result_message, bytes)

    # Test for correctness
    def test_dict_to_bytes(self):
        result_message = utils.dict_to_bytes(origin_json)
        decoded_message = result_message.decode(config.CHARACTER_ENCODING)
        test_message = json.loads(decoded_message)
        assert origin_json == test_message
