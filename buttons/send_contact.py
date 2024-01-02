import telebot
from telebot import types


def send_contact():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

    contact_button = types.KeyboardButton(
        text="Raqamimni yuborish📲", request_contact=True)
    markup.add(contact_button)

    return markup
