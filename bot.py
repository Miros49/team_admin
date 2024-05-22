import asyncio
import logging
import time
from datetime import datetime, timedelta


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types.bot_command import BotCommand
from aiogram.types.input_file import FSInputFile

from keyboards import UserKeyboards
from config_data import Config, load_config
from database import DataBase
from handlers import start_handlers, user_handlers, admin_handlers
from lexicon import LEXICON_RU

storage = MemoryStorage()

logging.basicConfig(level=logging.INFO)
# Загружаем конфиг в переменную config
config: Config = load_config('.env')

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

# Инициализируем бот и диспетчер
bot: Bot = Bot(token=config.tg_bot.token)
dp: Dispatcher = Dispatcher(storage=storage)
db = DataBase(DATABASE_URL)

# Регистриуем роутеры в диспетчере
dp.include_router(start_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(user_handlers.router)


# Функция конфигурирования и запуска бота
async def main():
    await db.create_tables()
    # Начинаем обновление баланса каждый день в 15:00

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=False)
    # await bot.set_my_commands(commands=[
    #     BotCommand(
    #         command='start',
    #         description='Начало работы'
    #     )
    # ])
    polling_task = asyncio.create_task(dp.start_polling(bot))
    await asyncio.gather(polling_task)


if __name__ == '__main__':
    asyncio.run(main())
