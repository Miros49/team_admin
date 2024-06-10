from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config_data import Config, load_config
from database import DataBase


config: Config = load_config('.env')
ADMIN_IDS: list[int] = config.tg_bot.admin_ids

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
db = DataBase(DATABASE_URL)


class IsAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in ADMIN_IDS or message.from_user.id in await db.get_admins_ids()


class IsUser(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in await db.get_all_users()


class IsNotBanned(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        user = await db.get_user(message.from_user.id)
        return not user.banned


class PrivateChat(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.chat.type == 'private'


class Payment(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.chat.id == config.tg_bot.payments_channel


class IsNotAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return not (message.from_user.id in ADMIN_IDS or message.from_user.id in await db.get_admins_ids())


class NewMember(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.new_chat_members
