# server_db_manager.py
# ClientManager class is responsible for storing and getting info from data base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging

from lib.config import DB_PATH
from lib.log_config import log
from db_model import Client, Contact


class ServerDbManager:
    """
    Class for handling information in data base
    """

    @log
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
        res = self.session.query(Client).filter(Client.name == client_name).first()
        if res is None:
            return -1
        else:
            return res.id

    @log
    def get_contacts(self, client_name):
        """
        Gets all client contacts
        :param client_name: Client name which is equivalent in database field clients.name
        :return: list of contacts (may be empty)
        """
        result = {}
        res = self.find_by_name(client_name)
        if res != -1:
            contacts = self.session.query(Contact).filter(Contact.owner_id == res).all()
            for item in contacts:
                client = self.session.query(Client).filter(Client.id == item.friend_id).first()
                result[item.friend_id] = client.name
        return result

    @log
    def add_contact(self, client_name, contact_name):
        """
        Add new contact to Contact table
        :param client_name:
        :param contact_name:
        :return: False if client or contact doesn't exist, True if information stored
        """
        client_id = self.find_by_name(client_name)
        contact_id = self.find_by_name(contact_name)
        client = self.session.query(Client).filter(Client.name == client_name).first()
        contact = self.session.query(Client).filter(Client.name == contact_name).first()
        logging.info('{} client_id: {}, {} contact_id: {}'.format(client_name, client_id, contact_name, contact_id))
        if client_id == -1 or contact_id == -1:
            result = False
        else:
            logging.info('Add_contact. Enter to Else')
            new_contact = Contact(owner_id=client.id, friend_id=contact.id)
            logging.info('Add_contact. Created new_contact {}'.format(new_contact))
            self.session.add(new_contact)
            logging.info('Add_contact. Contact added to session')
            self.session.commit()
            logging.info('Add_contact. Session committed')
            result = True
        return result

    @log
    def del_contact(self, client_name, contact_name):
        """
        Delete contact from Contact table
        :param client_name:
        :param contact_name:
        :return: False if client or contact doesn't exist, True if information stored
        """
        logging.info('User: {} wants delete contact {}'.format(client_name, contact_name))
        client_id = self.find_by_name(client_name)
        contact_id = self.find_by_name(contact_name)
        if client_id == -1 or contact_id == -1:
            result = False
        else:
            contact_record = self.session.query(Contact).filter(Contact.owner_id == client_id,
                                                                Contact.friend_id == contact_id).first()
            self.session.delete(contact_record)
            logging.info('Del_contact. Contact deleted in session')
            self.session.commit()
            logging.info('Del_contact. Session committed')
            result = True
        return result

