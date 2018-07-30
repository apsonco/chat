# test_db_init.py
# Python test for db_init.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from libchat.chat_config import DB_PATH
import db_init

GUEST = 'Guest'
OWNER = 'Owner'
Base = declarative_base()


class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(25))

    def __init__(self, name):
        self.name = name


class Contacts(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(Clients.id))
    friend_id = Column(Integer, ForeignKey(Clients.id))

    def __init__(self, owner_id, friend_id):
        self.owner_id = owner_id
        self.friend_id = friend_id


class History(Base):
    __tablename__ = 'history'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey(Clients.id))
    login_time = Column(String(25))
    ip = Column(String(15))

    def __init__(self, client_id, login_time, ip):
        self.client_id = client_id
        self.login_time = login_time
        self.ip = ip


class TestDb:
    def test_db_client(self):

        db_init.create_tables()

        engine = create_engine('sqlite:///' + DB_PATH, echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Clients(GUEST)

        session.add(guest_client)
        session.commit()
        result_client = session.query(Clients).first().name

        Clients.__table__.drop(engine)
        Contacts.__table__.drop(engine)

        assert result_client == GUEST

    def test_db_contacts(self):
        db_init.create_tables()

        engine = create_engine('sqlite:///srv_chat.db', echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Clients(GUEST)
        owner_client = Clients(OWNER)
        session.add_all([guest_client, owner_client])
        session.commit()

        item_contact = Contacts(owner_client.id, guest_client.id)
        session.add(item_contact)
        session.commit()

        result_client_id = session.query(Clients).first().id
        result_contact = session.query(Contacts).filter_by(owner_id=owner_client.id).first()
        result_contact_id = result_contact.id

        Clients.__table__.drop(engine)
        Contacts.__table__.drop(engine)

        assert result_contact_id == result_client_id

    def test_db_history(self):
        db_init.create_tables()

        engine = create_engine('sqlite:///srv_chat.db', echo=True)
        # Create session
        Session = sessionmaker(bind=engine)
        # Class session creates new objects which bind with data base
        session = Session()
        # Need add User class object to session for storing it
        guest_client = Clients(GUEST)

        session.add(guest_client)
        session.commit()

        history_row = History(guest_client.id, '18:00:25', '192.168.220.29')
        session.add(history_row)
        session.commit()

        result_client_id = session.query(Clients).first().id
        result_history = session.query(History).filter_by(client_id=result_client_id).first()

        assert history_row.id == result_history.id
