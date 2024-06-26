from aiogram.fsm.state import State, StatesGroup

class FormRegistration(StatesGroup):
	WaitingPassword = State()
	AllReady = State()
