import telebot
from telebot import types


def get_admin():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Statistika📊")
    button2 = telebot.types.KeyboardButton(text="Reklama 📤")
    button3 = telebot.types.KeyboardButton(text="Foydalanuvchilar👤")
    button4 = telebot.types.KeyboardButton(text="Materiallar📄")
    button5 = telebot.types.KeyboardButton(text="Foydalanuvchini o'chirish🗑")

    keyboard.add(button1)
    keyboard.add(button2, button3)
    keyboard.add(button4, button5)

    return keyboard


def get_speaking():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Speaking olish🗣")
    button2 = telebot.types.KeyboardButton(text="Foydalanuvchilar👤")
    button3 = telebot.types.KeyboardButton(text="Yozilganlar⏺")
    button4 = telebot.types.KeyboardButton(text="Materiallar📄")

    keyboard.add(button1)
    keyboard.add(button2, button3)
    keyboard.add(button4)

    return keyboard


def get_writing():
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = telebot.types.KeyboardButton(text="Insho tekshirish✅")
    button2 = telebot.types.KeyboardButton(text="Foydalanuvchilar👤")
    button3 = telebot.types.KeyboardButton(text="Yozilganlar⏺")
    button4 = telebot.types.KeyboardButton(text="Materiallar📄")

    keyboard.add(button1)
    keyboard.add(button2, button3)
    keyboard.add(button4)

    return keyboard