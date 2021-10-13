"""
Database module for bot.

Created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from config import Config as cfg


class Database:

    def __init__(self, base_models):
        self.__engine__ = create_engine(cfg.DB_URL)
        base_models.metadata.create_all(self.__engine__)
        self.__Session__ = sessionmaker(bind=self.__engine__)

    def get_session(self):
        self.session = self.__Session__()
        return self.session
