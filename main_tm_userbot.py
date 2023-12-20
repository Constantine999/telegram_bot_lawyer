from config import client, ex2
from data_base.groups_activity_db import sql_start_groups_activity_db
from data_base.users_activity_db import sql_start_users_activity_db
from services import get_datetime_now
from tm_userbot.handlers.admin import register_handlers_admin


def start_bot_pyrogram():
    '''Точка старта Pyrogram бота'''
    print(f"Бот pyrogram вышел в online - {get_datetime_now()}")
    register_handlers_admin(client)
    sql_start_groups_activity_db(ex2.connect)
    sql_start_users_activity_db(ex2.connect)
    client.run()
    print(f"Бот pyrogram вышел в offline - - {get_datetime_now()}")


if __name__ == "__main__":
    start_bot_pyrogram()
