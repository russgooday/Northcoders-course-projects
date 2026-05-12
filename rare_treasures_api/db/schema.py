'''
    This module contains the functions to create and drop the tables in the database.
    It is used by the `run_seed` function to create the tables before seeding the database.
'''

from .connection import engine
from .tables_classes import Base

def create_tables():
    '''Create the tables in the database'''
    Base.metadata.create_all(engine)


def drop_tables():
    '''Drop the tables in the database'''
    Base.metadata.drop_all(engine)
