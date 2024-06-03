import asyncio
import logging


from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config_data import Config, load_config
from database import DataBase
from handlers import start_handlers, user_handlers, admin_handlers, payments_handlers

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
dp.include_router(user_handlers.router)
dp.include_router(admin_handlers.router)
dp.include_router(payments_handlers.router)


# Функция конфигурирования и запуска бота
async def main():
    await db.create_tables()

    await bot.delete_webhook(drop_pending_updates=True)
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
