import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder, KeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram import F
from database import init_db, add_user, user_exists
from camera import take_photo
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

if not API_TOKEN:
    raise ValueError("No TELEGRAM_API_TOKEN provided in .env file")

logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация базы данных
init_db()

# Кнопка для получения фото
button_photo = InlineKeyboardButton(text='Photo', callback_data='get_photo')
builder = InlineKeyboardBuilder([[button_photo]])
markup = InlineKeyboardMarkup(inline_keyboard=builder.export())

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    logging.info(f"Received /start command from user {message.from_user.id}")
    if user_exists(message.from_user.id):
        await message.answer("Вы уже зарегистрированы.", reply_markup=markup)
    else:
        add_user(message.from_user.id)
        await message.answer("Добро пожаловать! Вы зарегистрированы.", reply_markup=markup)
    logging.info(f"Handled /start command for user {message.from_user.id}")

# Обработчик нажатия кнопки "Photo"
@dp.callback_query(lambda callback_query: callback_query.data == 'get_photo')
async def send_photo(callback_query: types.CallbackQuery):
    logging.info(f"Photo button clicked by user {callback_query.from_user.id}")
    photo_path = take_photo()
    with open(photo_path, 'rb') as photo:
        await callback_query.message.answer_photo(photo)
    logging.info(f"Sent photo to user {callback_query.from_user.id}")

async def main():
    logging.info("Starting bot")
    await dp.start_polling(bot, skip_updates=True)
    logging.info("Bot started")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())