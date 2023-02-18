#!/bin/env python3
import sys

import logging
logging.basicConfig(level=logging.INFO)
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.markdown as fmt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from utils.token import token_get
from  database import sqlite_db
import random
from aiogram.contrib.fsm_storage.memory import MemoryStorage

API_TOKEN = token_get()
#dbhost, dbport, dbuser, dbpasswd, dbname
#import database.py

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class UsersStateGroup(StatesGroup):
    last_name = State()
    frist_name = State()
    date = State()

async def on_startup(_):
    print('Бот онлайн')
    sqlite_db.sql_start()


#Start Message
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):


    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Сотрудник"]
    keyboard.add(*buttons)
    await message.answer("Приветствую 👋, ты используешь бота Росмолодежи, выбери роль!", reply_markup=keyboard)



@dp.message_handler(regexp='(^Сотрудник)')
async def youngcmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Зарегаться"]
    keyboard.add(*buttons)
    await message.answer('Привет ты, в системе зарегистрируейся!',reply_markup=keyboard)

    #await create_profile(user_id=message.from_user.id)

@dp.message_handler(regexp='(^Зарегаться)')
async def create_profile(message: types.Message):
    await sqlite_db.create_profile(id=message.from_user.id)
    await message.reply("Хорошо, давай начнем введи свою Фамилию:")
    await UsersStateGroup.last_name.set()

@dp.message_handler(state=UsersStateGroup.last_name)
async def last_name_in_db(message: types.Message, state:FSMContext):
    async with state.proxy() as data:
        data['last_name'] = message.text

    await  message.reply('Теперь как тебя зовут:')
    await UsersStateGroup.next()

@dp.message_handler(state=UsersStateGroup.frist_name)
async def first_name_in_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['first_name'] = message.text

    await  message.reply('Теперь введи свою дату рождения:')
    await UsersStateGroup.next()

@dp.message_handler(state=UsersStateGroup.date)
async def date_in_db(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['daterod'] = message.text
    await sqlite_db.edit_profile(state, id=message.from_user.id)
    await message.reply('Акк создан!')
    await state.finish()




if __name__ == '__main__':
    dbacc = sys.argv[1]
    # host:port@user:passwd
    dbhost = dbacc.split(":")[0]
    dbport = dbacc.split(":")[1].split("@")[0]
    dbuser = dbacc.split(":")[1].split("@")[1]
    dbpasswd = dbacc.split(":")[2]

    print(dbhost, dbport, dbuser, dbpasswd)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)