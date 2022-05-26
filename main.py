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


@dp.callback_query_handler(text='ps3')
@dp.callback_query_handler(text='xbox360')
async def process_callback_btn_game(callback_query: types.CallbackQuery):
    for game in parse(platform=callback_query.data, price=400):
        if game["availability"] != "Закончились" and game["price"] == '400':
            await callback_query.message.answer(f'Название игры: {game["title"]} цена {game["price"]} наличие {game["availability"]}' )


if __name__ == '__main__':
    executor.start_polling(dp)
