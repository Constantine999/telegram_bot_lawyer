import os

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode

from data_base import connectdb

load_dotenv()

# Список админов (участников проекта)
ADMINS_ID = {
    'KONSTANTIN': os.environ.get('ROOT_ID_KONSTANTIN'),
    'ANGEL': os.environ.get('ROOT_ID_ANGEL'),
    'JULIA': os.environ.get('ROOT_ID_JULIA'),
    'BOT_KONSTANTIN': os.environ.get('ROOT_NAME_BOT_KONSTANTIN'),
    'BOT_ANGEL': os.environ.get('ROOT_NAME_BOT_ANGEL'),
}

# Данные для подключения к Pyrogram
client = Client(
    name=os.environ.get('API_NAME_KONSTANTIN'),
    api_id=os.environ.get('API_ID_KONSTANTIN'),
    api_hash=os.environ.get('API_HASH_KONSTANTIN'),
    parse_mode=ParseMode.HTML
)

# Созданный клиент для aiogram
bot = Bot(token=os.environ.get('BOT_TOKEN_KONSTANTIN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=bot)

# Данные для подключения PostgreSQL
database_config = {
    'host': os.environ.get('HOST'),
    'user': os.environ.get('USER'),
    'password': os.environ.get('PASSWORD'),
    'db_name': os.environ.get('DB_NAME'),
    'port': os.environ.get('PORT'),
}

# Подключение для aiogram бота
ex1 = connectdb.ConnectDB(*database_config.values())
# Подключение для Pyrogram бота
ex2 = connectdb.ConnectDB(*database_config.values())
