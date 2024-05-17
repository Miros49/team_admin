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


class StartKeyboards:
    def accept_user(self, user_id):
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

        return kb.as_markup(resize_keyboard=True)

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

    tutors = create_inline_kb_dict(1, {callbacks['📝 Заявка в филиал']: '📝 Заявка в филиал'})
