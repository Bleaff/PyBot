import asyncio
import time
from functools import wraps


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

# def timer_start(func):
# 	time.sleep(self.time)
# 	def on_timer_end(func):
# 		func(self.name, self.time)
# 	return on_timer_end(func)

class Timer:
	def __init__(self, name = "Timer", time = 0):
		self.time = time
		self.name = name
	@staticmethod
	async def start_timer(func):
		@wraps(func)

		def wrapper(arg):
			rg = "check"
			return func(arg)
		return await wrapper
	
	@start_timer
	async def test(self, timer = None):
		print(f"Timer '{self.name}' starts")
		await time.sleep(self.time)
		print(f"{self.name} set on {self.time} sec and ends")


if __name__ == "__main__":
	t1 = Timer("Tasks", 15)
	t2 = Timer("Easy", 3)

	loop = 	asyncio.get_event_loop()
	asyncio.ensure_future(t1.test())
	asyncio.ensure_future(t2.test())
	loop.run_until_complete([t1.test(), t2.test()])
	print("Main")
