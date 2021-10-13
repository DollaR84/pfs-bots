"""
Keyboards for chat PayForSay Bot.

created on 12.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram import types

from languages import local


async def get_menu_keyboard():
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, selective=True)
    menu_keyboard.add(
        types.KeyboardButton(local('btn', 'close_chat')),
        types.KeyboardButton(local('btn', 'show_event'))
    )
    return menu_keyboard


async def get_menu_name_keyboard(name: str):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, selective=True)
    menu_keyboard.add(
        types.KeyboardButton(local('btn', 'close_chat_name').format(user_full_name=name))
    )
    return menu_keyboard


async def get_answer_name_keyboard(name: str, event_name: str, event_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(local('btn', 'answer_name').format(user_full_name=name), callback_data=f'btn_answer={event_id}'),
        types.InlineKeyboardButton(text=local('btn', 'show_event_name').format(event_name=event_name), url=f"https://t.me/PfsDRIBot?start={event_id}")
    )
    return keyboard


async def get_answer_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton(local('btn', 'answer'), callback_data=f'btn_answer={user_id}'),
        types.InlineKeyboardButton(local('btn', 'show_event'), callback_data='btn_show_event')
    )
    return keyboard
