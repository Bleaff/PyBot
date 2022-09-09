import asyncio
import time

class Chat:
	def __init__(self, chat_id, keyboard_markup):
		self.chat_id = chat_id
		self.keyboard = keyboard_markup
	
	def get_chatId(self):
		return self.chat_id
	
	def set_chatId(self, chat_id):
		self.chat_id = chat_id
	
	def get_markup(self):
		self.keyboard
	
	def set_markup(self, markup):
		self.keyboard = markup

class Timer:
	def __init__(self, name = "Timer", time = 0):
		self.time = time
		self.name = name
	
	async def timer_start(self, func):
		time.sleep(self.time)
		def on_timer_end(func):
			func(self.name)

		
	