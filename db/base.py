import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main_config import Config, logger

db_string = Config.db_string
engine = create_engine(db_string)
Base = declarative_base()
session = sessionmaker(engine)
session = session()


def create_tables():
    Base.metadata.create_all(engine)
    return True


def db_persist(func):
    def persist(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            session.commit()
            logger.debug("database model function called: " + func.__name__)
            return res
        except SQLAlchemyError as e:
            logger.exception(e.args)
            session.rollback()
            return False

    return persist
