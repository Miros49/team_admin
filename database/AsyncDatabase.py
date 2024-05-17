from sqlalchemy import Integer, Double, JSON, BINARY, DateTime
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

import asyncpg
from sqlalchemy.sql import or_, and_
from sqlalchemy import Column, MetaData, select, BigInteger, String, SmallInteger, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

meta = MetaData()


class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    lolz_profile = Column(String)
    tutor = Column(String)
    name_in_withdraws = Column(String)
    status = Column(Integer, default=0)
    nickname = Column(String)


class Statistics(Base):
    __tablename__ = 'statistics'
    id = Column(BigInteger, primary_key=True)
    balance = Column(Double, default=0.00)
    cash_flow = Column(Double, default=0.00)
    percent = Column(Integer, default=65)
    registrations_number = Column(Integer, default=0)


class Wallets(Base):
    __tablename__ = 'wallets'
    id = Column(BigInteger, primary_key=True)
    btc = Column(String)
    erc_20 = Column(String)
    trc_20 = Column(String)
    tron = Column(String)


class Limits(Base):
    __tablename__ = 'limits'
    id = Column(BigInteger, primary_key=True)
    proxies = Column(Integer)
    numbers = Column(Integer)

# # -------------При первом запуске раскомментировать вот этот код, после срау закомментировать-----------------#
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
        self.engine = create_async_engine(self.database_url, echo=True)
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def set_user(self, user_id: int):
        async with self.async_session() as session:
            async with session.begin():
                user = User(id=user_id)
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

    async def get_all_invoices(self):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User)
                result = await session.execute(query)
                user = result.scalars().all()
                ret = {}
                for i in user:
                    if i.invoice_ids != "":
                        ret[i.id] = i.invoice_ids
                return ret

    async def user_update_invoices(self, user_id, invoices_id):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                user.invoice_ids = invoices_id
                await session.commit()

    async def user_update_balance(self, user_id, type, amount):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                if type == "topup":
                    balance = round(float(user.balance) + amount, 2)
                else:
                    balance = round(float(user.balance) - amount, 2)
                user.balance = balance
                await session.commit()

    async def swap_lang(self, user_id):
        async with self.async_session() as session:
            async with session.begin():
                query = select(User).filter(User.id == user_id)
                result = await session.execute(query)
                user = result.scalars().first()
                lang = str(user.lang)
                if lang == "eng":
                    user.lang = "ru"
                else:
                    user.lang = "eng"
                await session.commit()
