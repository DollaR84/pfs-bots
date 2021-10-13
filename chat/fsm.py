"""
FSM for chat PayForSay Bot.

created on 12.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class Chating(StatesGroup):
    start: State = State()
    communicate: State = State()
    finish: State = State()
