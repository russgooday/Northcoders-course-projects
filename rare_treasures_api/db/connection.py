''' Database connection module for SQLAlchemy '''
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker #, Session
from sqlalchemy.exc import SQLAlchemyError
from ..dependencies import ROOT_PATH
from .logger import log_query_time

# Load the environment variables based on the app environment
APP_ENV = os.getenv('APP_ENV', default='dev')
load_dotenv(f'{ROOT_PATH}/.env.{APP_ENV}')
print(f'Environment: {APP_ENV}')

# create a connection URL for SQLAlchemy
CONNECTION_URL = URL.create(
    'postgresql+pg8000',
    username    = os.getenv('PG_USER'),
    password    = os.getenv('PG_PASSWORD'),
    host        = os.getenv('PG_HOST'),
    database    = os.getenv('PG_DATABASE'),
    port        = int(os.getenv('PG_PORT', '5432'))
)

# Create the SQLAlchemy engine
engine = create_engine(CONNECTION_URL, echo=False, hide_parameters=True)
# Create a factory for sessions to be used by the "Residents"
session_local = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    '''
    Standard factory function to provide a session.
    Using a factory is preferred over calling Session(engine) manually every time.
    '''
    return session_local()

def create_connection(logging: str = ''):
    ''' Standard function to create a connection '''
    try:
        if logging:
            log_query_time(f'log.{APP_ENV}.{logging}')
        return engine.connect()
    except SQLAlchemyError as exc:
        print(f'Error during connection: {exc}')
        return None

# def create_session(logging: str = ''):
#     ''' Standard function to create a session '''
#     try:
#         if logging:
#             log_query_time(f'log.{APP_ENV}.{logging}')
#         return Session(engine)
#     except SQLAlchemyError as exc:
#         print(f'Error with session: {exc}')
#         return None
