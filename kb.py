"""
Module main keyboard bot.

Created on 13.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram import types

from languages import local, load_language


async def get_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, selective=True)
    menu_keyboard.add(
        types.KeyboardButton(local('btn', 'catalog')),
        types.KeyboardButton(local('btn', 'add_event'))
    )
    return menu_keyboard
