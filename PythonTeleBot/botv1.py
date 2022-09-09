import telebot
from telebot import types

myBot = telebot.TeleBot("5319467602:AAHt1plxDpMvmPlwKvjqqqlpPZ8qfDju6iE")


	

@myBot.message_handler(commands=['start'])
def show_start_menu(message):
	markup = types.ReplyKeyboardMarkup()
	btn_start = types.KeyboardButton("Start timer")
	btn_setup = types.KeyboardButton("Set Up")
	markup.add(btn_start,btn_setup)
	myBot.reply_to(message, "Choose some option")

@myBot.message_handler(content_types="text")
def operate_commands(message):
	pass
@myBot.message_handler(commands=[]])
def show_start_menu(message):
	
myBot.infinity_polling()