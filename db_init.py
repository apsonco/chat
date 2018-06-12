# db_init.py
# Use this script for creating tables in srv_chat.db (sqlite database which comes empty)

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


def create_tables():
    metadata = MetaData()
    clients_table = Table('clients', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('name', String(25))
                          )

    contact_table = Table('contacts', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('owner_id', Integer, ForeignKey(clients_table.c.id)),
                          Column('friend_id', Integer, ForeignKey(clients_table.c.id))
                          )
    engine = create_engine('sqlite:///srv_chat.db', echo=True)
    metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()