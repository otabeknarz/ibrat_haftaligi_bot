from aiogram.fsm.state import State, StatesGroup


class SendPostStates(StatesGroup):
    post = State()
