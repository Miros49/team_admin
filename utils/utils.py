import re

from datetime import timedelta


def find_lolz_profile(text: str) -> str:
    lines = text.strip().split('\n')

    lolz_profile = None

    for line in lines:
        if line.startswith('Профиль Lolz:'):
            lolz_profile = line.split('Профиль Lolz:')[1].strip()
            break

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


def parse_deposit(text: str):
    lines = text.strip().split('\n')

    amount = None
    worker = None

    for line in lines:
        if line.startswith('сумма:'):
            try:
                amount = float(line.split('сумма:')[1].strip())
            except ValueError:
                raise ValueError("Некорректная сумма")
        elif line.startswith('воркер:'):
            worker = line.split('воркер:')[1].strip()

    return amount, worker
