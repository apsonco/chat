# db_model.py
# Classes for database

from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Clients table from libchat.config.DB_PATH DB
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)
    psw = Column(String(25))

    def __init__(self, name, psw=''):
        self.name = name
        self.psw = psw


# Contacts table from libchat.config.DB_PATH DB
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column('id', Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(Client.id))
    friend_id = Column(Integer, ForeignKey(Client.id))

    def __init__(self, owner_id, friend_id):
        self.owner_id = owner_id
        self.friend_id = friend_id


# History table from libchat.config.DB_PATH DB
class HistoryLogin(Base):
    __tablename__ = 'history_login'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey(Client.id))
    login_time = Column(String(25))
    ip = Column(String(15))

    def __init__(self, client_id, login_time, ip):
        self.client_id = client_id
        self.login_time = login_time
        self.ip = ip


# Message history table from libchat.config.DB_PATH DB
class MSHistory(Base):
    __tablename__ = 'history_ms'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey(Client.id))
    receiver_id = Column(Integer, ForeignKey(Client.id))
    ms_time = Column(Float)
    message = Column(String(500))

    def __init__(self, sender_id, receiver_id, ms_time, message):
        self.sender_id = sender_id
        self.ms_time = ms_time
        self.receiver_id = receiver_id
        self.message = message
