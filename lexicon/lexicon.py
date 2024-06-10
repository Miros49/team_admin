LEXICON_RU: dict[str, str | list[str]] = {
    'profile to admin': 'Пользоваель: @{username} (<code>{user_id}</code>)\n\n'
                        'Профиль Lolz: {lolz_profile}\n\n'
                        'Опыт работы: {work_exp}\n\n'
                        'Сколько времени готов уделять: {work_time}',
    'accepted': '\n\n✅ <b>Принят</b>',
    'denied': '\n\n❌ <b>Отклонён</b>',
    'already_accepted': '\n\n✅ Пользователь уже принят другим админом',
    'create_profile': ['Профиль лолз', 'Опыт работы', 'Сколько времени готов уделять?   ', 'Заявка успешно отправлена'],
    'accept user': '✅ Вы приняты в команду Renegade Team\n\nВам доступно меню воркера',
    'decline user': 'К сожалению мы пока не готовы с вами работать, если у вас есть вопросы можете '
                    'отписать @Ambassador_LZT',
    'profile': '<u>👤 Общая информация:</u>\n'
               'L🪪 ID:  <code>{user_id}</code>\n'
               'L⭐️ Никнейм:  {nickname}\n'
               'L👉 Профиль lolz:  <code>{lolz}</code>\n'
               'L👩‍🏫 Наставник: {tutor}\n'
               'L⚜️ Статус:  {status}\n\n'
               '<u>📈 Статистика:</u>\n'
               'L💵 Текущий баланс:  <code>{current_balance}</code>$\n'
               'L💸 Общий оборот:  <code>{total_turnover}</code>$\n'
               'L🚀 Процент:  <code>{percent}</code>%\n'
               'L👥 Сумма регистраций:  <code>{users_count}</code>\n\n'
               '<u>💳 Привязанные кошельки:</u>\n'
               'L🟠 BTC: <code>{btc}</code>\n'
               'L🔷 ETH: <code>{eth}</code>\n'
               'L🟢 USDT (TRC20): <code>{trc20}</code>\n'
               'L🔻 TRON: <code>{tron}</code>\n',
    'referral': '🥳 По Вашей реферальной ссылке принят новый воркер',
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
    'contacts': '<b>Командный состав 💎\n'
                '❤️ Team Leaders - @DarkmodeTS (только по важным вопросам)\n'
                '❤️ Supports - @BurmaldaTS, @DrosselRTeam</b>',
    'enter_tags_prompt': 'Введите ключевое(ые) слово(а)',
    'your_promo': '📜 Ваши промокоды:\n',
    'promo_type': 'Какой промокод нужно создать?',
    'promo_limit': 'Вы уже достигли лимита на создание промокодов (3 шт.)',
    'information': 'Вы можете вступить в наши чаты:',
    'dev': '🧑‍💻 В разработке',
    'choose_wallet': '👇 Выберите, какой кошелёк желаете привязать:',
    'enter_wallet': '📝 Введите кошелёк {}',
    'no_money': 'Нет доступных средств для вывода 😢\nиди работай 😉',
    'payout_amount': '💵 Ваш баланс:  <code>{balance}</code>$\n\nВведите сумму, которую хотите вывести 🤑',
    'wrong_amount': '🤕 Вы не можете вывести столько денег, попробуйте ещё раз',
    'referral_info': '💵 Всего заработано:  <code>{amount}</code>$\n'
                     '🤑 Общий оборот у рефералов:  <code>{ref_total_turnover}</code>$\n'
                     '👥 Всего рефералов:  <b>{ref_num}</b>\n'
                     '🚀 Ваш процент:  <b>{percent}%</b>\n\n'
                     '🔗 Реферальная ссылка:\n<code>{link}</code>',
    'admin_menu': 'Здравствуйте, {}! 😊',
    'not_allowed': '👩‍🦰⛔️ У вас недостаточно прав 💅❌',
    'joke': '😝 Ладно, шучу',
    'enter_mail': '📨 Отправьте сообщение для рассылки (пока что работает только текст)',
    'mailing': '📤 Начинаю рассылку...',
    'enter_id': '✏️ Введите id админа',
    'wrong_format': '🤕 Неверный формат ввода. Попробуйте ещё раз',
    'admin_added': '🥳 Теперь {} админ',
    'tutors': '🧑‍💻 В разработке',
    'select_generator': '📟 Выберите нужный генератор:',
    'tools_for_work': '🔧Инструменты для работы',
    'promo_ticker': '🎟 На какой тикер создать промокод?',
    'enter_amount': '💲 На какую сумму создать промокод?',
    'enter_custom_promo': '✍️ Введите кастомный промокод',
    'enter_promo': '✍️ Введите промокод',
    'enter_user_ban_info': '✍️🦍 Введите телеграм id пользователя, которого хотите забанить',
    'enter_creo_domain': '<b>Введите домен\nПример:</b> <code>higolimo.com</code>',
    'enter_creo_promo': '<b>Введите промокод\nПример:</b> <code>G97DW3SX5</code>',
    'enter_creo_amount': '<b>Введите сумму промокода\nПример:</b> <code>0.25 BTC</code>',
    'choose_admin_to_delete': '👇 Выберите, какого админа хотите удалить:',
    'admin_deleted': '✅ Админ удалён',
    'new_deposit': 'Новый депозит',
    'error': '👾 Произошла ошибка, попробуйте позже',
    'generation_is_running': '⏳ Идёт генерация, подождите',
    'worker_not_found': '‼️ <b>Ошибка выплаты</b> ‼️\n\nВоркер -  {} ({})\nСумма - {}$'
}

buttons: dict[str, str] = {
    'profile': '🧑‍💻 Профиль',
    'options': '⚙️ Опции',
    'generators': '📟 Генераторы',
    'current_domain': '🔗 Актуальный домен',
    'promo': '🎫 Промокод',
    'information': 'ℹ️ Информация',
    'contacts': '📞 Контакты',
    'referral': '🫂 Реферальная система',
    'request_payout_ref': '🫂💸 Запросить выплату по рефералам',
    'tutors': '👩‍🏫 Наставники/Филиалы',
    'back': '🔙 Назад',
    'admin_back': '🔙 Нaзад',
    'random_promo': '🎲 Случайный',
    'custom_promo': '✍️ Кастомный',
    'tags': '#️⃣ Tags',
    'creo': '🌄 Creo',
    'payments_channel': '💸 Канал с выплатами',
    'info_channel': 'ℹ️ Канал с информацией',
    'workers_chat': '💬 Чат',
    'creo_yt_mr_beast': '🔴 YT | Mr. Beast',
    'creo_PewDiePie': ' 🔴 YT | PewDiePie',
    'creo_poster_elon_musk': '📃 Poster | Elon Musk'
}

callbacks: dict[str, str] = {
    '🆙 Повысить лимиты': 'increase_limits',
    '📝 Изменить информацию': 'edit_profile',
    '👛 Привязать кошелек': 'link_wallet',
    '💸 Запросить выплату': 'request_payout',
    '⭐️ Установить никнейм': 'set_nickname',
    buttons['referral']: 'referral_system',
    buttons['request_payout_ref']: 'request_payout_ref',
    '🔷 Получить промокод': 'get_promo',
    '📈 Статистика промокодов': 'promo_stats',
    buttons['random_promo']: 'create_promo_random',
    buttons['custom_promo']: 'create_promo_custom',
    '🔗 Получить прокси': 'get_proxy',
    '📱 Получить номер': 'get_number',
    '📟 Генераторы': 'generators',
    '📝 Заявка в филиал': 'application_to_branch',
    buttons['tags']: 'generator_tags',
    '👧 Girls': 'generator_girl',
    '👻 NFT': 'generator_nft',
    buttons['creo']: 'generator_creo',
    'BTC': 'wallet_btc',
    'ETH': 'wallet_eth',
    'USDT (TRC20)': 'wallet_trc20',
    'TRX': 'wallet_trx',
    '📢 Рассылка': 'admin_mailing',
    '➕ Добавить админа': 'add_admin',
    '🗑 Удалить админа': 'delete_admin',
    '🚫👶 Забанить пользователя': 'ban_user',
    buttons['back']: 'back_button',
    buttons['admin_back']: 'admin_back_button',
    buttons['payments_channel']: 'https://t.me/+isjHdms-SxhhZTYy',
    buttons['info_channel']: 'https://t.me/+Xfcr0LA6ksdiOGRi',
    buttons['workers_chat']: 'https://t.me/+8Xq9x3FT3m5jYWQy',
    buttons['creo_yt_mr_beast']: 'creo_button_yt_mr_beast',
    buttons['creo_PewDiePie']: 'creo_button_yt_PewDiePie',
    buttons['creo_poster_elon_musk']: 'creo_button_poster_elon_musk'
}
