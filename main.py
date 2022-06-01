from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import bot_token
from aiogram import Bot, Dispatcher, executor, types
from parser import parse
import menu
from states import Storage_value

bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Выберите платформу для которой хотите спарсить игры.", reply_markup=menu.inline_kb1)
    await Storage_value.storage_input_platform.set()


@dp.callback_query_handler(text='ps3', state=Storage_value.storage_input_platform)
@dp.callback_query_handler(text='xbox360', state=Storage_value.storage_input_platform)
async def process_callback_btn_game(callback_query: types.CallbackQuery, state: FSMContext):
    platform = callback_query.data
    chat_id = callback_query.message.chat.id
    await bot.send_message(text=callback_query.data, chat_id=chat_id)
    await state.update_data(storage_input_platform=platform)
    await bot.send_message(text="Введите сумму", chat_id=chat_id)
    await Storage_value.storage_input_price.set()



@dp.message_handler(state=Storage_value.storage_input_price)
async def input_price(message: types.Message, state: FSMContext):
    price = message.text
    chat_id = message.chat.id
    platform = await state.get_data()
    await state.update_data(storage_input_price=price)
    await service_logic(chat_id, platform['storage_input_platform'], price)





async def service_logic(chat_id, platform, price):
    for game in parse(platform=platform, price=price):
        if game["availability"] != "Закончились" and game["price"] == price:
            await bot.send_message(
                text=f'Название игры: {game["title"]} цена {game["price"]} наличие {game["availability"]}',
                chat_id=chat_id)


if __name__ == '__main__':
    executor.start_polling(dp)
