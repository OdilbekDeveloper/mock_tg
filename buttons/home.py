import telebot
from telebot import types


def get_home(lang):

    if lang == 'uz':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Test topshirish ⚡️")
        button2 = telebot.types.KeyboardButton(text="Kabinet 👤")
        button3 = telebot.types.KeyboardButton(text="Balans 💰")
        button4 = telebot.types.KeyboardButton(text="Mening natijalarim 🔖")
        button5 = telebot.types.KeyboardButton(text="Yordam 💬")

        keyboard.add(button1)
        keyboard.add(button2, button3)
        keyboard.add(button4, button5)

        return keyboard

    elif lang == 'ru':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Пройти тест ⚡️")
        button2 = telebot.types.KeyboardButton(text="Кабинет 👤")
        button3 = telebot.types.KeyboardButton(text="Баланс 💰")
        button4 = telebot.types.KeyboardButton(text="Мои результаты 🔖")
        button5 = telebot.types.KeyboardButton(text="Помощь 💬")

        keyboard.add(button1)
        keyboard.add(button2, button3)
        keyboard.add(button4, button5)

        return keyboard

    elif lang == 'eng':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="Take a test ⚡️")
        button2 = telebot.types.KeyboardButton(text="Cabinet 👤")
        button3 = telebot.types.KeyboardButton(text="Balance 💰")
        button4 = telebot.types.KeyboardButton(text="My results 🔖")
        button5 = telebot.types.KeyboardButton(text="Help 💬")

        keyboard.add(button1)
        keyboard.add(button2, button3)
        keyboard.add(button4, button5)

        return keyboard

