import asyncio
import telebot



myBot = telebot.TeleBot("5319467602:AAHt1plxDpMvmPlwKvjqqqlpPZ8qfDju6iE")

async def add_timer(name, time, chatId):
	await asyncio.sleep(time)
	myBot.send_message(chatId, f"Таймер {name} завершен через {time} секунд!")

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
		self._timers_.append([name, time_str, False])

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




# timer = Timer()
# test = 	[["f", "0:15"],
# 		["s", "0:9"],
# 		["third", "0:5"],
# 		["fourth", "0:11"]]
# for t in test:
# 	timer.append(*t)
# print("alles ist gut")
# timer.start_timers()
# print("end first")
# timer.append("Giga", "0:3")
# timer.start_timers()
# print("Start second")
# test = 	[["1", "0:17"],
# 		["2", "0:25"],
# 		["4", "1:40"],
# 		["3", "1:13"]]
# for t in test:
# 	timer.append(*t)
# timer.start_timers()
