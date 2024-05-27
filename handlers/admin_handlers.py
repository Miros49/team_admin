import asyncio
from datetime import datetime

from aiogram import Bot, F, Router
from aiogram.filters import Command, StateFilter, CommandStart
from aiogram.handlers import MessageHandler
from aiogram.types import Message, CallbackQuery, ChatPermissions
from aiogram.fsm.context import FSMContext

from config_data import Config, load_config, admins
from database import DataBase
from filters import IsAdmin
from keyboards import AdminKeyboards, UserKeyboards
from lexicon import LEXICON_RU, callbacks
from state import AdminState
from utils import find_lolz_profile, parse_duration

config: Config = load_config('.env')
DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"
# Инициализируем роутер уровня модуля
router: Router = Router()
db = DataBase(DATABASE_URL)
bot: Bot = Bot(token=config.tg_bot.token)
kb = AdminKeyboards()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(F.data.startswith("user_"))
async def create_ads(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.data.split("_")[2])
    lolz = find_lolz_profile(callback.message.text).strip()
    await callback.message.answer(lolz + '\n' + str(len(lolz)))
    if callback.data.split("_")[1] == "accept":
        await bot.send_message(user_id, LEXICON_RU['accept user'], reply_markup=UserKeyboards.menu)
        try:
            await db.set_user(user_id=user_id, username=callback.from_user.username, lolz_profile=lolz)
        except Exception as e:
            print(str(e))
    else:
        await bot.send_message(user_id, LEXICON_RU['decline user'])


@router.message(Command('admin'))
async def admin_menu(message: Message, state: FSMContext):
    mes = await message.answer(LEXICON_RU['not_allowed'])
    await asyncio.sleep(1)
    await mes.delete()
    joke = await message.answer(LEXICON_RU['joke'])
    await message.answer(LEXICON_RU['admin_menu'].format(message.from_user.first_name), reply_markup=kb.menu())
    await asyncio.sleep(1)
    await joke.delete()


@router.callback_query(F.data == callbacks['📢 Рассылка'])
async def admin_mailing(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_mail'])
    await state.set_state(AdminState.enter_message)


@router.message(StateFilter(AdminState.enter_message))
async def admin_launch_mailing(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['mailing'])
    await state.clear()
    for user_id in await db.get_all_users():
        await bot.send_message(chat_id=user_id, text=message.text)


@router.callback_query(F.data == callbacks['➕ Добавить админа'])
async def enter_admin_id(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_id'])
    await state.set_state(AdminState.enter_admin_id)


@router.message(StateFilter(AdminState.enter_admin_id))
async def add_admin(message: Message, state: FSMContext):
    new_admin = message.text
    if new_admin.isdigit():
        admins.append(int(new_admin))
        await message.answer(LEXICON_RU['admin_added'].format(message.text))
        await state.clear()
    else:
        await message.answer(LEXICON_RU['wrong_format'])


@router.callback_query(F.data == callbacks['🗑 Удалить админа'])
async def delete_admin(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['dev'])


@router.callback_query(F.data == callbacks['🚫👶 Забанить пользователя'])
async def select_user_for_ban(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(LEXICON_RU['enter_user_ban_info'])
    await state.set_state(AdminState.ban_user)


@router.message(StateFilter(AdminState.ban_user))
async def ban_user(message: Message, state: FSMContext):
    # if len(message.text.split()) == 2:
    #     user_id, duration = message.text.split()
    #     if user_id.isdigit():
    #         user_id = int(user_id)
    #         chat_id = config.tg_bot.user_chat
    #         ban_duration = parse_duration(duration)
    #         if ban_duration is not None:
    #             until_date = datetime.now() + ban_duration
    #
    #             await bot.restrict_chat_member(
    #                 chat_id=chat_id,
    #                 user_id=user_id,
    #                 permissions=ChatPermissions(
    #                     can_send_messages=False,
    #                     can_send_media_messages=False,
    #                     can_send_other_messages=False,
    #                     can_add_web_page_previews=False
    #                 ),
    #                 until_date=until_date
    #             )
    #
    #             await message.reply(f"Пользователь {user_id} забанен на {duration}.")
    #         else:
    #             await message.reply("Неверный формат времени бана. Используйте число + s/m/h/d (например, 1d).")
    #     else:
    #         await message.reply("Неверный формат ID пользователя.")
    # else:
    #     await message.reply("Введите ID пользователя и время бана (например, 12345678 1d).")

    await state.clear()
