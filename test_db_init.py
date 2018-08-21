# test_db_init.py
# Python test for db_init.py

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

from libchat.chat_config import DB_PATH
from db_model import Client, Contact, HistoryLogin, MSHistory
import db_init

GUEST = 'Guest'
OWNER = 'Owner'
TEST_MESSAGE = 'This is test message'
Base = declarative_base()


class TestDb:
    @staticmethod
    def delete_tables(engine):
        Client.__table__.drop(engine)
        Contact.__table__.drop(engine)
        HistoryLogin.__table__.drop(engine)
        MSHistory.__table__.drop(engine)

    def test_db_client(self):

        db_init.create_tables()

        engine = create_engine('sqlite:///' + DB_PATH, echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Client(GUEST)

        session.add(guest_client)
        session.commit()
        result_client = session.query(Client).first().name

        self.delete_tables(engine)

        assert result_client == GUEST

    def test_db_contacts(self):
        db_init.create_tables()

        engine = create_engine('sqlite:///srv_chat.db', echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Client(GUEST)
        owner_client = Client(OWNER)
        session.add_all([guest_client, owner_client])
        session.commit()

        item_contact = Contact(owner_client.id, guest_client.id)
        session.add(item_contact)
        session.commit()

        result_client_id = session.query(Client).first().id
        result_contact = session.query(Contact).filter_by(owner_id=owner_client.id).first()
        result_contact_id = result_contact.id

        self.delete_tables(engine)

        assert result_contact_id == result_client_id

    def test_db_history_login(self):
        db_init.create_tables()

        engine = create_engine('sqlite:///srv_chat.db', echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Client(GUEST)

        session.add(guest_client)
        session.commit()

        history_row = HistoryLogin(guest_client.id, '18:00:25', '192.168.220.29')
        session.add(history_row)
        session.commit()

        result_client_id = session.query(Client).first().id
        result_history = session.query(HistoryLogin).filter_by(client_id=result_client_id).first()

        self.delete_tables(engine)

        assert history_row.id == result_history.id

    def test_db_history_messages(self):
        db_init.create_tables()

        engine = create_engine('sqlite:///srv_chat.db', echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        sender_client = Client(GUEST)
        receiver_client = Client(OWNER)
        session.add_all([sender_client, receiver_client])
        session.commit()

        history_row = MSHistory(sender_client.id, receiver_client.id, time.time(), TEST_MESSAGE)
        session.add(history_row)
        session.commit()

        result_sender_id = session.query(Client).first().id
        result_history = session.query(MSHistory).filter_by(sender_id=result_sender_id).first()

        self.delete_tables(engine)

        assert result_history.message == TEST_MESSAGE