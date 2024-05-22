import hashlib


def find_lolz_profile(text: str) -> str:
    lolz_profile = text[text.find('Профиль Lolz:') + 14:text.find('Опыт работы:') - 1]
    return lolz_profile
