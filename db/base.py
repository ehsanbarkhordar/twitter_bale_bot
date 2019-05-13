from balebot.utils.logger import Logger
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from main_config import DatabaseConfig

db_string = DatabaseConfig.db_string
engine = create_engine(db_string)
Base = declarative_base()
session = sessionmaker(engine)
session = session()

logger = Logger.get_logger()


def create_tables():
    Base.metadata.create_all(engine)
    return True


def db_persist(func):
    def persist(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            session.commit()
            logger.info("success calling db func: " + func.__name__)
            return res
        except SQLAlchemyError as e:
            logger.error(e.args)
            session.rollback()
            return False

    return persist
