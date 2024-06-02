from aiogram import Dispatcher, F, Bot, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import Config, load_config
from database import DataBase
from filters import Payment
from lexicon import *
from utils import parse_deposit

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


@router.message(F.text.startswith(LEXICON_RU['new_deposit']))  # TODO: доделать
async def new_payout(message: Message):
    amount, worker = parse_deposit(message.text)
    try:
        try:
            user = await db.get_user_by_username(worker)
            await bot.send_message(user.id, 'Новая выплата!\nпотом допишу')  # TODO: лексикон
        except Exception as e:
            print(f"\n\n{str(e)}\n\n")
    except Exception as e:
        try:
            user = await db.get_user_by_username(worker)
            await bot.send_message(config.tg_bot.admin_chat,
                                   LEXICON_RU['user_not_found'].format(user.username, user.id, amount))
        except:
            await bot.send_message(config.tg_bot.admin_chat,
                                   LEXICON_RU['user_not_found'].format('Не найден', 'id не найден', amount))
        print(f"\n\n{str(e)}\n\n")
