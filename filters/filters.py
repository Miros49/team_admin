from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config_data import Config, load_config, admins
from database import DataBase


config: Config = load_config('.env')
ADMIN_IDS: list[int] = config.tg_bot.admin_ids

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
db = DataBase(DATABASE_URL)


class IsAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        user = await db.get_user(message.from_user.id)
        if user.status == -1:
            await message.answer("Вы забанены")
        return message.from_user.id in ADMIN_IDS or message.from_user.id in admins


class IsUser(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in await db.get_all_users()


class PrivateChat(Filter):
    async def __call__(self, message: Message):
        return message.chat.type == 'private'
