"""
Handlers for chat PayForSay Bot.

created on 12.10.2021

@author: Ruslan Dolovanyuk

"""

from aiogram import types

from aiogram.dispatcher import FSMContext

from base import Agent as ag

from chat.api import get_another_token, is_client_bot, is_service_bot

from chat.fsm import Chating

from chat.kb import get_chat_menu_keyboard, get_chat_menu_name_keyboard, get_chat_answer_name_keyboard, get_chat_answer_keyboard

from kb import get_menu_keyboard

from languages import local


async def chat_init(message, owner_id, user_id, username, event):
    await Chating.start.set()
    state = ag.dp.current_state(user=owner_id)
    await state.update_data(user_id=user_id)
    await state.update_data(username=username)
    await state.update_data(event=event)
    await chat_start(message, state)


async def chat_close(message, state):
    await Chating.next()
    await chat_finish(message, state)


@ag.dp.message_handler(state=Chating.start, content_types=types.ContentTypes.ANY)
async def chat_start(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if is_client_bot(ag.token):
            kb = await get_chat_menu_keyboard()
            await message.answer(local('phrases', 'chat_start').format(event_title=data['event'].title), reply_markup=kb, parse_mode="HTML")
        else:
            kb = await get_chat_menu_name_keyboard(data['username'])
            await message.answer(local('phrases', 'chat_service_start').format(user_full_name=data['username']), reply_markup=kb, parse_mode="HTML")
    await Chating.next()


@ag.dp.message_handler(state=Chating.communicate, content_types=types.ContentTypes.ANY)
async def chat_communicate(message: types.Message, state: FSMContext):
    press_btn = await check_buttons(message, state)
    if press_btn:
        return
    token = get_another_token(ag.token)
    client = is_client_bot(ag.token)
    async with state.proxy() as data:
        with ag.bot.with_token(token):
            if client:
                kb = await get_chat_answer_name_keyboard(message.from_user.id, message.from_user.username, data['event'].name, data['event'].event_id)
                await ag.bot.send_message(data['event'].owner_id, local('phrases', 'chat_client_write').format(event_title=data['event'].title, user_full_name=message.from_user.username, text=message.text), reply_markup=kb)
            else:
                kb = await get_chat_answer_keyboard(data['event'].owner_id, data['event'].event_id)
                await ag.bot.send_message(data['user_id'], local('phrases', 'chat_service_write').format(event_name=data['event'].name, text=message.text), reply_markup=kb)


@ag.dp.message_handler(state=Chating.finish, content_types=types.ContentTypes.ANY)
async def chat_finish(message: types.Message, state: FSMContext):
    await state.finish()


async def check_buttons(message: types.Message, state: FSMContext):
    result = False
    if local('btn', 'show_event') == message.text:
        from events import show_event
        result = True
        async with state.proxy() as data:
            await show_event(message, data['event'])
    elif message.text.endswith('show_event'):
        from events import show_event
        result = True
        index = int(message.text.split(' ')[1].split(':')[0])
        await show_event(message, index)
    elif message.text.startswith(local('btn', 'close_chat')):
        await chat_close(message, state)
        result = True
        if is_client_bot(ag.token):
            kb = await get_menu_keyboard()
            await message.answer(local('phrases', 'chat_close'), reply_markup=kb)
        else:
            await message.answer(local('phrases', 'chat_close_name').format(user_full_name=message.from_user.username), reply_markup=types.ReplyKeyboardRemove(), parse_mode="HTML")
    return result
