from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

client_kb = ReplyKeyboardMarkup(resize_keyboard=True,
                                input_field_placeholder="задайте вопрос бесплатно",
                                is_persistent=True
                                )
# button_1 = KeyboardButton(text="💬 ПОЛУЧИТЬ ОНЛАЙН КОНСУЛЬТАЦИЮ")
# button_2 = KeyboardButton(text="⚖️ О НАС")
button_2 = KeyboardButton(text="☑️ О НАС. ВОПРОСЫ И ОТВЕТЫ")
button_3 = KeyboardButton(text="📄 УСЛУГИ И ЦЕНЫ")
button_4 = KeyboardButton(text="☎️ НАШИ КОНТАКТЫ")

client_kb.add(button_2)
client_kb.add(button_3, button_4)
