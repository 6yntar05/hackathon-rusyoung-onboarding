#!/bin/env python3
import sys

import logging
logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import aiogram.utils.markdown as fmt
from aiogram.dispatcher import FSMContext

from utils.token import token_get
API_TOKEN = token_get()

#dbhost, dbport, dbuser, dbpasswd, dbname
#import database.py

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

#Start Message
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Стажер","HR","Руководитель"]
    keyboard.add(*buttons)
    await message.answer("Приветствую 👋, ты используешь бота Росмолодежи, выбери себе роль!", reply_markup=keyboard)



@dp.message_handler(regexp='(^Стажер)')
async def youngcmd_start(message: types.Message):
    await message.answer('Отлично! Привет, мой друг давай раскажи себе о себе напиши в сообщении /create')
    #await create_profile(user_id=message.from_user.id)

if __name__ == '__main__':
    dbacc = sys.argv[1]
    # host:port@user:passwd
    dbhost = dbacc.split(":")[0]
    dbport = dbacc.split(":")[1].split("@")[0]
    dbuser = dbacc.split(":")[1].split("@")[1]
    dbpasswd = dbacc.split(":")[2]

    print(dbhost, dbport, dbuser, dbpasswd)

    executor.start_polling(dp, skip_updates=True)