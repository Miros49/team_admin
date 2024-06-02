import asyncio

from aiogram import Bot, Router
from aiogram.filters import StateFilter, CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from config_data import Config, load_config
from database import DataBase
from filters import PrivateChat
from keyboards import StartKeyboards, UserKeyboards
from lexicon import LEXICON_RU
from state import UserState

config: Config = load_config('.env')
DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
# Инициализируем роутер уровня модуля
router: Router = Router()
db = DataBase(DATABASE_URL)
bot: Bot = Bot(token=config.tg_bot.token)
kb = StartKeyboards()

router.message.filter(PrivateChat())


@router.message(CommandStart())
async def create_ads(message: Message, state: FSMContext):
    if not await db.get_user(message.from_user.id):
        await message.answer(LEXICON_RU['create_profile'][0])
        await state.set_state(UserState.create_profile_1)
    else:
        await message.answer(LEXICON_RU['accept user'], reply_markup=UserKeyboards.menu)


@router.message(StateFilter(UserState.create_profile_1))
async def ads_title(message: Message, state: FSMContext):
    profile_info = dict()
    profile_info['lolz_profile'] = message.text
    await message.answer(LEXICON_RU['create_profile'][1])
    await state.set_state(UserState.create_profile_2)
    await state.update_data(profile_info=profile_info)


@router.message(StateFilter(UserState.create_profile_2))
async def set_link(message: Message, state: FSMContext):
    data = await state.get_data()
    profile_info = data['profile_info']
    profile_info['work_exp'] = message.text
    await message.answer(LEXICON_RU['create_profile'][2])
    await state.set_state(UserState.create_profile_3)
    await state.update_data(profile_info=profile_info)


@router.message(StateFilter(UserState.create_profile_3))
async def set_link(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.clear()
    profile_info = data['profile_info']
    profile_info['work_time'] = message.text
    await message.answer(LEXICON_RU['create_profile'][3])
    for admin_id in config.tg_bot.admin_ids:
        await bot.send_message(
            admin_id,
            LEXICON_RU['profile to admin'].format(
                username=message.from_user.username,
                user_id=message.from_user.id,
                lolz_profile=profile_info['lolz_profile'],
                work_exp=profile_info['work_exp'],
                work_time=profile_info['work_time']),
            reply_markup=kb.accept_user(message.from_user.id), parse_mode='HTML'
        )
