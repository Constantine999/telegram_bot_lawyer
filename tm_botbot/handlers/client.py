from aiogram import Dispatcher, filters, types
from aiogram.utils.exceptions import BotKicked, MessageCantBeDeleted

from config import ADMINS_ID, bot, ex1
from data_base.groups_activity_db import sql_read_data_groups_activity_db
from data_base.users_activity_db import sql_add_data_users_activity_db
from services import *
from services import get_datetime_now
from tm_botbot.keyboards.client_kb import client_kb


async def add_base_action(message: types.Message, content=None) -> None:
    '''Добавляет информацию по отработанным хендлерам в таблицу БД.'''
    if str(message.from_user.id) not in ADMINS_ID:
        sql_add_data_users_activity_db(
            ex1.connect,
            str(message.from_user.id),
            content,
            message.from_user.first_name,
            message.from_user.username,
            get_datetime_now()
        )


async def command_start(message: types.Message):
    '''После нажатия на кнопку отправляет приветствие.'''
    await bot.send_photo(
        message.from_user.id,
        types.InputFile(str(Path("./content/images/pic_start.jpg"))),
        caption=f"<b>{message.from_user.first_name.title()}, приветствуем Вас!</b>\n\n{get_message_start()}",
        reply_markup=client_kb,
        parse_mode="HTML"
    )
    await message.delete()
    await add_base_action(message, message.text)


async def command_price(message: types.Message):
    '''После нажатия на кнопку отправляет картинку с ценами.'''
    await bot.send_photo(
        message.from_user.id,
        types.InputFile(str(Path("./content/images/pic_price.png"))),
        reply_markup=client_kb,
        disable_notification=True,
        caption="<b>📄 УСЛУГИ И ЦЕНЫ</b>",
        parse_mode="HTML"
    )
    await message.delete()
    await add_base_action(message, message.text)


async def command_contacts(message: types.Message):
    '''После нажатия на кнопку отправляет контакты юристов.'''
    await bot.send_message(
        message.from_user.id,
        get_contacts_message(),
        reply_markup=client_kb,
        parse_mode="HTML"
    )
    await message.delete()
    await add_base_action(message, message.text)


async def command_us(message: types.Message):
    '''После нажатия на кнопку информацию о нас с вопросами и ответами.'''
    await message.delete()
    await message.answer_document(
        types.InputFile(str(Path("./content/images/о_нас.png"))),
        caption="☑️ О НАС. ВОПРОСЫ И ОТВЕТЫ",
        disable_notification=True,
        reply_markup=client_kb
    )
    await add_base_action(message, message.text)


async def command_consultation(message: types.message):
    '''После нажатия на кнопку отправляет ссылку на сгенерированный чат.'''
    try:
        # делаем проверку на то что мы не отвечаем боту на его сообщение
        message.reply_to_message["from"]["is_bot"] == True
    except TypeError:
        _id = message.from_user.id
        try:
            await message.delete()
        except MessageCantBeDeleted as error:
            print(f"Ошибка в command_consultation - {error}, {get_datetime_now()}, ID-{_id} {message.text}")

        user_id = str(message.from_user.id)
        chat_url = None

        if sql_read_data_groups_activity_db(ex1.connect, user_id):
            chat_url = sql_read_data_groups_activity_db(ex1.connect, user_id)[-3]
        else:
            user_info = str(message.from_user.id), message.from_user.first_name, message.from_user.username
            await bot.send_message(ADMINS_ID['KONSTANTIN'], f"Консультация_c_ID {user_info}")
            while not chat_url:
                if sql_read_data_groups_activity_db(ex1.connect, user_id):
                    chat_url = sql_read_data_groups_activity_db(ex1.connect, user_id)[-3]

        chat_id = sql_read_data_groups_activity_db(ex1.connect, user_id)[3]
        user_firstname = message.from_user.first_name
        await bot.send_message(
            message.from_user.id,
            "<b>Ваше сообщение было отправлено юристам. Для получения ответа нажмите - 'ОТКРЫТЬ ГРУППУ' ⬇️</b>",
            reply_markup=client_kb
        )
        content = None

        # Получение текстового сообщения от пользователя
        if message.content_type == "text":
            await bot.send_message(
                chat_id,
                f"<b>{user_firstname} отправил(а) сообщение:</b>\n'{message.text}'",
                parse_mode="HTML"
            )
            content = f"Отправил текст - {message.text}"

        # Получение звукового сообщения от пользователя
        if message.content_type == "voice":
            await bot.send_message(
                chat_id,
                f"<b>{user_firstname} отправил(а) звуковое сообщение:</b>",
                parse_mode="HTML"
            )
            await bot.send_voice(
                chat_id,
                message.voice.file_id
            )
            content = "Отправлено звуковое сообщение"

        # Получение картинки от пользователя
        if message.content_type == "photo":
            await bot.send_message(
                chat_id,
                f"<b>{user_firstname} отправил(а) картинку:</b>",
                parse_mode="HTML"
            )
            await bot.send_photo(
                chat_id,
                message.photo[-1].file_id,
                caption=message.caption
            )
            content = "Отправлено фото"

        # Получение документа от пользователя
        if message.content_type == "document":
            await bot.send_message(
                chat_id,
                f"<b>{user_firstname} отправил(а) файл:</b>",
                parse_mode="HTML"
            )
            await bot.send_document(
                chat_id,
                message.document.file_id,
                caption=message.caption
            )
            content = "Отправлен документ"

        await message.answer(chat_url, reply_markup=client_kb)
        await add_base_action(message, content)


async def delete_content_commands(message: types.Message):
    "Игнорирует весь ненужный контент."
    if str(message.from_user.id) not in ADMINS_ID and message.content_type not in \
            ('new_chat_members', 'left_chat_member'):
        user_id = message.from_user.id
        try:
            await message.delete()
        # при удалении сообщений могут возникнуть ошибки, их необходимо исключать
        except (MessageCantBeDeleted, BotKicked) as error:
            print(f"delete_content_commands - {error}, {get_datetime_now()}, ID-{user_id}, {message.content_type}")
        finally:
            await add_base_action(message, message.content_type)


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, filters.Text(equals="/start"))
    dp.register_message_handler(command_us, filters.Text(equals="☑️ О НАС. ВОПРОСЫ И ОТВЕТЫ"))
    dp.register_message_handler(command_price, filters.Text(equals="📄 УСЛУГИ И ЦЕНЫ"))
    dp.register_message_handler(command_contacts, filters.Text(equals="☎️ НАШИ КОНТАКТЫ"))
    dp.register_message_handler(command_consultation,
                                content_types=[types.ContentType.TEXT, types.ContentType.VOICE,
                                               types.ContentType.PHOTO, types.ContentType.DOCUMENT])
    dp.register_message_handler(delete_content_commands, content_types=types.ContentType.ANY)
