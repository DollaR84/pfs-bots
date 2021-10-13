"""
Handlers for events PayForSay Bot.

created on 09.10.2021

@author: Ruslan Dolovanyuk

"""

import datetime

from aiogram import types

from aiogram.dispatcher import FSMContext

from base import Agent as ag

from chat import chat_init

from events.api import get_count_events, read_event_from_db, read_events_from_db, write_event_to_db, delete_event_from_db

from events.fsm import CreateEvent

from events.kb import get_keyboard

from languages import local


async def show_catalog(message: types.Message, state: FSMContext):
    total = await get_count_events()
    offset = 0
    step = 2
    events = await read_events_from_db(offset, step)
    async with state.proxy() as data:
        data['total'] = total
        data['offset'] = offset + step
    await show_events(message, state, events, message.from_user.id)


async def show_event(chat_id, event, kb=None):
    await ag.bot.send_photo(chat_id, event.media)
    await ag.bot.send_message(chat_id, event.title)
    if kb:
        await ag.bot.send_message(chat_id, event.description, reply_markup=kb, parse_mode="HTML")
    else:
        await ag.bot.send_message(chat_id, event.description)


async def show_events(message: types.Message, state: FSMContext, events, user_id):
    for event in events:
        if user_id == event.owner.user_id:
            kb = await get_keyboard(['connect', 'delete'], event.id)
        else:
            kb = await get_keyboard(['connect'], event.id)
        await show_event(message.chat.id, event, kb)
    async with state.proxy() as data:
        if data['offset'] < data['total']:
            kb = await get_keyboard(['+1', '+5'])
            await message.answer(local('phrases', 'more'), reply_markup=kb, parse_mode="HTML")
        else:
            await state.finish()


async def create_event(message: types.Message):
    """Start FSM CreateEvent."""
    kb = await get_keyboard(['cancel'])
    await message.answer(local('phrases', 'create_event'), reply_markup=kb, parse_mode="HTML")
    await CreateEvent.start.set()
    state = ag.dp.current_state(user=message.from_user.id)
    await state.update_data(user_id=message.from_user.id)
    await state.update_data(user_name=message.from_user.username)
    await create_event_start(message, state)


@ag.dp.message_handler(state=CreateEvent.start, content_types=types.ContentTypes.TEXT)
async def create_event_start(message: types.Message, state: FSMContext):
    await message.answer(local('phrases', 'add_name'))
    await CreateEvent.next()


@ag.dp.message_handler(state=CreateEvent.name, content_types=types.ContentTypes.TEXT)
async def create_event_name(message: types.Message, state: FSMContext):
    if message.text == '':
        return
    await state.update_data(event_name=message.text)
    await message.answer(local('phrases', 'add_title'))
    await CreateEvent.next()


@ag.dp.message_handler(state=CreateEvent.title, content_types=types.ContentTypes.TEXT)
async def create_event_title(message: types.Message, state: FSMContext):
    if message.text == '':
        return
    await state.update_data(event_title=message.text)
    await message.answer(local('phrases', 'add_description'))
    await CreateEvent.next()


@ag.dp.message_handler(state=CreateEvent.description, content_types=types.ContentTypes.TEXT)
async def create_event_description(message: types.Message, state: FSMContext):
    if message.text == '':
        return
    await state.update_data(event_description=message.text)
    await message.answer(local('phrases', 'add_media'))
    await CreateEvent.next()


@ag.dp.message_handler(state=CreateEvent.media, content_types=types.ContentTypes.PHOTO)
async def create_event_media(message: types.Message, state: FSMContext):
    if not message.photo:
        return
    await state.update_data(event_media=message.photo[0].file_id)
    kb = await get_keyboard(['empty'])
    await message.answer(local('phrases', 'date_expiry'), reply_markup=kb, parse_mode="HTML")
    await CreateEvent.next()


@ag.dp.message_handler(state=CreateEvent.expiry, content_types=types.ContentTypes.TEXT)
async def create_event_expiry(message: types.Message, state: FSMContext):
    if message.text != '':
        try:
            dt_list = message.text.split(' ')
            date = datetime.date(*[int(x) for x in list(reversed(dt_list[0].split('.')))])
            time = datetime.time(*[int(x) for x in dt_list[1].split(':')]) if (len(dt_list) > 1) else None
            dt = datetime.combine(date, time) if time else date
        except:
            return
        else:
            await state.update_data(date_expiry=dt)
    else:
        await state.update_data(date_expiry=None)
    await CreateEvent.next()
    await create_event_finish(message, state)


@ag.dp.message_handler(state=CreateEvent.finish, content_types=types.ContentTypes.TEXT)
async def create_event_finish(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await write_event_to_db(data)
    await ag.bot.send_photo(message.chat.id, data['event_media'])
    await message.answer(data['event_title'])
    await message.answer(data['event_description'])
    await message.answer(local('phrases', 'finish_create_event1'))
    await message.answer(local('phrases', 'finish_create_event2'))
    await state.finish()


@ag.dp.callback_query_handler(lambda c: c.data, state=[CreateEvent.start, CreateEvent.name, CreateEvent.title, CreateEvent.description, CreateEvent.media, CreateEvent.expiry])
async def process_callback_btn_create_event_state(callback_query: types.CallbackQuery, state: FSMContext):
    if 'btn_empty' == callback_query.data:
        await state.update_data(date_expiry=None)
        await CreateEvent.next()
        await create_event_finish(callback_query.message, state)
    elif 'btn_cancel' == callback_query.data:
        await callback_query.message.answer(local('phrases', 'create_event_cancel'))
        await state.finish()


@ag.dp.callback_query_handler(lambda c: c.data in ['btn_+1', 'btn_+5'])
async def process_callback_btn_more(callback_query: types.CallbackQuery, state: FSMContext):
    step = int(callback_query.data.split('+')[1])
    async with state.proxy() as data:
        events = await read_events_from_db(data['offset'], step)
        await state.update_data(offset=data['offset'] + step)
        await show_events(callback_query.message, state, events, callback_query.from_user.id)


@ag.dp.callback_query_handler(lambda c: c.data.startswith('btn_connect') or c.data.startswith('btn_delete'))
async def process_callback_btn_event(callback_query: types.CallbackQuery, state: FSMContext):
    btn, index = callback_query.data.split('=')
    index = int(index)
    if 'btn_connect' == btn:
        event = await read_event_from_db(index)
        await chat_init(callback_query.message, callback_query.from_user.id, event)
    elif 'btn_delete' == btn:
        kb = await get_keyboard(['yes', 'no'], index)
        await callback_query.message.answer(local('phrases', 'del_question'), reply_markup=kb)


@ag.dp.callback_query_handler(lambda c: c.data.startswith('btn_yes') or c.data.startswith('btn_no'))
async def process_callback_btn_comfirm(callback_query: types.CallbackQuery, state: FSMContext):
    btn, index = callback_query.data.split('=')
    index = int(index)
    if 'btn_yes' == btn:
        await delete_event_from_db(index)
        await callback_query.message.answer(local('phrases', 'del_ok'))
    elif 'btn_no' == btn:
        await callback_query.message.answer(local('phrases', 'del_cancel'))
