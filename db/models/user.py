from sqlalchemy import Column, String, Boolean

from constant.message import ReadyText
from db.base import Base, db_persist, session


class User(Base):
    __tablename__ = 'users'
    bale_id = Column(String, primary_key=True)
    bale_username = Column(String, nullable=False)
    twitter_user_id = Column(String, nullable=False)
    screen_name = Column(String, nullable=False)
    access_token = Column(String, nullable=False)
    access_token_secret = Column(String, nullable=False)
    is_premium = Column(Boolean, default=False)

    def __init__(self, bale_id, bale_username, twitter_user_id, screen_name, access_token, access_token_secret):
        self.bale_id = bale_id
        self.bale_username = bale_username
        self.twitter_user_id = twitter_user_id
        self.screen_name = screen_name
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    @classmethod
    @db_persist
    def add_new_user(cls, new_user):
        result = cls.get_user_by_user_id(new_user.bale_id)
        if result:
            return ReadyText.register_before
        else:
            session.add(new_user)
            return new_user

    @classmethod
    @db_persist
    def get_user_by_user_id(cls, bale_id: str):
        return session.query(cls).filter(cls.bale_id == bale_id).one_or_none()
