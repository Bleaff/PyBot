import telebot
from telebot import types
import asyncio




class MyTimer:
	def __init__(self):
		
		self._timers_ = list()
		self._tasks_ = list()
		self.loop = asyncio.get_event_loop()

	def _convertTime_(self, time:str):
		seconds = 0
		splited_time = time.split(":")
		for i, t in enumerate(reversed(splited_time)):
		    seconds += int(t) * (60 ** i)
		return seconds

	def append(self, name="default", time_str="0:10", chatId = 0):
		self._tasks_.append(self.loop.create_task(add_timer(name, self._convertTime_(time_str), chatId)))
		self._timers_.append([name, time_str, False, chatId])
		print(self._timers_)

	def __countActive__(self):
		count_active = 0
		for el in self._timers_:
			if el[2] == True:
				count_active += 1
		return count_active

	async def __ready_to_go__(self):
		for i, task in enumerate(self._tasks_):
			if self._timers_[i][2] != True:
				await task
				self._timers_[i][2] = True
		print("To complete ready ", self.__countActive__())

	def start_timers(self):
		self.loop.run_until_complete(self.__ready_to_go__())
	
	def get_logs(self, chatId):
		msg = ""
		for row in self._timers_:
			if chatId == row[3]:
				msg += addAllString(row[0]) + " " + row[1] + ", был ли он запущен:"+ str(row[2])+"\n"
		myBot.send_message(chatId, f"Ваша таймерная история такова:\n{msg}")


myBot = telebot.TeleBot("5319467602:AAHt1plxDpMvmPlwKvjqqqlpPZ8qfDju6iE")
myTimer = MyTimer()

async def add_timer(name, time, chatId):
	await asyncio.sleep(time)
	Summary = ""
	for i in name:
		Summary += i + " "
	nSum = Summary[0].upper() + Summary[1:]
	myBot.send_message(chatId, f"Таймер {Summary}завершен через {time} секунд!")

def spliter(msg:str):
	splited = msg.lower().split()
	return splited

def parser(msg):
	array_from_msg = spliter(msg.text)
	name = array_from_msg[1:-1]
	time = array_from_msg[-1]
	return name, time, msg.chat.id

def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    SetTimer = types.KeyboardButton(text="Установить таймер")
    RunTimer = types.KeyboardButton(text="Запустить")
    InfoTimers = types.KeyboardButton(text="Посмотреть использованные таймеры")
    keyboard.add(SetTimer, RunTimer, InfoTimers)
    return keyboard

@myBot.message_handler(commands=['start'])
def show_start_menu(message):
	OptionKey = start_keyboard()
	myBot.send_message(message.chat.id, "Выберите раздел", reply_markup=OptionKey)

@myBot.message_handler(content_types="text")
def operate_commands(message):
	if message.text == "Установить таймер":
		myBot.send_message(message.chat.id, "Для установки таймера отправьте мне сообщение с названием таймера и его продолжительностью как в примере ниже:")
		myBot.send_message(message.chat.id, "'Таймер Простоять в планке 3:15' ,где 3 это минуты, а 15 секунды")
		myBot.send_message(message.chat.id, "В таком и только таком формате! Иначе могу понять неправильно...")
		myBot.send_message(message.chat.id, "Для запуска таймера напишите мне одно слово: 'Запустить' и мы поймем друг друга. Кстати, перед этим можно добавить несколько задач:)")

	elif spliter(message.text)[0] == "таймер":
		myTimer.append(*parser(message))
	elif message.text == "Запустить":
		myTimer.start_timers()
	elif spliter(message.text)[0] == "посмотреть":
		myTimer.get_logs(message.chat.id)
	else:
		myBot.send_message(message.chat.id, "Неопознанные слова. Выберите команду из списка или задайте таймер.")


def addAllString(array:list):
	Summary = ""
	for i in array:
		Summary += i + " "
	return Summary

myBot.infinity_polling()