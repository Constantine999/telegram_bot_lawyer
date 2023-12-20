from datetime import datetime
from pathlib import Path


def get_datetime_now() -> str:
    '''Создает строку формата ДД.ММ.ГГГГ ЧЧ:ММ'''
    return datetime.now().strftime('%d.%m.%Y %H:%M')


def get_message_start() -> str:
    '''Отправляет текст с подробной информацией о юристах'''
    with open(str(Path("content/messages/text_start.txt")), encoding="utf-8") as file:
        return file.read()


def get_contacts_message() -> str:
    '''Отправляет текст c контактами юристов, если запрос был в нерабочее время, отправляет данные без номера телефона'''
    file_name = "text_contacts_not_working_hours.txt" if datetime.now().hour in range(8) else "text_contacts_working_hours.txt"
    with open(str(Path(f"./content/messages/{file_name}")), encoding="utf-8") as file:
        return file.read()


def get_greeting_in_superchat() -> str:
    '''Отправляет приветственный текст в супергруппу'''
    with open(str(Path("content/messages/text_greeting_in_superchat.txt")), encoding="utf-8") as file:
        return file.read()


def get_description_group() -> str:
    '''Отправляет текст описание супергруппы'''
    with open(str(Path("content/messages/text_description_group.txt")), encoding="utf-8") as file:
        return file.read()
