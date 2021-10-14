"""
Module client bot.

Created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import asyncio

from aiogram import types, executor

from aiogram.dispatcher import FSMContext

from config import Config as cfg

from base import Agent as ag
ag.token = cfg.API_TOKEN_CLIENT

from chat import chat_start, chat_communicate, chat_finish

from database import Database

from events import EventBaseModel
from events import show_catalog, create_event
from events import create_event_start, create_event_name, create_event_title, create_event_description, create_event_media, create_event_expiry, create_event_finish
from events import process_callback_btn_create_event_state, process_callback_btn_event
from events import process_callback_btn_more, process_callback_btn_comfirm

from kb import get_menu_keyboard

from languages import local, load_language


@ag.dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_full_name = ''
    if message.from_user.username is not None:
        user_full_name = message.from_user.username
    menu_keyboard = await get_menu_keyboard()
    await message.answer(local('phrases', 'start').format(user_full_name=user_full_name), reply_markup=menu_keyboard, parse_mode="HTML")


@ag.dp.message_handler(commands=['about'])
async def cmd_about(message: types.Message):
    await message.answer(local('about', 'author'), parse_mode="HTML")


@ag.dp.message_handler(content_types=types.ContentTypes.ANY)
async def cmd_menu(message: types.Message, state: FSMContext):
    if local('btn', 'catalog') == message.text:
        await show_catalog(message, state)
    elif local('btn', 'add_event') == message.text:
        await create_event(message)


def main():
    load_language(cfg.lang)
    ag.db = Database(EventBaseModel)
    executor.start_polling(ag.dp, skip_updates=True)


if '__main__' == __name__:
    main()
