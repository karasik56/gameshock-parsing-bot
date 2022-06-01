from aiogram.dispatcher.filters.state import StatesGroup, State


class Storage_value(StatesGroup):
    storage_input_price = State()
    storage_input_platform = State()
