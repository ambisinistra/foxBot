from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

#from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy import create_engine
 
from sqlalchemy.orm import sessionmaker
from settings import SQL_ENGINE

Base = declarative_base()


class tg_chats(Base):

    __tablename__ = "welcome_animations.db"

    chat_id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=False)
    animation_link = Column(String)
    welcome_message = Column(String)
    capcha = Column(Boolean)
    begin_date = Column(DateTime)

class tg_messages(Base):

    __tablename__ =  "messages.db"

    inner_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    message_id = Column(Integer)
    chat_id = Column(Integer)
    begin_date = Column(DateTime)
    message_text = Column(String)
    message_status = Column(String)
    

class tg_members(Base):

    __tablename__ =  "members.db"

    inner_id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    chat_id = Column(Integer)
    user_id = Column(Integer)
    status = Column(String)
    message_id = Column(String)
    begin_date = Column(String)


engine = create_engine(SQL_ENGINE)
session = sessionmaker()
session.configure(bind=engine)
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
