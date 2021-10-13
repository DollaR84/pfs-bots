"""
FSM for events PayForSay Bot.

created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram.dispatcher.filters.state import State, StatesGroup


class CreateEvent(StatesGroup):
    start: State = State()
    name: State = State()
    title: State = State()
    description: State = State()
    media: State = State()
    expiry: State = State()
    finish: State = State()
