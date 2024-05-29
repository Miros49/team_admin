from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к боту
    admin_ids: list[int]  # Список id админов
    user_chat: int
    admin_chat: int
    payments_channel: int


@dataclass
class ApiKey:
    token: str  # Токен для доступа к api для работы с промокодами


@dataclass
class Proxy:
    ip: str
    port: str
    login: str
    password: str


@dataclass
class DatabaseConfig:
    database: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных


@dataclass
class Config:
    tg_bot: TgBot
    api_key: ApiKey
    proxy: Proxy
    db: DatabaseConfig


def load_config(path: str | None) -> Config:
    env: Env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env('BOT_TOKEN'),
            admin_ids=list(map(int, env.list('ADMIN_IDS'))),
            user_chat=env('USERS_CHAT_ID'),
            admin_chat=env('ADMINS_CHAT_ID'),
            payments_channel=env('PAYMENTS_CHANNEL_ID')),
        api_key=ApiKey(env('API_KEY')),
        proxy=Proxy(
            ip=env('PROXY_IP'),
            port=env('PROXY_PORT'),
            login=env('PROXY_LOGIN'),
            password=env('PROXY_PASSWORD')
        ),
        db=DatabaseConfig(
            database=env('DATABASE'),
            db_host=env('DB_HOST'),
            db_user=env('DB_USER'),
            db_password=env('DB_PASSWORD'))
    )
