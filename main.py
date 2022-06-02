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

PARS_DATA = []
PARS_DATA_CACHE = []
cache_platform_list = []


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Стартовое сообщение, ожидание нажатия кнопки с выбором платформы """
    await message.answer("Выберите платформу для которой хотите спарсить игры.", reply_markup=menu.inline_kb1)
    await Storage_value.storage_input_platform.set()


@dp.callback_query_handler(text='ps3', state=Storage_value.storage_input_platform)
@dp.callback_query_handler(text='xbox360', state=Storage_value.storage_input_platform)
async def process_callback_btn_game(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка нажатия кнопки и запрос на ввод диапазона цен"""
    platform = callback_query.data
    chat_id = callback_query.message.chat.id
    await bot.send_message(text=callback_query.data, chat_id=chat_id)
    await state.update_data(storage_input_platform=platform)
    await bot.send_message(text="Введите диапазон цены через запятую (например '200,400')", chat_id=chat_id)
    await Storage_value.storage_input_price.set()


@dp.message_handler(state=Storage_value.storage_input_price)
async def input_price(message: types.Message, state: FSMContext):
    """Преобразование цены из строки в кортеж, вызов логики парсинга"""
    price = message.text.split(',')
    chat_id = message.chat.id
    platform = await state.get_data()
    await state.update_data(storage_input_price=price)
    if len(price) == 2 and (price[0].isdigit() and price[1].isdigit()):
        await bot.send_message(text='Выполняется поиск, подождите...', chat_id=message.chat.id)
        await parse_func(platform['storage_input_platform'])
        await service_logic(chat_id, price=price)
        await bot.send_message(text='Нажмите на /start чтобы начать сначала', chat_id=message.chat.id)

    else:
        await bot.send_message(text='Неправильно введен диапазон цен.Нажмите на /start чтобы начать сначала',
                               chat_id=message.chat.id)
    await state.finish()


async def parse_func(platform):
    """ Вызов функции парсинга, запуск один раз на платформу """
    global PARS_DATA, PARS_DATA_CACHE, cache_platform_list
    if platform not in cache_platform_list:
        cache_platform_list.insert(0, platform)
        PARS_DATA_CACHE = parse(cache_platform_list[0])
        PARS_DATA = PARS_DATA_CACHE
    else:
        PARS_DATA = PARS_DATA_CACHE


async def service_logic(chat_id, price):
    """Фильтрация спарсенных данных"""
    flag = False
    for game in PARS_DATA:
        if game["availability"] != "Закончились" and int(price[0]) <= int(game["price"]) <= int(
                price[1]):  # Игры должны быть в наличии и в нужном ценовом диапазоне
            await bot.send_message(
                text=f'Название игры: {game["title"]} цена {game["price"]} наличие {game["availability"]}',
                chat_id=chat_id)
            flag = True
    if flag is False:
        await bot.send_message(text='Ничего не найдено', chat_id=chat_id)


if __name__ == '__main__':
    executor.start_polling(dp)
