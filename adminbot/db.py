"""Helper class to get a database engine and to get a session."""
from adminbot.config import config
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

pollbot_engine = create_engine(
    config["database"]["pollbot_sql_uri"],
    pool_size=config["database"]["pollbot_connection_count"],
    max_overflow=config["database"]["pollbot_overflow_count"],
    echo=False,
)
pollbot_base = declarative_base(bind=pollbot_engine)


def get_pollbot_session(connection=None):
    """Get a new db session."""
    session = scoped_session(sessionmaker(bind=pollbot_engine))
    return session
