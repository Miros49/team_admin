import asyncio
import time

from aiogram import Dispatcher, F, Bot, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import Config, load_config
from database import DataBase
from keyboards import UserKeyboards
from lexicon import *
from state import UserState

from aiocryptopay import AioCryptoPay, Networks

config: Config = load_config('.env')

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

# Инициализируем роутер уровня модуля
router: Router = Router()
config: Config = load_config('.env')
db = DataBase(DATABASE_URL)
storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)
kb = UserKeyboards()


@router.message(F.text == buttons['profile'])
async def profile(message: Message):
    await message.answer(LEXICON_RU['profile'].format(
        user_id=message.from_user.id,
        lolz='',
        tutor='Нет',
        displayed_nickname='',
        status='',
        nickname='',
        current_balance='',
        total_turnover='',
        percent='',
        proxy='',
        numbers='',
        erc='',
        btc='',
        trc='',
        tron=''
    ), reply_markup=kb.profile_kb())


@router.callback_query(F.data == callbacks['🆙 Повысить лимиты'])
async def profile_menu(callback: CallbackQuery):
    await callback.message.answer(callback.data)


@router.callback_query(F.data == callbacks['📝 Изменить информацию'])
async def profile_menu(callback: CallbackQuery):
    await callback.message.answer(callback.data)


@router.callback_query(F.data == callbacks['👛 Привязать кошелек'])
async def profile_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(callback.data)


@router.callback_query(F.data == callbacks['💸 Запросить выплату'])
async def profile_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(callback.data)


@router.callback_query(F.data == callbacks['⭐️ Установить никнейм'])
async def profile_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(callback.data)


@router.callback_query(F.data == callbacks['🫂 Реферальная система'])
async def profile_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(callback.data)


@router.message(F.text == buttons['options'])
async def options_menu(message: Message):
    await message.answer('🔧Инструменты для работы', reply_markup=kb.options)


@router.callback_query(F.data == callbacks['🔗 Получить прокси'])
async def get_proxy(callback: CallbackQuery):
    # TODO: proxy logic
    await callback.message.answer('прокси')


@router.callback_query(F.data == callbacks['📱 Получить номер'])
async def get_number(callback: CallbackQuery):
    # TODO: number logic
    await callback.message.answer('номер')


@router.callback_query(F.data == callbacks['📟 Генераторы'])
async def generators(callback: CallbackQuery):
    # TODO: понять, что это такое
    await callback.message.answer('?')


@router.message(F.text == buttons['current_domain'])
async def domain_menu(message: Message):
    await message.answer(LEXICON_RU['current_domain'], parse_mode='HTML')


@router.message(F.text == buttons['promo'])
async def promo_menu(message: Message):
    await message.answer(LEXICON_RU['your_promo'], reply_markup=kb.promo)


@router.callback_query(F.data == callbacks['🔷 Получить промокод'])
async def get_promo(callback: CallbackQuery):
    await callback.message.answer('промик')  # TODO: что это


@router.callback_query(F.data == callbacks['📈 Статистика промокодов'])
async def promo_statistics(callback: CallbackQuery):
    await callback.message.answer('стата')


@router.callback_query(F.data == callbacks['➕ Добавить промокод'])
async def add_promo(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('добавляй (не работает)')
    # await state.set_state()


@router.message(F.text == buttons['information'])
async def information(message: Message):
    await message.answer(LEXICON_RU['information'])


@router.message(F.text == buttons['tutors'])
async def tutors(message: Message):
    await message.answer(LEXICON_RU['tutors'], reply_markup=UserKeyboards.tutors)


@router.callback_query(F.data == callbacks['📝 Заявка в филиал'])
async def application_to_branch(callback: CallbackQuery):
    await callback.message.answer(LEXICON_RU['dev'])

# @router.callback_query()
# async def temp(callback: CallbackQuery):
#     await callback.message.answer(callback.data)
#
#
# @router.message()
# async def calosbornik(message: Message):
#     if await db.user_exists(message.from_user.id):
#         await message.answer('yes')
#     else:
#         await db.set_user(message.from_user.id)
#         await message.answer('added')
