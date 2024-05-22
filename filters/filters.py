from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from config_data import Config, load_config, admins


config: Config = load_config('.env')
ADMIN_IDS: list[int] = config.tg_bot.admin_ids


class IsAdmin(Filter):
    async def __call__(self, message: Message, *args, **kwargs):
        return message.from_user.id in ADMIN_IDS or message.from_user.id in admins


class PrivateChat(Filter):
    async def __call__(self, message: Message):
        return message.chat.type == 'private'