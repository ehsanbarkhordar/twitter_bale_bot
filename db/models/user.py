from sqlalchemy import Column, String, Boolean, BigInteger

from constant.message import ReadyText
from balebot.utils.logger import Logger

from db.base import Base, db_persist, session

logger = Logger.get_logger()


class User(Base):
    __tablename__ = 'users'
    peer_id = Column(BigInteger, primary_key=True)
    access_hash = Column(String, nullable=False)
    twitter_user_id = Column(String, nullable=False)
    screen_name = Column(String, nullable=False)
    oauth_token = Column(String, nullable=False)
    oauth_token_secret = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)

    def __init__(self, peer_id, access_hash, twitter_user_id, screen_name, oauth_token, oauth_token_secret):
        self.peer_id = peer_id
        self.access_hash = access_hash

        self.twitter_user_id = twitter_user_id
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    @classmethod
    @db_persist
    def add_new_user(cls, new_user):
        result = cls.get_user_by_peer_id(new_user.peer_id)
        if result:
            return ReadyText.register_before
        else:
            session.add(new_user)
            return new_user

    @classmethod
    @db_persist
    def get_user_by_peer_id(cls, peer_id):
        return session.query(cls).filter(cls.peer_id == peer_id).one_or_none()
