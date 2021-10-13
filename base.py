"""
Base module for bots.

Created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import logging

import asyncio

from aiogram import Bot, Dispatcher

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.contrib.middlewares.logging import LoggingMiddleware


logging.basicConfig(level=logging.INFO)


class AgentMeta(type):

    @property
    def token(cls):
        return cls.__token__

    @token.setter
    def token(cls, API_TOKEN: str):
        cls.__token__ = API_TOKEN
        cls.bot = Bot(token=cls.__token__)
        storage = MemoryStorage()
        cls.dp = Dispatcher(cls.bot, loop=asyncio.get_event_loop(), storage=storage)
        cls.dp.middleware.setup(LoggingMiddleware())


class Agent(metaclass=AgentMeta):
    bot = None
    dp = None
