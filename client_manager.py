# client_manager.py
# ClientManager class is responsible for storing and getting info from data base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.config import DB_PATH
from db_model import Client


class ClientManager:

    def __init__(self):
        self.engine = create_engine('sqlite:///' + DB_PATH, echo=True)
        Session = sessionmaker(bind=self.engine)
        # Class session creates new objects which bind with data base
        self.session = Session()

    def add_client(self, client_name):
        """
        Storing client to clients table, if client exist do nothing
        :param client_name: user name
        :return: id field from clients table
        """
        res = self.find(client_name)
        # if client_name doesnt exist in clients table
        if res == -1:
            new_client = Client(client_name)
            self.session.add(new_client)
            self.session.commit()
            id = new_client.id
            return id
        else:
            return res

    def find(self, client_name):
        """
        Check client_name exist in clients table
        :param client_name:
        :return: record id if exist, -1 otherwise
        """
        res = self.session.query(Client).filter_by(name=client_name).first()
        if res is None:
            return -1
        else:
            return res.id

    def get_contacts(self, client_name):
        """
        Gets all client contacts
        :param client_name: Client name which is equivalent in database field clients.name
        :return: list of contacts (may be empty)
        """
        res = self.find(client_name)
        if res == -1:
            result = ()
        else:
            result = {'1': 'test_user'}
        return result
