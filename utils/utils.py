import re

from datetime import timedelta


def find_lolz_profile(text: str) -> str:
    lolz_profile = text[text.find('Профиль Lolz:') + 14:text.find('Опыт работы:') - 1]
    return lolz_profile


def parse_duration(duration: str) -> timedelta | None:
    match = re.match(r"(\d+)([smhd])", duration)
    if not match:
        return None

    value, unit = int(match.group(1)), match.group(2)
    if unit == 's':
        return timedelta(seconds=value)
    elif unit == 'm':
        return timedelta(minutes=value)
    elif unit == 'h':
        return timedelta(hours=value)
    elif unit == 'd':
        return timedelta(days=value)
    return None
