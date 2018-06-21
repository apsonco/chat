# config.py
#
# Configuration file for jim protocol use

CHARACTER_ENCODING = 'utf-8'
DB_PATH = 'srv_chat.db'

KEY_RESPONSE = 'response'
KEY_TIME = 'time'
KEY_ALERT = 'alert'
KEY_ACTION = 'action'
KEY_TYPE = 'type'
KEY_USER = 'user'
KEY_ACCOUNT_NAME = 'account_name'
KEY_STATUS = 'status'
KEY_TO = 'to'
KEY_FROM = 'from'
KEY_ENCODING = 'encoding'
KEY_MESSAGE = 'message'
KEY_QUANTITY = 'quantity'
KEY_USER_ID = 'user_id'

VALUE_PRESENCE = 'presence'
VALUE_QUIT = 'quit'
VALUE_STATUS_DEFAULT = 'status'
VALUE_MESSAGE = 'msg'
VALUE_GET_CONTACTS = 'get_contacts'
VALUE_ADD_CONTACT = 'add_contact'
VAlUE_DEL_CONTACT = 'del_contact'
VALUE_CONTACT_LIST = 'contact_list'
VALUE_DEFAULT_USER = 'Guest'

HTTP_CODE_OK = 200
HTTP_CODE_ACCEPTED = 202
HTTP_CODE_WRONG_ORDER = 400
HTTP_CODE_SERVER_ERROR = 500

STR_PRESENCE_RECEIVED = 'Presence received'
STR_ONLINE = 'Hey! I am online'
STR_ORDER_WITHOUT_PRESENCE = '''Server received order without 'presence' key '''
STR_QUIT = 'Good bye!'

DEFAULT_PORT = 5335
DEFAULT_SERVER_IP_LISTENING_ADDRESS = ''

SERVER = 'server'
