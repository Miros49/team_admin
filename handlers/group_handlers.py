import asyncio
from pprint import pprint

from aiogram import Dispatcher, F, Bot, Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import Message, CallbackQuery, FSInputFile, ChatMemberUpdated
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramRetryAfter

from config_data import Config, load_config
from database import DataBase
from filters import NewMember
from keyboards import UserKeyboards
from lexicon import *
from state import UserState
from utils import *


config: Config = load_config('.env')

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

router: Router = Router()
config: Config = load_config('.env')
db = DataBase(DATABASE_URL)
storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)

router.message.filter()
router.callback_query()


@router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def new_user(event: ChatMemberUpdated):
    if await db.user_exists(event.from_user.id):
        # await bot.send_message(event.from_user.id, 'Hi!')
        pass


@router.message(NewMember())
async def test(message: Message):
    await message.delete()
