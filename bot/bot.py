#!/bin/env python3
import sys

import logging
logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from utils.token import token_get
API_TOKEN = token_get()

#dbhost, dbport, dbuser, dbpasswd, dbname
#import database.py

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    kb = [
        [
            types.KeyboardButton(text="Стажер"),
            types.KeyboardButton(text="HR"),
            types.KeyboardButton(text="Ментор")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Приветствую 👋, ты используешь бота Росмолодежи, выбери себе роль!", reply_markup=keyboard)

# INLINE TEST
inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
@dp.message_handler(commands=['1'])
async def process_command_1(message: types.Message):
    await message.reply("Первая инлайн кнопка", reply_markup=inline_kb1)

@dp.callback_query_handler(text="button1")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer("Aboba")
    await callback.answer(
        text="Спасибо, что воспользовались ботом!",
        show_alert=True
    )
    # или просто await call.answer()

@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await message.reply_photo(photo, caption='Cats are here 😺')

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)

if __name__ == '__main__':
    dbacc = sys.argv[1]
    # host:port@user:passwd
    dbhost = dbacc.split(":")[0]
    dbport = dbacc.split(":")[1].split("@")[0]
    dbuser = dbacc.split(":")[1].split("@")[1]
    dbpasswd = dbacc.split(":")[2]

    print(dbhost, dbport, dbuser, dbpasswd)

    executor.start_polling(dp, skip_updates=True)