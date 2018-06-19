# client_manager.py
# ClientManager class is responsible for storing and getting info from data base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from lib.config import DB_PATH
from lib import log_config
from db_model import Client, Contact


class ClientManager:
    """
    Class for handling information in data base
    """

    @log_config.logging_dec
    def __init__(self):
        self.engine = create_engine('sqlite:///' + DB_PATH, echo=False)
        Session = sessionmaker(bind=self.engine)
        # Class session creates new objects which bind with data base
        self.session = Session()

    def add_client(self, client_name):
        """
        Storing client to clients table, if client exist do nothing
        :param client_name: user name
        :return: id field from clients table
        """
        res = self.find_by_name(client_name)
        # if client_name doesnt exist in clients table
        if res == -1:
            new_client = Client(client_name)
            self.session.add(new_client)
            self.session.commit()
            id = new_client.id
            return id
        else:
            return res

    def find_by_name(self, client_name):
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

    @log_config.logging_dec
    def get_contacts(self, client_name):
        """
        Gets all client contacts
        :param client_name: Client name which is equivalent in database field clients.name
        :return: list of contacts (may be empty)
        """
        result = {}
        res = self.find_by_name(client_name)
        if res != -1:
            contacts = self.session.query(Contact).filter_by(owner_id=res).all()
            for item in contacts:
                client = self.session.query(Client).filter_by(id=item.friend_id).first()
                result[item.friend_id] = client.name
        return result
