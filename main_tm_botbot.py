from aiogram.utils import executor

from config import dp
from services import get_datetime_now
from tm_botbot.handlers import client


def start_bot_aiogram():
    '''Точка старта aiogram бота'''
    print(f"Бот aiogram вышел в online - {get_datetime_now()}")
    client.register_handlers_client(dp)
    executor.start_polling(dispatcher=dp, skip_updates=True)
    print(f"Бот aiogram вышел в offline - {get_datetime_now()}")


if __name__ == "__main__":
    start_bot_aiogram()
