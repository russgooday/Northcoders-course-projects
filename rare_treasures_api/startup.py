'''Startup functions for the `Cat's Rare Treasures` FastAPI app.'''

from sqlalchemy import select, func

from rare_treasures_api.db.connection import get_session, APP_ENV
from rare_treasures_api.db.schema import create_tables, drop_tables
from rare_treasures_api.db.seed_mapped import seed_db
from rare_treasures_api.db.tables_classes import Shops

def init_db(env: str = APP_ENV, seed: bool = False) -> tuple[int, int] | None:
    '''
        Initialize the database by creating tables and
        optionally seeding the tables with data.
    '''
    create_tables()

    with get_session() as session:
        with session.begin():
            # Check if the shops table is empty and needs seeding
            count = session.scalar(select(func.count()).select_from(Shops))
            if count == 0 or seed:
                print('Seeding the database...')
                return seed_db(session, env)

    return None

def reset_db(env: str = APP_ENV) -> tuple[int, int] | None:
    '''
        Reset the database by dropping existing tables,
        creating new tables, and seeding the tables with data.
    '''
    drop_tables()
    create_tables()

    with get_session() as session:
        with session.begin():
            return seed_db(session, env)
