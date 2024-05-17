import random


def generate_phone_number() -> str:
    # Генерируем случайный 10-значный номер
    number = ''.join(random.choices('0123456789', k=9))
    return f"<code>+79{number}</code>"


def generate_proxy() -> str:
    path = ''.join(random.choices('qwertyuiopasdfghjklzxcvbnm//-0123456789', k=15))
    return f"https://{path}"
