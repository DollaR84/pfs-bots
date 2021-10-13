"""
Module service bot.

Created on 12.10.2021

@author: Ruslan Dolovanyuk

"""

import asyncio

from aiogram import types, executor

from aiogram.dispatcher import FSMContext

from config import Config as cfg

from base import Agent as ag
ag.token = cfg.API_TOKEN_SERVICE

from chat import chat_init
from chat import chat_start, chat_communicate, chat_finish

from database import Database

from events import read_event_from_db
from events import EventBaseModel

from languages import local, load_language


@ag.dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    user_full_name = ''
    if message.from_user.username is not None:
        user_full_name = message.from_user.username
    await message.answer(local('phrases', 'start').format(user_full_name=user_full_name))


@ag.dp.message_handler(commands=['about'])
async def cmd_about(message: types.Message):
    await message.answer(local('about', 'author'), parse_mode="HTML")


@ag.dp.callback_query_handler(lambda c: c.data.startswith('btn_answer'))
async def process_callback_btn_event(callback_query: types.CallbackQuery, state: FSMContext):
    btn, index = callback_query.data.split('=')
    index = int(index)
    if 'btn_answer' == btn:
        event = await read_event_from_db(index)
        await chat_init(callback_query.message, callback_query.from_user.id, event, callback_query.from_user.username)


def main():
    load_language(cfg.lang)
    ag.db = Database(EventBaseModel)
    executor.start_polling(ag.dp, skip_updates=True)


if '__main__' == __name__:
    main()
