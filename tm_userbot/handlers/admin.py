from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
from pyrogram.types import ChatPermissions, Message

from config import ADMINS_ID, client, ex2
from data_base.groups_activity_db import sql_add_data_groups_activity_db, sql_delete_data_groups_activity_db
from data_base.users_activity_db import sql_add_data_users_activity_db
from services import *


async def create_new_group(_, message: Message):
    '''Генератор приватных чатов.'''
    await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)

    try:
        user_id, first_name, username = eval(message.text.split(maxsplit=1)[1])
    except Exception as error:
        print(f"Таблица не была создана из-за ошибки {type(error).__name__} - {error}")
    else:
        chat_create = get_datetime_now()
        chat_title = f"Консультация от {chat_create}"
        # создаем чат и получаем id чата
        chat_id = str((await client.create_supergroup(chat_title, get_description_group())).__dict__["id"])
        # добавляем фото в чат
        await client.set_chat_photo(chat_id, photo=str(Path("./content/images/pic_logo_chat.png")))
        # отправляем приветственное сообщение в созданный чат
        await client.send_message(chat_id, get_greeting_in_superchat())

        # pin_message = await client.send_message(chat_id, get_greeting_in_superchat())
        # закрепить сообщение в чате
        # await client.pin_chat_message(chat_id=chat_id, message_id=pin_message.id)

        # Задаем правило для участников чата (не администраторов чата)
        await client.set_chat_permissions(
            chat_id=chat_id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_send_polls=False,
                can_add_web_page_previews=True,
                can_change_info=False,
                can_invite_users=False,
                can_pin_messages=False
            )
        )
        # добавляем в чат бота и Юльку
        await client.add_chat_members(chat_id, [ADMINS_ID['BOT_KONSTANTIN']])  # , ADMINS_ID['ROOT_NAME_JULIA']
        # Юльку делаем админом группы
        # await client.promote_chat_member(chat_id, ADMINS_ID['ROOT_NAME_JULIA'])
        # Задаем название должности администраторам чата
        # await client.set_administrator_title(chat_id, ROOT_ID["Angela_tinkoff"], "юрист")
        await client.set_administrator_title(chat_id, ADMINS_ID['KONSTANTIN'], "юрист")
        # await client.set_administrator_title(chat_id, ADMINS_ID['ROOT_NAME_ANGEL'], "юрист")
        # Получаем ссылку чата
        chat_url = (await client.get_chat(chat_id)).__dict__["invite_link"]
        # Отдаем дынные в БД
        sql_add_data_groups_activity_db(
            ex2.connect,
            user_id,
            first_name,
            username,
            chat_id,
            chat_url,
            chat_create
        )

        # чистим от ненужных сообщений в чате
        async for message in client.get_chat_history(chat_id):
            if message.id != 3:
                await client.delete_messages(chat_id, message.id)

        # если чат был создан ночью
        if datetime.now().hour in range(9):
            await client.send_message(
                chat_id,
                "Наш рабочий день начинается с 9:00 по московскому времени. Напишите нам и мы обязательно Вам ответим в рабочее время."
            )


async def command_delete(client: Client, message: Message):
    '''Удаляет супергруппы с ее участниками и историей переписки'''
    await client.delete_messages(chat_id=message.chat.id, message_ids=message.id)
    chat_id = str(message.chat.id)

    # делаем проверку что сообщение не было введено из самого ботбота
    if chat_id not in (ADMINS_ID['BOT_KONSTANTIN'], ADMINS_ID['BOT_ANGEL']):  # это ID ботов

        # удаляем историю сообщений
        async for message in client.get_chat_history(chat_id):
            await client.delete_messages(chat_id, message.id)

        # удаляем участников группы
        async for user in client.get_chat_members(chat_id):
            if str(user.user.id) != ADMINS_ID['KONSTANTIN']:
                await client.ban_chat_member(chat_id, user.user.id)

        # удаляем группу
        await client.delete_supergroup(chat_id)
        # await client.leave_chat(chat_id, delete=True)  # удаляем группу и переписку

        # удаляем информацию о чате из БД
        sql_delete_data_groups_activity_db(ex2.connect, chat_id)


@client.on_message(filters.new_chat_members)
async def new_chat_members(client: Client, message: Message):
    '''Ловит апдейты на вход в чат'''
    user_id = str(message.new_chat_members[0].id)
    if user_id not in ADMINS_ID:
        sql_add_data_users_activity_db(
            ex2.connect,
            user_id,
            f"Зашёл в чат {message.chat.title}, chat_id={message.chat.id}",
            message.new_chat_members[0].first_name,
            message.new_chat_members[0].username,
            str(message.date)
        )


@client.on_message(filters.left_chat_member)
async def left_chat_member(client: Client, message: Message):
    '''Ловит апдейты на выход из чата'''
    user_id = str(message.left_chat_member.id)
    if user_id not in ADMINS_ID:
        sql_add_data_users_activity_db(
            ex2.connect,
            user_id,
            f"Вышел из чата {message.chat.title}, chat_id={message.chat.id}",
            message.left_chat_member.first_name,
            message.left_chat_member.username,
            str(message.date)
        )


def register_handlers_admin(client: Client) -> None:
    '''Регистрирует handlers'''
    client.add_handler(MessageHandler(create_new_group, filters.regex(r'Консультация_c_ID \(.+\)')))
    client.add_handler(MessageHandler(command_delete, filters.command(commands="kill_chat", case_sensitive=False,
                                                                      prefixes="") & filters.outgoing))
