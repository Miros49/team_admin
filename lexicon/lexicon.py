LEXICON_RU: dict[str, str | list[str]] = {
    'profile to admin': 'Пользоваель: <code>{user_id}</code>\n\n'
                        'Профиль Lolz: {lolz_profile}\n\n'
                        'Опыт работы: {work_exp}\n\n'
                        'Сколько времени готов уделять: {work_time}',
    'create_profile': ['Профиль лолз', 'Опыт работы', 'Время работы', 'Заявка успешно отправлена'],
    'accept user': 'Вы успешно приняты в команду *название*\n\nВам доступно меню воркера',
    'decline user': 'К сожалению мы пока не готовы с вами работать, если у вас есть вопросы можете '
                    'отписать @Ambassador_LZT',
    'profile': '👤 Общая информация:\n'
               'L👉 ID:  <code>{user_id}</code>\n'
               'L👉 Профиль lolz:  <code>{lolz}</code>\n'
               'L👉 Наставник: {tutor}\n'
               'L⭐️ Отображение ника в выплатах:  {displayed_nickname}\n'
               'L⚜️ Статус:  {status}\n'
               'L  Никнейм:  {nickname}\n\n'
               '📈 Статистика:\n'
               'L💵 Текущий баланс:  <code>{current_balance}$</code>\n'
               'L💸 Общий оборот:  {total_turnover}\n'
               'L  Процент:  {percent}\n'
               'L  Сумма регистраций\n\n'
               '⁉️ Лимиты:\n'
               'L  Прокси:  {proxy}\n'
               'L  Номера:  {numbers}\n\n'
               '💳 Привязанные кошельки:\n'
               'L  BTC: {btc}\n'
               'L  ETH: {eth}\n'
               'L  USDT (TRC20): {trc20}\n'
               'L  TRON: {tron}\n',
    'no_wallets': 'Для начала привяжите кошелёк в профиле',
    'choose_wallet_for_payout': 'Выберите кошелёк для выплаты',
    'payout_requested': '⏳ Запрос отправлен',
    'payout_info': '💸 Запрос выплаты:\n\n'
                   '{wallet_type}: {wallet}\n'
                   'Сумма: {amount}\n'
                   'Воркер: @{username} ({tg_id})',
    'enter_nickname': '✍️ Введите никнейм',
    'nickname_is_set': '✅ Установлен никнейм {}',
    'current_domain': '✅ Актуальный домен: <code>higolimo.com</code>',
    'enter_tags_prompt': 'Введите ключевое(ые) слово(а)',
    'your_promo': '📜 Ваши промокоды',
    'promo_type': 'Какой промокод нужно создать?',
    'information': 'ℹ️ some information',
    'dev': '🧑‍💻 В разработке',
    'choose_wallet': '👇 Выберите, какой кошелёк желаете привязать:',
    'enter_wallet': '📝 Введите кошелёк {}',
    'no_money': 'Нет доступных средств для вывода 😢\nиди работай 😉',
    'payout_amount': '💵 Ваш баланс:  <code>{balance}</code>$\n\nВведите сумму, которую хотите вывести 🤑',
    'wrong_amount': '🤕 Вы не можете вывести столько денег, попробуйте ещё раз',
    'admin_menu': 'Здравствуйте, {}! 😊',
    'not_allowed': '👩‍🦰⛔️ У вас недостаточно прав 💅❌',
    'joke': '😝 Ладно, шучу',
    'enter_mail': '📨 Отправьте сообщение для рассылки (пока что работает только текст)',
    'mailing': '📤 Начинаю рассылку...',
    'enter_id': '✏️ Введите id админа',
    'wrong_format': '🤕 Неверный формат ввода. Попробуйте ещё раз',
    'admin_added': 'Теперь {} админ',
    'tutors': '🧑‍💻 В разработке',
    'select_generator': '📟 Выберите нужный генератор:',
    'tools_for_work': '🔧Инструменты для работы',
    'promo_ticker': 'Какой тикер?',
    'enter_amount': 'На какую сумму создать промокод?',
    'enter_custom_promo': 'Введите кастомный промокод',
    'enter_user_ban_info': 'Введите телеграм id или ник (в формате @username) пользователя, которого хотите забанить',
    'enter_creo_text': 'Введите текст (👨‍🔬 тест)'
}

buttons: dict[str, str] = {
    'profile': '🧑‍💻 Профиль',
    'options': '⚙️ Опции',
    'current_domain': '🔗 Актуальный домен',
    'promo': '🎫 Промокод',
    'information': 'ℹ️ Информация',
    'tutors': '👩‍🏫 Наставники/Филиалы',
    'back': '🔙 Назад',
    'random_promo': '🎲 Случайный',
    'custom_promo': '✍️ Кастомный'
}

callbacks: dict[str, str] = {
    '🆙 Повысить лимиты': 'increase_limits',
    '📝 Изменить информацию': 'edit_profile',
    '👛 Привязать кошелек': 'link_wallet',
    '💸 Запросить выплату': 'request_payout',
    '⭐️ Установить никнейм': 'set_nickname',
    '🫂 Реферальная система': 'referral_system',
    '🔷 Получить промокод': 'get_promo',
    '📈 Статистика промокодов': 'promo_stats',
    buttons['random_promo']: 'create_promo_random',
    buttons['custom_promo']: 'create_promo_custom',
    '🔗 Получить прокси': 'get_proxy',
    '📱 Получить номер': 'get_number',
    '📟 Генераторы': 'generators',
    '📝 Заявка в филиал': 'application_to_branch',
    '👮🏿‍♀️ Tags': 'generator_tags',
    '👧 Girls': 'generator_girl',
    '👻 NFT': 'generator_nft',
    '🤯 Creo': 'generator_creo',
    'BTC': 'wallet_btc',
    'ETH': 'wallet_eth',
    'USDT (TRC20)': 'wallet_trc20',
    'TRX': 'wallet_trx',
    '📢 Рассылка': 'admin_mailing',
    '➕ Добавить админа': 'add_admin',
    '🗑 Удалить админа': 'delete_admin',
    '🚫👶 Забанить пользователя': 'ban_user',
    buttons['back']: 'back_button'
}
