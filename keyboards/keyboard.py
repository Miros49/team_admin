import math

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database import DataBase
from lexicon import LEXICON_RU, buttons, callbacks
from config_data import Config, load_config

config: Config = load_config('.env')

DATABASE_URL = f"postgresql+asyncpg://{config.db.db_user}:{config.db.db_password}@{config.db.db_host}/{config.db.database}"

db = DataBase(DATABASE_URL)


# Функция для формирования инлайн-клавиатуры на лету
def create_inline_kb(width: int,
                     *args: str,
                     **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_linked_inline_kb(width: int,
                            **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []
    if kwargs:
        for text, url in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                url=url))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    buttons.append(InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_menu"))
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_profile_inline_kb(width: int,
                             *args: str,
                             **kwargs: str) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button,
                callback_data=button))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)
    kb_builder.adjust(2, 1, 2, 2)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_inline_kb_dict(width: int,
                          dict) -> InlineKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    for button, text in dict.items():
        buttons.append(InlineKeyboardButton(
            text=text,
            callback_data=button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_menu_reply_kb(
        btn: list, ) -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if btn:
        for button in btn:
            buttons.append(KeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=2)
    kb_builder.adjust(2, 2, 2, 1)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


def create_reply_kb(width: int,
                    btn: list, ) -> ReplyKeyboardMarkup:
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[KeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if btn:
        for button in btn:
            buttons.append(KeyboardButton(
                text=LEXICON_RU[button] if button in LEXICON_RU else button))
    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup(resize_keyboard=True)


back_button: InlineKeyboardButton = InlineKeyboardButton(text=buttons['back'], callback_data=callbacks[buttons['back']])


class StartKeyboards:
    def accept_user(self, user_id) -> InlineKeyboardMarkup:
        buttons = dict()
        buttons[f'user_accept_{user_id}'] = "✅ Принять"
        buttons[f'user_decline_{user_id}'] = "❌ Отклонить"
        return create_inline_kb_dict(2, buttons)


class UserKeyboards:
    menu = create_menu_reply_kb(
        [buttons['profile'], buttons['options'], buttons['current_domain'], buttons['promo'],
         buttons['information'], buttons['tutors']]
    )

    def profile_kb(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='🆙 Повысить лимиты', callback_data=callbacks['🆙 Повысить лимиты']),
            InlineKeyboardButton(text='📝 Изменить информацию', callback_data=callbacks['📝 Изменить информацию']),
            InlineKeyboardButton(text='👛 Привязать кошелек', callback_data=callbacks['👛 Привязать кошелек']),
            InlineKeyboardButton(text='💸 Запросить выплату', callback_data=callbacks['💸 Запросить выплату']),
            InlineKeyboardButton(text='⭐️ Установить никнейм', callback_data=callbacks['⭐️ Установить никнейм']),
            InlineKeyboardButton(text='🫂 Реферальная система', callback_data=callbacks['🫂 Реферальная система'])
        )
        kb.adjust(2, 2, 1, 1)

        return kb.as_markup()

    def wallets(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='BTC', callback_data=callbacks['BTC']),
            InlineKeyboardButton(text='ETH', callback_data=callbacks['ETH']),
            InlineKeyboardButton(text='USDT (TRC20)', callback_data=callbacks['USDT (TRC20)']),
            InlineKeyboardButton(text='TRX', callback_data=callbacks['TRX']),
            back_button
        )
        kb.adjust(2, 2)
        return kb.as_markup()

    def walets_for_payout(self, linked_wallets: dict) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        for i in linked_wallets.keys():
            kb.add(InlineKeyboardButton(text=i, callback_data=f'payout_{i.lower()}'))
        kb.add(back_button)
        kb.adjust(2, 2, 1)

        return kb.as_markup()

    options = create_inline_kb_dict(2, {
        callbacks['🔗 Получить прокси']: '🔗 Получить прокси',
        callbacks['📱 Получить номер']: '📱 Получить номер',
        callbacks['📟 Генераторы']: '📟 Генераторы'
    })

    promo = create_inline_kb_dict(1, {
        callbacks['🔷 Получить промокод']: '🔷 Получить промокод',
        callbacks['📈 Статистика промокодов']: '📈 Статистика промокодов',
        callbacks['➕ Добавить промокод']: '➕ Добавить промокод'
    })

    def tutors(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(InlineKeyboardButton(text='📝 Заявка в филиал', callback_data=callbacks['📝 Заявка в филиал']),
               back_button)
        kb.adjust(1, 1)
        return kb.as_markup()

    def generators(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='👮🏿‍♀️ Tags', callback_data=callbacks['👮🏿‍♀️ Tags']),
            InlineKeyboardButton(text='👧 Girls', callback_data=callbacks['👧 Girls']),
            InlineKeyboardButton(text='👻 NFT', callback_data=callbacks['👻 NFT']),
            InlineKeyboardButton(text='🤯 Creo', callback_data=callbacks['🤯 Creo']),
            back_button
        )
        kb.adjust(1, 2, 1, 1)

        return kb.as_markup()

    def back(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(back_button)
        return kb.as_markup()


class AdminKeyboards:
    def menu(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(
            InlineKeyboardButton(text='📢 Рассылка', callback_data=callbacks['📢 Рассылка']),
            InlineKeyboardButton(text='➕ Добавить админа', callback_data=callbacks['➕ Добавить админа']),
            InlineKeyboardButton(text='🗑 Удалить админа', callback_data=callbacks['🗑 Удалить админа']),
            InlineKeyboardButton(text='🚫👶 Забанить пользователя', callback_data=callbacks['🚫👶 Забанить пользователя'])
        )
        kb.adjust(1, 2, 1)

        return kb.as_markup()

    def back(self) -> InlineKeyboardMarkup:
        kb = InlineKeyboardBuilder()
        kb.row(back_button)
        return kb.as_markup()
