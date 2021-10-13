"""
Keyboards for events PayForSay Bot.

created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram import types

from languages import local


async def get_keyboard(phrases: list, event_id=None):
    keyboard = types.InlineKeyboardMarkup(row_width=len(phrases))
    phrases = {phrase: f'btn_{phrase}' for phrase in phrases}
    for check_phrase in ['connect', 'delete', 'yes', 'no']:
        if event_id and (check_phrase in phrases):
            phrases[check_phrase] += f'={event_id}'
    keyboard.add(*[types.InlineKeyboardButton(local('btn', phrase), callback_data=data) for phrase, data in phrases.items()])
    return keyboard
