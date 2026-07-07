from aiogram.fsm.state import StatesGroup, State


class PaymentState(StatesGroup):
    waiting_payment = State()
    waiting_confirmation = State()