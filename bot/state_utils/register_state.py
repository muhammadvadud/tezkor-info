from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    wait_phone = State()
