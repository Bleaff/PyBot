#!/usr/bin/python

import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.types import FSInputFile
from aiogram.filters import Command
from aiogram import F
from database import init_db, add_user, user_exists
from camera import take_photo
from dotenv import load_dotenv
from aiogram.fsm.context import FSMContext
from registration import FormRegistration

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')
REGISTRATION_PASSWORD = os.getenv('REGISTRATION_PASSWORD')

if not API_TOKEN:
    raise ValueError("No TELEGRAM_API_TOKEN provided in .env file")
if not REGISTRATION_PASSWORD:
    raise ValueError("No REGISTRATION_PASSWORD provided in .env file")

logging.basicConfig(level=logging.DEBUG)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Кнопка для получения фото
button_photo = InlineKeyboardButton(text='Photo', callback_data='get_photo')
builder = InlineKeyboardBuilder([[button_photo]])
markup = InlineKeyboardMarkup(inline_keyboard=builder.export())

reply_button = KeyboardButton(text="Photo")
rbuilder = ReplyKeyboardBuilder([[reply_button]])
reply_markup = ReplyKeyboardMarkup(keyboard=rbuilder.export())

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message, state=FSMContext):
    logging.info(f"Received /start command from user {message.from_user.id}")
    logging.info(f"Current state is {await state.get_state()}")
    logging.info(f"User exists: {user_exists(message.from_user.id)}")
    await message.answer("Добро пожаловать! Вы можете зарегистрироваться. Используйте команду /registration.\n Вы можете проверить свой аккаунт, используя команду /is_registered.")
    if user_exists(message.from_user.id):
        await state.set_state(FormRegistration.AllReady)
        await message.answer("Вы уже зарегистрированы.", reply_markup=markup)
    logging.info(f"Handled /start command for user {message.from_user.id}")

# Обработчик нажатия кнопки "Registration"
@dp.message(Command('registration'))
async def registration(message: types.Message, state=FSMContext):
    logging.info(f"Registration button clicked by user {message.from_user.id}")
    logging.info(f"Current state is {await state.get_state()}")
    logging.info(f"User exists: {user_exists(message.from_user.id)}")
    if user_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы.", reply_markup=reply_markup)
        await state.set_state(FormRegistration.AllReady)
    else:
        await message.answer("Пожалуйста, введите пароль для регистрации:")
        await state.set_state(FormRegistration.WaitingPassword)
    logging.info(f"Handled registration button for user {message.from_user.id}")

@dp.message(Command('is_registered'))
async def is_registered(message: types.Message, state=FSMContext):
    logging.info(f"Registration button clicked by user {message.from_user.id}")
    logging.info(f"Current state is {await state.get_state()}")
    logging.info(f"User exists: {user_exists(message.from_user.id)}")
    if user_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы.", reply_markup=markup)
    else:
        await message.answer("Вы ещё не зарегистрированы.")

@dp.message(FormRegistration.WaitingPassword, F.text == REGISTRATION_PASSWORD)
async def registration_password(message: Message, state=FSMContext):
    state_now = await state.get_state()
    logging.info(f"Current state is {state_now}")
    logging.info(f"Message from: {message.from_user.id}")
    logging.info(f"User exists: {user_exists(message.from_user.id)}")
    if state_now == FormRegistration.AllReady:
        await message.answer("Аккаунт уже зарегистрирован!", reply_markup=reply_markup)
        return
    if state_now == FormRegistration.WaitingPassword and str(message.text) == str(REGISTRATION_PASSWORD):
            await message.answer("Вы успешно зарегистрированы!", reply_markup=reply_markup)
            await state.set_state(FormRegistration.AllReady)
            add_user(message.from_user.id)
    else:
        logging.info(f"Was expected password {REGISTRATION_PASSWORD}, but got {message.text}")
        await message.answer("Неправильный пароль. Попробуйте ещё раз.")

# Обработчик нажатия кнопки "Photo"
@dp.callback_query(lambda callback_query: callback_query.data == 'get_photo')
async def send_photo(callback_query: types.CallbackQuery, state=FSMContext):
    state_now = await state.get_state()
    logging.info(f"Current state is {state_now}")
    if not state_now == FormRegistration.AllReady:
        await callback_query.answer("Вы ещё не зарегистрированы")
    else:
        logging.info(f"Photo button clicked by user {callback_query.from_user.id}")
        photo_path = take_photo()
        await callback_query.message.reply_photo(FSInputFile(photo_path), reply_markup=reply_markup)
        logging.info(f"Sent photo to user {callback_query.from_user.id}")


@dp.message(FormRegistration.AllReady, F.text == 'Photo')
async def send_photo(message: Message, state=FSMContext):
    state_now = await state.get_state()
    logging.info(f"Current state is {state_now}")
    if not state_now == FormRegistration.AllReady:
        await message.answer("Вы ещё не зарегистрированы")
    else:
        logging.info(f"Photo button clicked by user {message.from_user.id}")
        photo_path = take_photo()
        await message.reply_photo(FSInputFile(photo_path), reply_markup=reply_markup)
        logging.info(f"Sent photo to user {message.from_user.id}")

async def main():
    logging.info("Starting bot")
    await dp.start_polling(bot, skip_updates=True)
    logging.info("Bot started")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())