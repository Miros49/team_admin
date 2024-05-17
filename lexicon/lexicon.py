LEXICON_RU: dict[str | dict[str, str], str | list[str]] = {
    'start': '<b>Привет</b>, 👽\n\n'
             '👾 Добывай руду в космосе на собственной планете и получай прибыль в TON каждые несколько часов!\n\n'
             '<b>Наш канал</b> - \n'
             '<b>Наш чат</b> - ',
    'menu': 'Меню',
    'profile to admin': 'Пользоваель: <code>{user_id}</code>\n\n'
                        'Профиль Lolz: {lolz_profile}\n\n'
                        'Опыт работы: {work_exp}\n\n'
                        'Сколько времени готов уделять: {work_time}',
    'create_profile': ['Профиль лолз', 'Опыт работы', 'Время работы', 'Заявка успешно отправлена'],
    'accept user': 'Вы успешно приняты в команду *название*\n\nВам доступно меню воркера',
    'decline user': 'К сожалению мы пока не готовы с вами работать, если у вас есть вопросы можете '
                    'отписать @Ambassador_LZT',
    'insert_amount': '<b>Напишите суммы вывода в сообщении</b>\n\n'
                     'Ваш кошелек: \n{wallet}\n\n'
                     'Если вы хотите изменить ваш кошелек - нажмите кнопку "Назад ↩️"\n\n'
                     '*с каждого вывода взимается комиссия 3% на поддержку и развитие проекта\n'
                     '*минимальный вывод = 0.20 TON',
    'insert_amount not enough': '<b>На вашем счете недостаточно средств, введите корректную сумму вывода</b>\n\n'
                                'Ваш кошелек: \n<b>{wallet}</b>\n\n'
                                'Если вы хотите изменить ваш кошелек - нажмите кнопку "Назад ↩️"\n\n'
                                '*с каждого вывода взимается комиссия 3% на поддержку и развитие проекта\n'
                                '*минимальный вывод = <b>0.30 TON</b>',
    'check_cashout': '✅ <b>Успешно!</b> Все выводы обрабатываются в течении 12 часов, пожалуйста ожидайте\n\n'
                     'Сумма вывода: <b>{amount}</b>\n\n'
                     'TON будет отправлен на кошелек:\n'
                     '<b>{address}</b>',
    'cashout admin': 'Пользователь <code>{user_id}</code>\n\n'
                     'вывод {amount} TON\n\n'
                     'адрес:\n<code>{address}</code>',
    'profile': '👤 Общая информация:'
               'L  ID: {user_id}\n'
               'L  Профиль lolz: {lolz}\n'
               'L  Наставник: {tutor}\n'
               'L  Отображение ника в выплатах: {displayed_nickname}\n'
               'L  Статус: {status}\n'
               'L  Никнейм: {nickname}\n\n'
               '📈 Статистика:\n'
               'L  Текущий баланс: {current_balance}\n'
               'L  Общий оборот: {total_turnover}\n'
               'L  Процент: {percent}\n'
               'L  Сумма регистраций\n\n'
               '?! Лимиты:\n'
               'L  Прокси: {proxy}\n'
               'L  Номера: {numbers}\n\n'
               '💳 Привязанные кошельки:\n'
               'L  ERC20/BEP20: {erc}\n'
               'L  BTC: {btc}\n'
               'L  TRC: {trc}\n'
               'L  TRON: {tron}\n',
    'current_domain': '✅ Актуальный домен: <code>firatex.com</code>',
    # 'select_color': '❕ Выберите цвет домена',
    # 'color_options': {
    #     '⚫️ Тёмный дизайн': 'dark_color',
    #     '🔵 Синий дизайн': 'blue_color',
    #     '🟢 Зелёный дизайн': 'green_color',
    #     '🟡 Жёлтый дизайн': 'yellow_color',
    #     '🌲 Тёмно-зелёный дизайн': 'dark-green_color'
    # },
    'your_promo': '📜 Ваши промокоды',
    'promo_options': ['Получить промокод', 'Статистика промокодов', 'Добавить промокод'],
    'select_checker': 'Выберите, какой нужен чекер',
    'enter_link': '📟 Введите ссылки на видео\nПример:\nyour link',
    'checking': '⌛️ Чекаю',
    'check_result': '✅#{num} Видео:\n\n'
                    'Видео наберёт просмотры: {predict}\n'
                    'Страна: {country}\n'
                    'Интересы: {interests}\n'
                    'Время залива: {upload_time}\n'
                    '👁: {views}  ❤️: {likes}  💬: {comments}, 📢: {reposts}, 💾: {saved}\n\n'
                    'Наличие теневого бана 💔: {shadow_ban}',
    'information': 'ℹ️ some information',
    'tutors': 'будет позже',  # TODO: заполнить текст тьютора
    'dev': 'будет позже'
}

LEXICON_ENG: dict[str, str | list[str]] = {

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
    '➕ Добавить промокод': 'add_promo',
    '🔗 Получить прокси': 'get_proxy',
    '📱 Получить номер': 'get_number',
    '📟 Генераторы': 'generators',
    '📝 Заявка в филиал': 'application_to_branch'
}

buttons: dict[str, str] = {
    'profile': '🧑‍💻 Профиль',
    'options': '⚙️ Опции',
    'current_domain': '🔗 Актуальный домен',
    'promo': '🎫 Промокод',
    'information': 'ℹ️ Информация',
    'tutors': '👩‍🏫 Наставники/Филиалы'
    # TODO: решить проблему с масштабированием (текст инлайн кнопок хранить тут)
}
