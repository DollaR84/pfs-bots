"""
Models for events PayForSay Bot.

created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import datetime

from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String, Text
from sqlalchemy import DateTime

from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False, unique=True)
    full_name = Column(String(100))


class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(100), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    media = Column(String(100), nullable=False)
    created = Column(DateTime(), default=datetime.datetime.now)
    expiry = Column(DateTime())
    owner = relationship('User', backref='events')
