from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import create_engine
 
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.sql.schema import ForeignKey
from settings import SQL_ENGINE

Base = declarative_base()


class tg_chats(Base):

    __tablename__ = "welcome_animations.db"

    chat_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=False)
    animation_link = Column(String)
    welcome_message = Column(String)
    capcha = Column(Boolean)

    tg_members = relationship("tg_members", back_populates="tg_chats")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class tg_members(Base):

    __tablename__ =  "members.db"

    inner_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    chat_id = Column(Integer, ForeignKey(tg_chats.chat_id), nullable=True)
    user_id = Column(Integer)
    status = Column(String)

    # primaryjoin="User.id == Post.user_id"

    tg_chats = relationship("tg_chats", back_populates="tg_members")
    tg_messages_chat_id = relationship("tg_messages", foreign_keys=[chat_id], back_populates="tg_members", 
                                    primaryjoin="tg_members.chat_id == tg_messages.chat_id")
    tg_messages_user_id = relationship("tg_messages", foreign_keys=[user_id], back_populates="tg_members",
                                    primaryjoin="tg_members.user_id == tg_messages.user_id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class tg_messages(Base):

    __tablename__ =  "messages.db"

    inner_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    message_id = Column(Integer)
    chat_id = Column(Integer, ForeignKey(tg_members.chat_id), nullable=True)
    user_id = Column(Integer, ForeignKey(tg_members.user_id), nullable=True)
    message_text = Column(String)
    message_status = Column(String)

    tg_member_chat_id = relationship("tg_members", foreign_keys=[chat_id], back_populates="tg_messages",
                                    primaryjoin="tg_messages.chat_id == tg_members.chat_id")
    tg_member_user_id = relationship("tg_members", foreign_keys=[user_id], back_populates="tg_messages",
                                    primaryjoin="tg_messages.user_id == tg_members.user_id")

    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    

engine = create_engine(SQL_ENGINE, echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)

class SQLchatGreatings():

    def delete_record(self, chat_id: int):
        pass

    def update_record(self, chat_id: int, animation_link="", welcome_text="", capcha=None):
        pass


class SQLmembers():

    def add_member(self, chat_id:int, user_id:int, status:str, message_id:int):
        pass

    def delete_record(self, chat_id: int, user_id: int):
        pass

    def check_old_messages(self, time_diff : str, status="awaiting"):
        pass


class SQLmessages():

    def record_by_type(self, chat_id : int, message_type : str):
        pass

    def check_old_messages(self, time_diff : str):
        pass

    def insert_record(self, chat_id: int, message_id: int, message_text="", message_type="default"):
        pass

    def delete_record(self, chat_id: int, message_id: int):
        pass
