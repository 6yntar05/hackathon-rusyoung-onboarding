#!/bin/env python3
import sys

import logging

logging.basicConfig(level=logging.INFO)
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
import aiogram.utils.markdown as fmt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from utils.token import token_get
from database import sqlite_db
import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_TOKEN = token_get()
# dbhost, dbport, dbuser, dbpasswd, dbname
# import database.py

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserStateGroup(StatesGroup):
    new_user = State()
    last_name = State()
    first_name = State()
    date = State()
    registrated_user = State()


async def on_startup(_):
    print('Бот онлайн')
    sqlite_db.sql_start()


# Start Message
@dp.message_handler(commands='start')
async def send_welcome(message: types.Message):
    await UserStateGroup.new_user.set()
    user_id = message.from_user.id
    if await sqlite_db.is_user_logged_in(user_id):
        await UserStateGroup.registrated_user.set()
        await message.reply('Переход в личный кабинет. Напиши /restart для работы')
    else:
        await sqlite_db.create_profile(id=message.from_user.id)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Сотрудник"]
        keyboard.add(*buttons)
        await UserStateGroup.next()
        await message.answer("Приветствую 👋, ты используешь бота Росмолодежи, выбери роль!", reply_markup=keyboard)


@dp.message_handler(state=UserStateGroup.last_name)
async def create_profile(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await message.reply('Теперь как тебя зовут:')
    await UserStateGroup.next()


@dp.message_handler(state=UserStateGroup.first_name)
async def first_name_in_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await  message.reply('Теперь введи свою дату рождения:')
    await UserStateGroup.next()


@dp.message_handler(state=UserStateGroup.date)
async def date_in_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['daterod'] = message.text
    await sqlite_db.edit_profile(state, id=message.from_user.id)
    await message.reply('Аккаунт успешно создан! для рестарта напишите /restart')
    # await state.finish()
    await UserStateGroup.next()
    # await message.answer('State has been set to registrated_user')




@dp.message_handler(text='(^(Список задач))')
async def spisok_zadac(message: types.Message, state: FSMContext):
    await message.reply("Твой список задач:"
                         "Сходить поговорить с руководителем"
                         "Познакомиться с колективом"
                         "Сделать проект на Django")

@dp.message_handler(text='(^(Контакты руководителей))')
async def spisok_zadac(message: types.Message, state: FSMContext):
        await message.reply("Контакты руководителей:"
                             "Пушкин SEO: 88005553535"
                             "Катя-руководитель back-end: 87452487887")

@dp.message_handler(text='(^(Основная документация))')
async def spisok_zadac(message: types.Message, state: FSMContext):
    await message.reply("Вся основная документация находится по ссылке: https://youthbit.nya.pub")


@dp.message_handler(state=UserStateGroup.registrated_user)
async def registrated_user(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Список задач", "Контакты руководителей", "Основная документация"]
    keyboard.add(*buttons)
    await message.reply('Добро пожаловать в личный кабинет сотрудника!', reply_markup=keyboard)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)