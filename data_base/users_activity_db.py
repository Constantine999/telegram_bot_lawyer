# Здесь происходит взаимодествие с БД, куда мы вносим все действия пользователей в боте
from typing import Optional

import psycopg2


def sql_start_users_activity_db(connect: psycopg2) -> None:
    with connect.cursor() as cursor:
        if cursor:
            print(f"Бот подключился к таблице БД users_activity_db")
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS users_activity_db(
            user_id VARCHAR(15) NOT NULL,
            action_user VARCHAR(4096) NOT NULL,
            user_firstname VARCHAR(100) NULL,
            username VARCHAR(40) NULL,
            user_datetime_action VARCHAR(20) NOT NULL)"""
        )


def sql_add_data_users_activity_db(
        connect: psycopg2,
        user_id: str,
        action_user: str,
        user_firstname: str,
        username: Optional[str],
        user_datetime_action: str) -> None:
    with connect.cursor() as cursor:
        values = user_id, action_user[:4096], user_firstname, username, user_datetime_action
        cursor.execute(
            "INSERT INTO users_activity_db (user_id, action_user, user_firstname, username, user_datetime_action) VALUES (%s, %s, %s, %s, %s)",
            values
        )
    print(f"Данные добавлены {values}")
