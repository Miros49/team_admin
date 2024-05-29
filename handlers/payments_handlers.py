import asyncio
import io
import time

import aiofiles
from aiogram import Dispatcher, F, Bot, Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import Config, load_config
from database import DataBase
from filters import Payment
from keyboards import UserKeyboards
from lexicon import *
from state import UserState
from utils import *

config: Config = load_config('.env')

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

# Инициализируем роутер уровня модуля
router: Router = Router()
config: Config = load_config('.env')
db = DataBase(DATABASE_URL)
storage = MemoryStorage()
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)


router.message.filter(Payment())


@router.message(F.text.startswith(LEXICON_RU['new_deposit']))
async def parse_deposit(message: Message):
    print(message.text)  # TODO: доделать
