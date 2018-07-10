# db_model.py
# Classes for database

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Clients table from lib.config.DB_PATH DB
class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String(25), unique=True)

    def __init__(self, name):
        self.name = name


# Contacts table from lib.config.DB_PATH DB
class Contact(Base):
    __tablename__ = 'contacts'
    id = Column('id', Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey(Client.id))
    friend_id = Column(Integer, ForeignKey(Client.id))

    def __init__(self, owner_id, friend_id):
        self.owner_id = owner_id
        self.friend_id = friend_id
