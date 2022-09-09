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
	