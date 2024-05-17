from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config_data import Config, load_config
from database import DataBase
from keyboards import UserKeyboards
from lexicon import LEXICON_RU

config: Config = load_config('.env')
DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
# Инициализируем роутер уровня модуля
router: Router = Router()
db = DataBase(DATABASE_URL)
bot: Bot = Bot(token=config.tg_bot.token)
kb = UserKeyboards()


@router.callback_query(F.data.startswith("user_"))
async def create_ads(callback: CallbackQuery, state: FSMContext):
    user_id = callback.data.split("_")[2]
    if callback.data.split("_")[1] == "accept":
        await bot.send_message(user_id, LEXICON_RU['accept user'], reply_markup=kb.menu)
        try:
            await db.set_user(user_id=int(user_id))
            user = await db.get_user(int(user_id))
            await callback.message.answer(user)
        except Exception as e:
            print('\n\n\n\n' + str(e) + '\n\n\n\n')
    else:
        await bot.send_message(user_id, LEXICON_RU['decline user'])
