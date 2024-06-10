import asyncio

from aiogram import Dispatcher, F, Bot, Router
from aiogram.filters import StateFilter, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.exceptions import TelegramRetryAfter

from config_data import Config, load_config
from database import DataBase
from filters import IsUser, PrivateChat, IsNotBanned, IsNotAdmin
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
kb = UserKeyboards()

router.message.filter(PrivateChat(), IsUser(), IsNotBanned())
router.callback_query(PrivateChat(), IsUser(), IsNotBanned())


@router.callback_query(F.data == callbacks[buttons['back']])
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if not current_state or current_state == UserState.enter_nickname:
        if callback.message.text == LEXICON_RU['select_generator']:
            await callback.message.edit_text(LEXICON_RU['tools_for_work'], reply_markup=kb.options)
        elif callback.message.text == LEXICON_RU['promo_type']:
            user = await db.get_promocodes(callback.from_user.id)
            text = LEXICON_RU['your_promo']
            if not user or not user.promocodes:
                if not user:
                    await db.set_user_promocodes(callback.from_user.id)
                text += 'У Вас ещё нет промокодов'
            elif user.promocodes:
                text += '<code>' + '</code>\n'.join(user.promocodes.split(',')) + '</code>'

            await callback.message.answer(text, reply_markup=kb.promo, parse_mode='HTML')
        elif callback.message.text == LEXICON_RU['promo_ticker']:
            await callback.message.edit_text(LEXICON_RU['promo_type'], reply_markup=kb.create_promo)
        else:
            user = await db.get_user(callback.from_user.id)
            wallets = await db.get_wallets(callback.from_user.id)
            await callback.message.edit_text(LEXICON_RU['profile'].format(
                user_id=callback.from_user.id,
                nickname=f"<code>{user.nickname}</code>" if user and user.nickname else 'Нет',
                lolz=user.lolz_profile if user.lolz_profile else 'Нет профиля',
                tutor='Отсутствует',
                status=user.status,
                current_balance=str(user.balance),
                total_turnover=str(user.total_turnover),
                percent=str(await get_percent(user.total_turnover)),
                users_count=user.users_count,
                btc=f"<code>{wallets.btc}</code>" if wallets and wallets.btc else 'Не привязан',
                eth=f"<code>{wallets.eth}</code>" if wallets and wallets.eth else 'Не привязан',
                trc20=f"<code>{wallets.trc20}</code>" if wallets and wallets.trc20 else 'Не привязан',
                tron=f"<code>{wallets.trx}</code>" if wallets and wallets.trx else 'Не привязан'
            ), reply_markup=kb.profile_kb(), parse_mode='HTML')
    elif current_state == UserState.generate_tags:
        await callback.message.edit_text(LEXICON_RU['select_generator'], reply_markup=kb.generators())
    elif current_state == UserState.enter_promo:
        await callback.message.edit_text(LEXICON_RU['your_promo'], reply_markup=kb.promo)
    await state.clear()


@router.message(F.text == buttons['profile'])
async def profile(message: Message):
    user = await db.get_user(message.from_user.id)
    wallets = await db.get_wallets(message.from_user.id)
    await message.answer(LEXICON_RU['profile'].format(
        user_id=message.from_user.id,
        nickname=f"<code>{user.nickname}</code>" if user and user.nickname else 'Нет',
        lolz=user.lolz_profile if user.lolz_profile else 'Нет профиля',
        tutor='Отсутствует',
        status=user.status,
        current_balance=str(user.balance),
        total_turnover=str(user.total_turnover),
        percent=str(await get_percent(user.total_turnover)),
        users_count=user.users_count,
        btc=f"<code>{wallets.btc}</code>" if wallets and wallets.btc else 'Не привязан',
        eth=f"<code>{wallets.eth}</code>" if wallets and wallets.eth else 'Не привязан',
        trc20=f"<code>{wallets.trc20}</code>" if wallets and wallets.trc20 else 'Не привязан',
        tron=f"<code>{wallets.trx}</code>" if wallets and wallets.trx else 'Не привязан'
    ), reply_markup=kb.profile_kb(), parse_mode='HTML')


@router.callback_query(F.data == callbacks['🆙 Повысить лимиты'])
async def profile_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(LEXICON_RU['dev'])


@router.callback_query(F.data == callbacks['📝 Изменить информацию'])
async def profile_menu(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(LEXICON_RU['dev'])


@router.callback_query(F.data == callbacks['👛 Привязать кошелек'])
async def profile_menu(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON_RU['choose_wallet'], reply_markup=kb.wallets())


@router.callback_query(F.data.startswith('wallet'))
async def enter_wallet(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    wallet = callback.data.split('_')[1]
    await callback.message.edit_text(LEXICON_RU['enter_wallet'].format(wallet.upper()))
    await state.set_state(UserState.enter_wallet)
    await state.update_data({'wallet': wallet})


@router.message(StateFilter(UserState.enter_wallet))
async def enter_wallet(message: Message, state: FSMContext):
    data = await state.get_data()
    if await db.wallet_exists(message.from_user.id):
        await db.add_wallet(message.from_user.id, {data['wallet']: message.text})
    else:
        await db.set_wallet(message.from_user.id)
        await db.add_wallet(message.from_user.id, {data['wallet']: message.text})
    await message.answer(f"кошелёк {data['wallet'].upper()} установлен")
    await state.clear()


@router.callback_query(F.data == callbacks['💸 Запросить выплату'])
async def choose_wallet_for_payout(callback: CallbackQuery):
    await callback.answer()
    user = await db.get_user(callback.from_user.id)
    linked_wallets = await db.get_linked_wallets(callback.from_user.id)

    if not user:
        await db.set_wallet(callback.from_user.id)
    if not user.balance:
        await callback.message.answer(LEXICON_RU['no_money'])
        if callback.from_user.id in config.tg_bot.admin_ids:
            await callback.message.answer('Поскольку Вы являетесь администратором, в целях тестирования Вам доступна'
                                          'команда <code>/add n</code> для зачисления на баланс n денег',
                                          parse_mode='HTML')
    elif linked_wallets:
        await callback.message.edit_text(LEXICON_RU['choose_wallet_for_payout'],
                                         reply_markup=kb.walets_for_payout(linked_wallets))
    else:
        await callback.message.answer(LEXICON_RU['no_wallets'])
        await callback.answer()


@router.callback_query(F.data.startswith('payout'))
async def enter_payout_amount(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    user = await db.get_user(callback.from_user.id)
    await callback.message.edit_text(LEXICON_RU['payout_amount'].format(balance=str(user.balance)), parse_mode='HTML')
    await state.set_state(UserState.enter_payout_amount)
    await state.update_data({"wallet_type": callback.data.split('_')[1]})


@router.message(StateFilter(UserState.enter_payout_amount))
async def request_payout(message: Message, state: FSMContext):
    try:
        amount = float(message.text)
        data = await state.get_data()
        user = await db.get_user(message.from_user.id)
        if 0 < amount <= user.balance:
            wallet_type = data['wallet_type']
            wallet = await db.get_linked_wallets(message.from_user.id)
            await bot.send_message(chat_id=config.tg_bot.admin_chat, text=LEXICON_RU['payout_info'].format(
                wallet_type=wallet_type,
                wallet=wallet[wallet_type],
                amount=amount,
                username=message.from_user.username,
                tg_id=message.from_user.id
            ))
            await message.answer(LEXICON_RU['payout_requested'])
            await db.edit_balance(message.from_user.id, -amount)
        else:
            await message.answer(LEXICON_RU['wrong_amount'])
    except ValueError:
        await message.answer(LEXICON_RU['wrong_format'])
    await state.clear()


@router.callback_query(F.data == callbacks['⭐️ Установить никнейм'])
async def enter_nickname(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_nickname'], reply_markup=kb.back())
    await state.set_state(UserState.enter_nickname)


@router.message(StateFilter(UserState.enter_nickname))
async def set_nickname(message: Message, state: FSMContext):
    try:
        await db.set_nickname(message.from_user.id, message.text)
        await message.answer(LEXICON_RU['nickname_is_set'].format(message.text))
    except Exception as e:
        await message.answer(str(e))
    await state.clear()


@router.callback_query(F.data == callbacks[buttons['referral']])
async def profile_menu(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    await callback.message.edit_text(LEXICON_RU['referral_info'].format(
        amount=str(user.total_turnover),
        ref_total_turnover=await db.get_total_turnover_by_referrer(callback.from_user.id),
        ref_num=str(user.ref_num),
        percent='1',
        link=f'https://t.me/RenegadeTeamBot?start={callback.from_user.id}'
    ), reply_markup=kb.request_payout_ref(), parse_mode='HTML')


@router.callback_query(F.data == callbacks[buttons['request_payout_ref']])  # TODO: доделать
async def request_payout_ref(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(LEXICON_RU['dev'])


@router.message(F.text == buttons['options'])
async def options_menu(message: Message):
    # await message.answer(LEXICON_RU['tools_for_work'], reply_markup=kb.options)
    await message.answer('Теперь кнопки в главном меню выглядят по-другому 🤗', reply_markup=kb.menu)


# @router.callback_query(F.data == callbacks['🔗 Получить прокси'])
# async def get_proxy(callback: CallbackQuery):
#     await callback.message.answer(await generate_proxy(), parse_mode='HTML')
#     await callback.answer()
#
#
# @router.callback_query(F.data == callbacks['📱 Получить номер'])
# async def get_number(callback: CallbackQuery):
#     await callback.answer()
#     await callback.message.answer(await generate_phone_number(), parse_mode='HTML')


@router.message(F.text == buttons['generators'])
async def generators(message: Message):
    await message.answer(LEXICON_RU['select_generator'], reply_markup=kb.generators())


@router.callback_query(F.data == callbacks[buttons['tags']])
async def tags_generator(callback: CallbackQuery, state: FSMContext):
    mes = await callback.message.edit_text(LEXICON_RU['enter_tags_prompt'], reply_markup=kb.back())
    await state.set_state(UserState.generate_tags)
    await state.update_data({"message_id": mes.message_id})


@router.message(StateFilter(UserState.generate_tags))
async def generate_tags(message: Message, state: FSMContext):
    data = await get_youtube_tags(message.text)
    if data['success']:
        await message.answer(f'<code>#{"</code>      <code>#".join(data["tags"])}</code>', parse_mode='HTML')
    else:
        await message.answer('Произошла ошибка, попробуйте позже\n\n{}'.format(data['message']))
    await state.clear()


@router.callback_query(F.data == callbacks['👧 Girls'])
async def girls(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(LEXICON_RU['dev'] + '\nНужны исходники')


@router.callback_query(F.data == callbacks['👻 NFT'])
async def nfts(callback: CallbackQuery):
    await callback.message.edit_text(callback.message.text)
    media_group = MediaGroupBuilder()
    for img in get_random_nft():
        media_group.add(type="photo", media=FSInputFile(img))

    await bot.send_media_group(callback.from_user.id, media=media_group.build())


@router.callback_query(F.data == callbacks[buttons['creo']])
async def creo(callback: CallbackQuery):
    await callback.message.edit_text('🔥 CREO:', reply_markup=await kb.creo())


@router.callback_query(F.data.startswith('creo_button'))
async def creo_photo(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_creo_domain'], parse_mode='HTML')
    await state.set_state(UserState.enter_creo_domain)
    await state.update_data({"photo": callback.data[12:]})


@router.message(StateFilter(UserState.enter_creo_domain))
async def creo_domain(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['enter_creo_promo'], parse_mode='HTML')
    await state.set_state(UserState.enter_creo_promo)
    data = await state.get_data()
    await state.update_data({"photo": data["photo"], "domain": message.text})


@router.message(StateFilter(UserState.enter_creo_promo))
async def creo_promo(message: Message, state: FSMContext):
    await message.answer(LEXICON_RU['enter_creo_amount'], parse_mode='HTML')
    data = await state.get_data()
    await state.set_state(UserState.enter_creo_amount)
    await state.update_data({"photo": data["photo"], "domain": data["domain"], "promo": message.text})


@router.message(StateFilter(UserState.enter_creo_amount))
async def generate_creo_handler(message: Message, state: FSMContext):
    mes = await message.answer(LEXICON_RU['generation_is_running'])
    try:
        data = await state.get_data()
        image_path = await generate_creo(
            photo=data["photo"],
            domain=data["domain"],
            promo=data["promo"],
            amount=message.text,
            user_id=message.from_user.id
        )
        image = FSInputFile(image_path)

        for _ in range(3):
            try:
                await bot.send_photo(message.from_user.id, photo=image)
                break
            except TelegramRetryAfter:
                await asyncio.sleep(8)
        await mes.delete()
    except Exception as e:
        await mes.edit_text("🤕 Произошла ошибка при генерации изображения.\nПожалуйста, попробуйте позже.")
        print(f"\nОшибка генерации изображения: {str(e)}\n")
    await state.clear()


@router.message(F.text == buttons['contacts'])
async def contacts(message: Message):
    await message.answer(LEXICON_RU['contacts'], parse_mode='HTML')


@router.message(F.text == buttons['current_domain'])
async def domain_menu(message: Message):
    await message.answer(LEXICON_RU['current_domain'], parse_mode='HTML')


@router.message(F.text == buttons['promo'])
async def promo_menu(message: Message):
    text = LEXICON_RU['your_promo']
    user = await db.get_promocodes(message.from_user.id)
    if not user or not user.promocodes:
        if not user:
            await db.set_user_promocodes(message.from_user.id)
        text += 'У Вас ещё нет промокодов'
    elif user.promocodes:
        text += '▪️<code>' + '</code>\n▪️<code>'.join(user.promocodes.split(',')) + '</code>'

    await message.answer(text, reply_markup=kb.promo, parse_mode='HTML')


@router.callback_query(F.data == callbacks['🔷 Получить промокод'])
async def handler_create_promo(callback: CallbackQuery):
    await callback.message.edit_text(LEXICON_RU['promo_type'], reply_markup=kb.create_promo)


@router.callback_query(F.data.startswith('create_promo'))
async def create_promo_first(callback: CallbackQuery, state: FSMContext):

    if callback.data.split('_')[-1] == 'custom':
        await state.update_data({"custom": True})
    else:
        await state.update_data({"custom": False})

    await callback.message.edit_text(LEXICON_RU['promo_ticker'], reply_markup=kb.tickers)


@router.callback_query(F.data.startswith('ticker_'))
async def ticker(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(LEXICON_RU['enter_amount'])
    data = await state.get_data()
    await state.set_state(UserState.create_promo_amount)
    await state.update_data({"custom": data["custom"], "ticker": callback.data.split('_')[1].upper()})


@router.message(StateFilter(UserState.create_promo_amount))
async def create_default_promo(message: Message, state: FSMContext):
    data = await state.get_data()

    if data["custom"]:
        await message.answer(LEXICON_RU['enter_custom_promo'])
        data = await state.get_data()
        await state.set_state(UserState.create_promo_custom)
        return await state.update_data(
            {"custom": data["custom"], "ticker": data["ticker"], "amount": float(message.text)})

    response = await create_promo(data["ticker"], float(message.text), message.from_user.id)
    if response["success"]:
        code = response["codes"][0]
        await message.answer(f"<code>{code}</code>", parse_mode='HTML')
        await db.add_promocode(user_id=message.from_user.id, promocode=str(code))
    else:
        await message.answer(response["message"])
    await state.clear()


@router.message(StateFilter(UserState.create_promo_custom))
async def create_promo_custom(message: Message, state: FSMContext):
    data = await state.get_data()
    response = await create_promo(ticker=data["ticker"], amount=data["amount"], user_id=message.from_user.id,
                                  custom_code=message.text)
    if response["success"]:
        code = response["codes"][0]
        await message.answer(f"Промокод создан: <code>{code}</code>", parse_mode='HTML')
        await db.add_promocode(message.from_user.id, str(code))
    else:
        await message.answer(response["message"])
    await state.clear()


@router.callback_query(F.data == callbacks['📈 Статистика промокодов'])
async def promo_statistics(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    mes = await callback.message.edit_text(LEXICON_RU['enter_promo'], reply_markup=kb.back())
    await state.set_state(UserState.enter_promo)
    await state.update_data({"mes_id": mes.message_id})


@router.message(StateFilter(UserState.enter_promo))
async def check_promo(message: Message, state: FSMContext):
    response = await get_promo_info(message.text, message.from_user.id)
    text = ''
    if response["success"]:
        for key, value in response.items():
            if key == "info":
                text += "Сумма: {}\n".format(value["amount"])
                text += "Тикер: {}\n".format(value["ticker"])
                text += "Общая сумма депозитов: {}\n".format(value["deposit_sum"])
                text += "Общее число регистраций: {}\n".format(value["users_count"])
            elif key != "message" and key != "success":
                text += "{}: {}\n".format(key.capitalize(), value)
    else:
        text = "Error: {response['message']}"

    await message.answer(text)
    data = await state.get_data()
    await bot.edit_message_text(text='Введите промокод', chat_id=message.from_user.id, message_id=data["mes_id"])
    await state.clear()


@router.message(F.text == buttons['information'])
async def information(message: Message):
    await message.answer(LEXICON_RU['information'], reply_markup=await kb.info())


@router.message(F.text == buttons['tutors'])
async def tutors(message: Message):
    await message.answer(LEXICON_RU['tutors'], reply_markup=kb.tutors())


@router.callback_query(F.data == callbacks['📝 Заявка в филиал'])
async def application_to_branch(callback: CallbackQuery):
    await callback.message.answer(LEXICON_RU['dev'])


@router.message(Command('admin'), IsNotAdmin())
async def admin_menu(message: Message):
    await message.answer(LEXICON_RU['not_allowed'])


@router.message(Command('test'))
async def add_money(message: Message, state: FSMContext):
    try:
        image_path = await generate_creo(
            photo='yt_PewDiePie',
            domain='higolimo.com',
            promo='G97DW3SX5',
            amount='0.25 BTC',
            user_id=message.from_user.id
        )
        image = FSInputFile(image_path)
        await bot.send_photo(message.from_user.id, photo=image)
    except Exception as e:
        await message.answer(str(e))
