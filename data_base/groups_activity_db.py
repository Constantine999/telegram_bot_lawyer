import psycopg2

from services import get_datetime_now


def sql_start_groups_activity_db(connect: psycopg2) -> None:
    '''Подключение к БД'''
    with connect.cursor() as cursor:
        if cursor:
            print(f"Бот подключился к таблице БД groups_activity_db")
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS groups_activity_db(
                user_id VARCHAR(15) NOT NULL,
                user_firstname VARCHAR(100) NULL,
                username VARCHAR(40) NULL,                
                chat_id VARCHAR(40) NOT NULL,
                chat_url VARCHAR(40) NOT NULL,
                chat_create VARCHAR(20) NOT NULL,
                chat_status VARCHAR(6) DEFAULT 'active')"""
            )


def sql_read_data_groups_activity_db(connect: psycopg2, user_id: str) -> tuple[str, str] | tuple:
    '''Проверяет в БД chat_status'''
    with connect.cursor() as cursor:
        cursor.execute("SELECT * FROM groups_activity_db WHERE user_id = (%s) AND chat_status = 'active';", (user_id,))
        result = cursor.fetchone()
        return result if result else ()


def sql_add_data_groups_activity_db(
        connect: psycopg2,
        user_id: str,
        user_firstname: str,
        username: str,
        chat_id: str,
        chat_url: str,
        chat_create: str) -> None:
    '''Добавляет новую строку в БД при создании новой группы'''
    values = (user_id, user_firstname, username, chat_id, chat_url, chat_create)

    with connect.cursor() as cursor:
        cursor.execute(
            "INSERT INTO groups_activity_db (user_id,  user_firstname, username, chat_id, chat_url, chat_create) VALUES (%s, %s, %s, %s, %s, %s);",
            values)
        print("{} был создан чат {} для пользователя {} c ID={}".format(chat_create, chat_url, user_firstname, user_id))


def sql_delete_data_groups_activity_db(connect: psycopg2, chat_id: str) -> None:
    '''Удаляет группу(чат)'''
    with connect.cursor() as cursor:
        cursor.execute("UPDATE groups_activity_db SET chat_status = 'delete' WHERE chat_id = (%s);", (chat_id,))
        print(f"Удалён чат с номером {chat_id}, время удаления - {get_datetime_now()}")
