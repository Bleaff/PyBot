import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from database import init_db, add_user, user_exists
from camera import take_photo

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Инициализация базы данных
init_db()

# Кнопка для получения фото
button_photo = KeyboardButton('Фото')
markup = ReplyKeyboardMarkup().add(button_photo)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if user_exists(message.from_user.id):
        await message.reply("Вы уже зарегистрированы.", reply_markup=markup)
    else:
        add_user(message.from_user.id)
        await message.reply("Добро пожаловать! Вы зарегистрированы.", reply_markup=markup)

@dp.message_handler(lambda message: message.text == "Фото")
@dp.message_handler(commands=['photo'])
async def send_photo(message: types.Message):
    photo_path = take_photo()
    with open(photo_path, 'rb') as photo:
        await message.reply_photo(photo)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)