# db_init.py
# Use this script for creating tables in srv_chat.db (sqlite database which comes empty)

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

metadata = MetaData()
clients_table = Table('clients', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('name', String(25))
                      )

engine = create_engine('sqlite:///srv_chat.db', echo=True)
metadata.create_all(engine)

contact_table = Table('contacts', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('id_owner', Integer, ForeignKey(clients_table.c.id)),
                      Column('id_friend', Integer, ForeignKey(clients_table.c.id))
                      )
metadata.create_all(engine)
