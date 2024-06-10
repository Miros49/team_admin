from sqlalchemy import Integer, Double, JSON, BINARY, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

import asyncpg
from sqlalchemy.sql import or_, and_
from sqlalchemy import Column, MetaData, select, BigInteger, String, DECIMAL, SmallInteger, create_engine, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

meta = MetaData()


class Admin(Base):
    __tablename__ = 'admins'
    id = Column(BigInteger, primary_key=True)
    username = Column(String)


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, unique=True)
    lolz_profile = Column(String)
    tutor = Column(String)
    status = Column(String, default="Воркер")
    nickname = Column(String)
    balance = Column(DECIMAL(10, 2), default=0.00)
    username = Column(String, unique=True, nullable=False)
    banned = Column(Integer, default=0)
    users_count = Column(Integer, default=0)
    total_turnover = Column(DECIMAL(10, 2), default=0.00)
    your_ref = Column(BigInteger, default=0)
    ref_num = Column(SmallInteger, default=0)


class Promocodes(Base):
    __tablename__ = 'promocodes'
    id = Column(BigInteger, primary_key=True, unique=True)
    num = Column(SmallInteger, nullable=False, default=0)
    promocodes = Column(ARRAY(String))


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(BigInteger, primary_key=True)
    balance = Column(Double, default=0.00)
    cash_flow = Column(Double, default=0.00)
    percent = Column(Integer, default=50)
    registrations_number = Column(Integer, default=0)


class Wallets(Base):
    __tablename__ = 'wallets'
    id = Column(BigInteger, primary_key=True)
    btc = Column(String)
    eth = Column(String)
    trc20 = Column(String)
    trx = Column(String)


class Limits(Base):
    __tablename__ = 'limits'
    id = Column(BigInteger, primary_key=True)
    proxies = Column(Integer)
    numbers = Column(Integer)


# # -------------При первом запуске раскомментировать вот этот код, после сразу закомментировать-----------------#
# connection = psycopg2.connect(user="postgres", password="1111")
# connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#
# # Создаем курсор для выполнения операций с базой данных
# cursor = connection.cursor()
# sql_create_database = cursor.execute('create database team_admin')
# # Создаем базу данных
# engine = create_engine("postgresql+psycopg2://postgres:1111@localhost/team_admin")
# # Закрываем соединение
# cursor.close()
# connection.close()
#
# meta.create_all(engine)


class DataBase:
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_async_engine(self.database_url, echo=False)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_admins_ids(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin)
                result = await session.execute(query)
                admin_ids = [admin.id for admin in result.scalars().all()]
                return admin_ids

    async def get_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin).filter(Admin.id == admin_id)
                result = await session.execute(query)
                admin = result.scalars().first()
                return admin

    async def set_admin_username(self, admin_id: int, username: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin).filter(Admin.id == admin_id)
                result = await session.execute(query)
                admin = result.scalars().first()
                admin.username = username
                await session.commit()

    async def add_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                admin = User(id=admin_id)
                session.add(admin)
                return await session.commit()

    async def get_admins(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin)
                result = await session.execute(query)
                admins = result.scalars().all()
                return admins

    async def delete_admin(self, admin_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Admin).filter(Admin.id == admin_id)
                result = await session.execute(query)
                admin = result.scalars().first()
                if admin:
                    await session.delete(admin)
                    await session.commit()
                    return True

    async def get_admins_usernames(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                user_ids = [user.id for user in result.scalars().all()]
                return user_ids

    async def set_user(self, user_id: int, username: str, lolz_profile: str | None = None,
                       ref_id: str | int | None = None):
        async with self.async_session() as session:
            async with session.begin():
                user = User(id=user_id, username=username, lolz_profile=lolz_profile, balance=0.00,
                            your_ref=int(ref_id) if ref_id else 0)
                session.add(user)
                await session.commit()
                return user.id

    async def get_user(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def get_user_by_username(self, username: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.username == username)
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def user_exists(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user:
                    return True
                else:
                    return False

    async def get_all_users(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                user_ids = [user.id for user in result.scalars().all()]
                return user_ids

    async def set_lolz_profile(self, user_id: int, lolz_profile):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user.lolz_profile == " " or user.lolz_profile is None or user.lolz_profile == "":
                    lolz_profile = lolz_profile
                else:
                    lolz_profile = str(user.lolz_profile)
                user.lolz_profile = lolz_profile
                await session.commit()

    async def set_nickname(self, user_id: int, nickname: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.nickname = nickname
                await session.commit()

    async def set_status(self, user_id: int, status: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.status = status
                await session.commit()

    async def edit_balance(self, user_id: int, amount: float):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                balance = round(float(user.balance) + amount, 2)
                user.balance = balance
                await session.commit()

    async def ban_user(self, user_id: int | None = None, username: str | None = None, ban: bool = True):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if ban:
                    user.banned = 1
                else:
                    user.banned = 0
                await session.commit()

    async def add_ref(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == int(user_id))
                result = await session.execute(query)
                user = result.scalars().first()
                user.ref_num = user.ref_num + 1
                await session.commit()

    async def get_total_turnover_by_referrer(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(func.sum(User.total_turnover)).filter(User.your_ref == int(user_id))
                result = await session.execute(query)
                total_turnover = result.scalar()
                return total_turnover if total_turnover is not None else 0.00

    async def set_user_promocodes(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                user = Promocodes(id=int(user_id))
                session.add(user)
                await session.commit()
                return user.id

    async def get_promocodes(self, user_id: int | str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Promocodes).filter(Promocodes.id == int(user_id))
                result = await session.execute(query)
                user = result.scalars().first()
                return user

    async def add_promocode(self, user_id: int | str, promocode: str):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Promocodes).filter(Promocodes.id == int(user_id))
                result = await session.execute(query)
                user = result.scalars().first()
                if not user:
                    new_user = Promocodes(id=int(user_id), num=1, promocode=[promocode])
                    session.add(new_user)
                elif user.num < 3:
                    user.promocodes.append(promocode)
                    user.num += 1
                await session.commit()

    async def set_wallet(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                user = Wallets(id=user_id)
                session.add(user)
                await session.commit()
                return user.id

    async def wallet_exists(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Wallets).filter(Wallets.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if user:
                    return True
                else:
                    return False

    async def add_wallet(self, user_id: int, wallet: dict):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Wallets).filter(Wallets.id == user_id)
                result = await session.execute(query)
                wallets = result.scalars().first()

                if wallets:
                    for key, value in wallet.items():
                        if hasattr(wallets, key):
                            setattr(wallets, key, value)
                    await session.commit()
                else:
                    # Если кошелек не найден, можно поднять исключение или обработать этот случай иным образом.
                    raise ValueError(f"Wallet for user_id {user_id} not found.")

    async def get_wallets(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Wallets).filter(Wallets.id == user_id)
                result = await session.execute(query)
                wallets = result.scalars().first()
                return wallets

    async def get_linked_wallets(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                query = select(Wallets).filter(Wallets.id == user_id)
                result = await session.execute(query)
                wallets = result.scalars().first()

                if wallets:
                    linked_wallets = {
                        'btc': wallets.btc,
                        'eth': wallets.eth,
                        'trc20': wallets.trc20,
                        'trx': wallets.trx
                    }
                    return {k: v for k, v in linked_wallets.items() if v}
                else:
                    return {}
