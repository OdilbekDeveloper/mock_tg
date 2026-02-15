# Importing packages
from enum import property

import telebot
from telebot import *
import sqlite3
import requests
import json
import os
from telebot.types import ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
# Importing functions or buttons
from buttons.admin import get_admin as admin_buttons
from buttons.admin import get_speaking as adminS_buttons
from buttons.admin import get_writing as adminW_buttons
from buttons.home import get_home
from config import *
from functions.user_exists import user_exists, username_exists
from buttons.send_contact import send_contact
from functions.user_data import get_user_data, is_allowed_number
from functions.get_user_result import get_user_result
from functions.check_balance_for_test import check_balance_for_test, get_prices
from functions.edit_user import edit_user, edit_user_status, edit_user_cabinet
from functions.filter_candidates import filter_candidates
from functions.speaking_test import create_speakingtest, question_speaking
from functions.writing_test import get_essays_unchecked, get_users_writing_unchecked, create_writing
from functions.token import saveToken, delete_token
from functions.get_statistics import get_statistics
from functions.get_lang import get_lang, update_lang
from functions.add_payment import Add_payment, GenerateLink_Click
from functions.referral import Add_referral
from functions.get_result import Check_Result
from functions.sendmessageall import SendMessageAll

import random
from config import  provider_token, error_group_id
from apscheduler.schedulers.blocking import BlockingScheduler

# importing urls
from elements.urls import mysite, api
from elements.urls import register_url
from elements.texts import *


sched = BlockingScheduler()

bot = telebot.TeleBot(BOT_TOKEN)

admins = [8378412613, 5643782731]

conn = sqlite3.connect("database.db")
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS user
             (id INTEGER PRIMARY KEY, token TEXT, telegram_id INTEGER, lang TEXT)''')

conn.commit()


@bot.message_handler(commands=['start'])
def start(message):
    if user_exists(message.chat.id) == True:
        lang = get_lang(message.chat.id)
        if lang == 'uz':
            bot.send_message(message.chat.id, text="🔰Bosh menyu",
                             reply_markup=get_home(lang))

        elif lang == 'ru':
            bot.send_message(message.chat.id, text="🔰Главное меню",
                             reply_markup=get_home(lang))

        elif lang == 'eng':
            bot.send_message(message.chat.id, text="🔰Main menu",
                             reply_markup=get_home(lang))

    else:
        start_command = message.text
        referrer_id = str(start_command[7:])
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="O'zbekcha🇺🇿")
        button2 = telebot.types.KeyboardButton(text="Русский🇷🇺")
        button3 = telebot.types.KeyboardButton(text="English🇺🇸")

        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, '🇺🇿Tilni tanlang\n🇷🇺Выберите язык\n🇺🇸Select your language', reply_markup=keyboard)
        bot.register_next_step_handler(message, register_user, referrer_id)


# Admin panel

@bot.message_handler(commands=['admin'])
def admin_main(message):
    res = get_user_data(message.chat.id)
    resjson = json.loads(res)

    if resjson['type'] == 2:
        bot.send_message(message.chat.id, text="Admin panelga xush kelibsiz🙃👎🏻", reply_markup=admin_buttons())

    elif resjson['type'] == 3:
        bot.send_message(message.chat.id, text="Examiner paneliga xush kelibsiz🙃👎🏻", reply_markup=adminS_buttons())

    elif resjson['type'] == 4:
        bot.send_message(message.chat.id, text="Examiner paneliga xush kelibsiz🙃👎🏻", reply_markup=adminW_buttons())

    else:
        bot.send_message(message.chat.id, text="Siz admin emassiz")



@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):

    if message.text == "Statistika📊":
        stats = get_statistics()
        stats_json = json.loads(stats)

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button = types.InlineKeyboardButton("Yangilash🔄", callback_data='refresh_stats')
        keyboard.add(button)

        bot.send_message(message.chat.id, f"Statistik ma'lumotlar📊\n\n⚡️Botdagi barcha foydalanuvchilar: {stats_json['users']}\n🗓Bugun qo'shilganlar: {stats_json['users_today']}\n⚡️Umumiy sotilgan testlar: {stats_json['tests']}\n🗓Bugun sotilgan testlar: {stats_json['tests_today']}", reply_markup=keyboard)

    elif message.text == "Reklama 📤":
        res = get_user_data(message.chat.id)
        resjson = json.loads(res)

        if resjson['type'] == 2:
            bot.send_message(message.chat.id, "Reklama matnini yuboring\nBekor qilish uchun /cancel")
            bot.register_next_step_handler(message, sendmessageall)

    elif message.text == "Foydalanuvchini o'chirish🗑":
        bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan foydalanuvchi telegram ID raqamini yuboring")
        bot.register_next_step_handler(message, delete_user)

    elif message.text == "Insho tekshirish✅":

        users = json.loads(get_users_writing_unchecked().text)
        users_list = "Ularning ro'yhati📝:\n"
        users_count = 0
        for user in users:
            users_count +=1
            user_info = f"{users_count}){user['last_name']} {user['first_name']}  ID: {user['id']}\n"
            users_list += user_info

        if users_count > 0:
            bot.send_message(message.chat.id, f"Inshosi tekshirilishi kutilayotgan foydalanuvchilar: {users_count}ta\n\n{users_list}", reply_markup=types.ReplyKeyboardRemove())
            bot.send_message(message.chat.id, "Inshosini tekshirmoqchi bo'lgan user ID raqamini yuboring")
            bot.register_next_step_handler(message, get_user_writing_with_id)
        else:
            bot.send_message(message.chat.id, "Barcha insholar tekshirilgan. Birozdan so'ng qayta urining")

    elif message.text == "Materiallar📄":

        bot.send_message(message.chat.id, "Kechirasiz🥲 bu bo'lim hozircha ta'mirda♻️")
    elif message.text == "Yozilganlar⏺":

        bot.send_message(message.chat.id, "Kechirasiz🥲 bu bo'lim hozircha ta'mirda♻️")

    elif message.text == "Speaking olish🗣":
        users = filter_candidates(3)
        users_json = json.loads(users)
        users_list = "Ularning ro'yhati📝:\n"

        users_count = 0
        for user in users_json:
            users_count +=1
            user_info = f"{users_count}){user['last_name']} {user['first_name']} {user['telegram_id']}\n"
            users_list += user_info

        bot.send_message(message.chat.id, f"🥸Speaking olinishi kutilayotgan foydalanuvchilar: {users_count}ta\n\n{users_list}", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "Speaking olmoqchi bo'lgan user ID raqamini yuboring")
        bot.register_next_step_handler(message, get_user_speaking_with_id)


    elif message.text == "Foydalanuvchilar👤":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        button1 = types.InlineKeyboardButton("Bo'sh👋", callback_data='users_free')
        button2 = types.InlineKeyboardButton("Testda🤌", callback_data='users_testing')
        button3 = types.InlineKeyboardButton("Speaking🥸", callback_data='users_speaking')
        keyboard.add(button1, button2, button3)
        bot.send_message(message.chat.id, "Qaysi foydalanuvchilar kerak?", reply_markup=keyboard)

    elif message.text == "Пройти тест ⚡️":
        is_enough = check_balance_for_test(message.chat.id)
        if is_enough == True:
            bot.reply_to(message, text="Тест начинается. Пожалуйста, подождите.", reply_markup=ReplyKeyboardRemove())
            user_data = get_user_data(message.chat.id)
            data = json.loads(user_data)
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            phone = data['phone']
            balance1 = data['balance']
            url = f"{mysite}/api/get/test_details/"
            res2 = requests.get(url).text
            res2_data = json.loads(res2)
            balance = balance1 - int(res2_data['price1'])
            a = edit_user(username,
                          first_name, last_name, phone, balance, message.chat.id)
            edit_user_status(message.chat.id, status=2)
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text='Начать тест🚀', callback_data='start_test')
            markup.add(button)

            bot.send_message(
                message.chat.id,
                text=f"Username: `{username}`\n\nСкопируйте имя пользователя, чтобы начать тест.. \n\nИспользуйте кнопку ниже, чтобы начать тест👇",
                reply_markup=markup, parse_mode="Markdown")
        else:
            bot.reply_to(
                message, text="Недостаточно средств Пополните свой счет")

    elif message.text == "Take a test ⚡️":
        is_enough = check_balance_for_test(message.chat.id)
        if is_enough == True:
            bot.reply_to(message, text="The test is starting. Please wait", reply_markup=ReplyKeyboardRemove())
            user_data = get_user_data(message.chat.id)
            data = json.loads(user_data)
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            phone = data['phone']
            balance1 = data['balance']
            url = f"{mysite}/api/get/test_details/"
            res2 = requests.get(url).text
            res2_data = json.loads(res2)
            balance = balance1 - int(res2_data['price1'])
            a = edit_user(username,
                          first_name, last_name, phone, balance, message.chat.id)
            edit_user_status(message.chat.id, status=2)
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text='Start the test🚀', callback_data='start_test')
            markup.add(button)

            bot.send_message(
                message.chat.id,
                text=f"Username: `{username}`\n\nCopy the username to start the test. \n\nUse the button below to start the test👇",
                reply_markup=markup, parse_mode="Markdown")
        else:
            bot.reply_to(
                message, text="Insufficient funds. Top up your account")

    elif message.text == "Test topshirish ⚡️":
        is_enough = check_balance_for_test(message.chat.id)
        if is_enough == True:
            bot.reply_to(message, text="Test boshlanyapti.Biroz kuting", reply_markup=ReplyKeyboardRemove())
            user_data = get_user_data(message.chat.id)
            data = json.loads(user_data)
            first_name = data['first_name']
            last_name = data['last_name']
            username = data['username']
            phone = data['phone']
            balance1 = data['balance']
            url = f"{mysite}/api/get/test_details/"
            res2 = requests.get(url).text
            res2_data = json.loads(res2)
            balance = balance1 - int(res2_data['price1'])
            a = edit_user(username,
                      first_name, last_name, phone, balance, message.chat.id)
            edit_user_status(message.chat.id, status=2)
            markup = telebot.types.InlineKeyboardMarkup()
            button = telebot.types.InlineKeyboardButton(
                text='Testni boshlash🚀', callback_data='start_test')
            markup.add(button)

            bot.send_message(
            message.chat.id, text=f"Username: `{username}`\n\nTestni boshlash uchun usernameni nusxalab oling. \n\nTestni boshlash uchun quyidagi tugmadan foydalaning👇", reply_markup=markup, parse_mode="Markdown")
        else:
            bot.reply_to(
                message, text="Mablag' yetarli emas hisobingizni to'ldiring")
    elif message.text == 'Kabinet 👤':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            "Ma'lumotlarni o'zgartirish✏️", callback_data='edit_cabinet')
        button2 = types.InlineKeyboardButton(
            "Tilni o'zgartirish⚙️", callback_data='update_lang')
        keyboard.add(button1, button2)

        bot.reply_to(message, text=home_cabinet(
            message.chat.id), reply_markup=keyboard)

    elif message.text == "Кабинет 👤":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            "Изменить личные данные✏️", callback_data='edit_cabinet')
        button2 = types.InlineKeyboardButton(
            "Изменить язык⚙️", callback_data='update_lang')
        keyboard.add(button1, button2)

        bot.reply_to(message, text=home_cabinet(
            message.chat.id), reply_markup=keyboard)

    elif message.text == "Cabinet 👤":
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            "Edit details✏️", callback_data='edit_cabinet')
        button2 = types.InlineKeyboardButton(
            "Change language⚙️", callback_data='update_lang')
        keyboard.add(button1, button2)

        bot.reply_to(message, text=home_cabinet(
            message.chat.id), reply_markup=keyboard)

    elif message.text == 'Balans 💰':
        res = get_user_data(message.chat.id)
        res_json = json.loads(res)
        balance = res_json['balance']

        balance = f"{balance:,}"

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Pul solish💸', callback_data='add_payment')
        button2 = types.InlineKeyboardButton(
            'Referral👥', callback_data='referral_link')

        keyboard.add(button1)
        keyboard.add(button2)
        bot.reply_to(
            message, text=f"""💰Balans: {balance} so'm \n\n🔄Hisobingizni to'ldirish uchun pastdagi tugmadan foydalaning""", reply_markup=keyboard)

    elif message.text == 'Баланс 💰':
        res = get_user_data(message.chat.id)
        res_json = json.loads(res)
        balance = res_json['balance']

        balance = f"{balance:,}"

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Пополнить счет💸', callback_data='add_payment')
        button2 = types.InlineKeyboardButton(
            'Реферрал👥', callback_data='referral_link')
        keyboard.add(button1)
        keyboard.add(button2)
        bot.reply_to(
            message, text=f"""💰Баланс: {balance} сум \n\n🔄Используйте кнопку ниже, чтобы пополнить свой счет""", reply_markup=keyboard)

    elif message.text == 'Balance 💰':
        res = get_user_data(message.chat.id)
        res_json = json.loads(res)
        balance = res_json['balance']

        balance = f"{balance:,}"

        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Top up account💸', callback_data='add_payment')
        button2 = types.InlineKeyboardButton(
            'Referral👥', callback_data='referral_link')
        keyboard.add(button1)
        keyboard.add(button2)
        bot.reply_to(
            message, text=f"""💰Balance: {balance} sum \n\n🔄Use the button below to top up your account""", reply_markup=keyboard)


    elif message.text == 'Mening natijalarim 🔖':
        res = get_user_result(message.chat.id)
        if res.status_code == 404:
            bot.reply_to(
                message, text="Siz biror marta test topshirmagan ekansiz☹️")
        else:
            data = json.loads(res.text)
            user_name = data[0]["user"]["last_name"] + \
                " " + data[0]["user"]["first_name"]
            test_count = len(data)
            highest_listening_score = max(
                result["listening"]["band_score"] for result in data)
            highest_reading_score = max(
                result["reading"]["band_score"] for result in data)
            highest_writing_score = max(
                result["writing"]["band_score"] for result in data)
            highest_speaking_score = max(
                result["speaking"]["band_score"] for result in data)
            last_test_date = data[-1]["date_joined"]

            # Convert the string to a datetime object
            parsed_date = datetime.strptime(last_test_date, "%Y-%m-%dT%H:%M:%S.%f%z")

            # Format the datetime object to the desired format
            formatted_date = parsed_date.strftime("%B %d, %Y. %H:%M")
            # Format the variable
            result_variable = (
                f"👤Ism familiya: {user_name}\n"
                f"🖇Umumiy testlar: {test_count}ta\n"
                f"🎧Eng yuqori eshitish bali: {highest_listening_score}\n"
                f"📖Eng yuqori o'qish bali: {highest_reading_score}\n"
                f"✍️Eng yuqori yozish bali: {highest_writing_score}\n"
                f"🗣Eng yuqori gapirish bali: {highest_speaking_score}\n"
                f"\nOhirgi test sanasi: {formatted_date}"
            )

            keyboard = InlineKeyboardMarkup()

            button = InlineKeyboardButton(text="Yangi natija📥", callback_data="last_result")
            keyboard.add(button)
            bot.reply_to(message, text=result_variable, reply_markup=keyboard)

    elif message.text == 'My results 🔖':
        res = get_user_result(message.chat.id)
        if res.status_code == 404:
            bot.reply_to(
                message, text="You have never taken a test before☹️")
        else:
            data = res.json()
            user_name = data[0]["user"]["last_name"] + \
                " " + data[0]["user"]["first_name"]
            test_count = len(data)
            highest_listening_score = max(
                result["listening"]["band_score"] for result in data)
            highest_reading_score = max(
                result["reading"]["band_score"] for result in data)
            highest_writing_score = max(
                result["writing"]["band_score"] for result in data)
            highest_speaking_score = max(
                result["speaking"]["band_score"] for result in data)
            last_test_date = data[-1]["date_joined"]

            # Convert the string to a datetime object
            parsed_date = datetime.strptime(last_test_date, "%Y-%m-%dT%H:%M:%S.%f%z")

            # Format the datetime object to the desired format
            formatted_date = parsed_date.strftime("%B %d, %Y. %H:%M")

            # Format the variable
            result_variable = (
                f"👤Fullname : {user_name}\n"
                f"🖇Taken tests: {test_count}ta\n"
                f"🎧The highest listening score: {highest_listening_score}\n"
                f"📖The highest reading score: {highest_reading_score}\n"
                f"✍️The highest writing score: {highest_writing_score}\n"
                f"🗣The highest speaking score: {highest_speaking_score}\n"
                f"\nLast test date: {formatted_date}"
            )
            keyboard = InlineKeyboardMarkup()

            button = InlineKeyboardButton(text="New result📥", callback_data="last_result")
            keyboard.add(button)
            bot.reply_to(message, text=result_variable, reply_markup=keyboard)

    elif message.text == 'Мои результаты 🔖':
        res = get_user_result(message.chat.id)
        if res.status_code == 404:
            bot.reply_to(
                message, text="Вы никогда не проходили тест☹️")
        else:
            data = res.json()
            user_name = data[0]["user"]["last_name"] + \
                " " + data[0]["user"]["first_name"]
            test_count = len(data)
            highest_listening_score = max(
                result["listening"]["band_score"] for result in data)
            highest_reading_score = max(
                result["reading"]["band_score"] for result in data)
            highest_writing_score = max(
                result["writing"]["band_score"] for result in data)
            highest_speaking_score = max(
                result["speaking"]["band_score"] for result in data)
            last_test_date = data[-1]["date_joined"]

            # Convert the string to a datetime object
            parsed_date = datetime.strptime(last_test_date, "%Y-%m-%dT%H:%M:%S.%f%z")

            # Format the datetime object to the desired format
            formatted_date = parsed_date.strftime("%B %d, %Y. %H:%M")

            # Format the variable
            result_variable = (
                f"👤Имя и фамилия : {user_name}\n"
                f"🖇Пройдены тесты: {test_count}ta\n"
                f"🎧Высшая оценка прослушивания: {highest_listening_score}\n"
                f"📖Высший балл за чтение: {highest_reading_score}\n"
                f"✍️Высший балл за письмо: {highest_writing_score}\n"
                f"🗣Высший балл за разговорную речь: {highest_speaking_score}\n"
                f"\nДата последнего теста: {formatted_date}"
            )

            keyboard = InlineKeyboardMarkup()

            button = InlineKeyboardButton(text="Новый результат📥", callback_data="last_result")
            keyboard.add(button)
            bot.reply_to(message, text=result_variable, reply_markup=keyboard)

    elif message.text == 'Yordam 💬':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Qoidalar❗️', callback_data='rules')
        button2 = types.InlineKeyboardButton(
            "Tez-tez so'raladigan savollar❓", callback_data='faq')
        button3 = types.InlineKeyboardButton(
            'Operator🧑‍💻', callback_data='operator')
        button4 = types.InlineKeyboardButton(
            'Taklif va shikoyatlar🤝', callback_data='send_requests')
        button5 = types.InlineKeyboardButton(
            "Qo'llanmalar📹", callback_data='guidelines')
        keyboard.add(button1, button2)
        keyboard.add(button3, button4)
        keyboard.add(button5)

        bot.reply_to(message, text="Sizga qanday yordam kerakligini quyidagi menyular orqali tanlang👇", reply_markup=keyboard)


    elif message.text == 'Помощь 💬':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Правила❗️', callback_data='rules')
        button2 = types.InlineKeyboardButton(
            'Часто задаваемые вопросы❓', callback_data='faq')
        button3 = types.InlineKeyboardButton(
            'Оператор🧑‍💻', callback_data='operator')
        button4 = types.InlineKeyboardButton(
            'Предложения и жалобы🤝', callback_data='send_requests')
        button5 = types.InlineKeyboardButton(
            "Руководства📹", callback_data='guidelines')
        keyboard.add(button1, button2)
        keyboard.add(button3, button4)
        keyboard.add(button5)

        bot.reply_to(message, text="Выберите необходимую вам помощь из меню ниже👇",
                     reply_markup=keyboard)

    elif message.text == 'Help 💬':
        keyboard = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
                'Rules❗️', callback_data='rules')
        button2 = types.InlineKeyboardButton(
            'FAQ❓', callback_data='faq')
        button3 = types.InlineKeyboardButton(
            'Operator🧑‍💻', callback_data='operator')
        button4 = types.InlineKeyboardButton(
            'Suggestions and complaints🤝', callback_data='send_requests')
        button5 = types.InlineKeyboardButton(
            "Guidelines📹", callback_data='guidelines')
        keyboard.add(button1, button2)
        keyboard.add(button3, button4)
        keyboard.add(button5)

        bot.reply_to(message, text="Select the help you need from the menu below👇",
                     reply_markup=keyboard)


def sendmessageall(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, "So'rov bekor qilindi", reply_markup=admin_buttons())
    else:
        try:
            res = SendMessageAll(message.text)
            print(res.status_code)
            print(res.text)
            bot.send_message(message.chat.id, "Xabar yuborildi")
        except Exception as err:
            bot.send_message(message.chat.id, f"Xatolik yuz berdi\n{err}")



def delete_user(message):
    tg_id = message.text
    try:
        res = delete_token(tg_id)
        if res == True:
            bot.send_message(message.chat.id, "Foydalanuvchi o'chirildi")
        else:
            bot.send_message(message.chat.id, "Foydalanuvchi topilmadi")
    except Exception as err:
        bot.send_message(message.chat.id, err)

def get_user_writing_with_id(message):
    id = message.text

    essays = get_essays_unchecked(id)
    file_path = f'{id}_essay.txt'

    if len(essays.text) >= 2:
        essays_json = json.loads(essays.text)
        with open(file_path, 'w') as file:
            file.write(f'ID{id} raqamli foydalanuvchining insholari \n\n\n\nTask1 \n\n')
            file.write(f'{essays_json[0]['user_answer']}\n\n\n\n\n')
            file.write(f'Task2\n\n\n\n')
            file.write(f'{essays_json[1]['user_answer']}\n')

        essay_file = open(f"{id}_essay.txt", 'rb')


        img1_url = essays_json[0]['question']['img']
        img2_url = essays_json[1]['question']['img']
        task1_img = f"{api}{img1_url}"
        task2_img = f"{api}{img2_url}"


        markup = telebot.types.InlineKeyboardMarkup()
        button = telebot.types.InlineKeyboardButton(
            text='Baxolash☑️', callback_data='rate_essay')
        markup.add(button)


        bot.send_photo(message.chat.id, task1_img, f"ID{essays_json[0]['question']['id']} raqamli savol")
        bot.send_photo(message.chat.id, task2_img, f"ID{essays_json[1]['question']['id']} raqamli savol")
        bot.send_document(message.chat.id, essay_file, reply_markup=markup, caption=f"Task1 ID: {essays_json[0]['id']}\nTask2 ID: {essays_json[1]['id']}")
    else:
        bot.send_message(message.chat.id, "Ushbu foydalanuvchi Task 2 qismini tugatmagan", reply_markup=adminW_buttons())


def get_user_speaking_with_id(message):
    id = message.text
    user_data = get_user_data(id)
    data = json.loads(user_data)

    bot.send_message(message.chat.id, f"Speaking uchun kerakli ma'lumotlar:\n\nIsm Familiya:{data['first_name']}{data['last_name']}\nTel raqam:{data['phone']}\nUsername: @{data['username']}")


    question1 = question_speaking(1)
    question2 = question_speaking(2)
    question3 = question_speaking(3)

    bot.send_photo(message.chat.id, question1, "Part 1 uchun savol")
    bot.send_photo(message.chat.id, question2, "Part 2 uchun savol")
    bot.send_photo(message.chat.id, question3, "Part 3 uchun savol")

    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(
        text='Fayllarni yuklash📁', callback_data='create_speakingtest')
    markup.add(button)

    bot.send_message(message.chat.id, "Speaking testni o'tkazib bo'lgach pastdagi tugmalar orqali jarayonni yakunlang.\n\nDiqqat! Speaking testni yakunlamasdan turib pastdagi tugmalardan foydalanish mumkin emas.", reply_markup=markup)







@bot.message_handler(commands=['register'])
def register_user(message, referrer_id):
    lang = message.text
    if lang == "O'zbekcha🇺🇿":
        lang = "uz"
        bot.reply_to(
            message, """Botga xush kelibsiz😊! Botdan foydalanish uchun ro'yxatdan o'tishingiz kerak! \nIltimos ismingizni kiriting:""", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_user_firstname, lang, referrer_id)
    elif lang == "Русский🇷🇺":
        lang = "ru"
        bot.reply_to(
            message, """Добро пожаловать в бот😊! Для использования бота необходимо зарегистрироваться!\n\n🇷🇺Пожалуйста, введите ваше имя:""", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_user_firstname, lang, referrer_id)
    elif lang == "English🇺🇸":
        lang = "eng"
        bot.reply_to(message, "Welcome to our bot😊! You have to register to use the bot!\n🇺🇸Please enter your firstname:", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_user_firstname, lang, referrer_id)

def get_user_firstname(message, lang, referrer_id):
    user_firstname = message.text

    if lang == "uz":
        bot.reply_to(message, f"""{user_firstname}, Familiyangizni kiriting:""")
        bot.register_next_step_handler(message, get_user_lastname, user_firstname, lang, referrer_id)
    elif lang == "ru":
        bot.reply_to(message, f"""{user_firstname}, Введите свою фамилию:""")
        bot.register_next_step_handler(message, get_user_lastname, user_firstname, lang, referrer_id)
    elif lang == "eng":
        bot.reply_to(message, f"""{user_firstname}, Enter your surname:""")
        bot.register_next_step_handler(message, get_user_lastname, user_firstname, lang, referrer_id)


def get_user_lastname(message, user_firstname, lang, referrer_id):
    user_lastname = message.text

    if lang == "uz":
        bot.reply_to(message, f"""{user_firstname} {user_lastname}, 🇺🇿Telefon raqamingizni yuborish uchun <b>Kontaktimni yuborish</b> tugmasini bosing""", parse_mode="html", reply_markup=send_contact())
        bot.register_next_step_handler(
            message, get_user_contact, user_firstname, user_lastname, lang, referrer_id)

    elif lang == "ru":
        bot.reply_to(message, f"""{user_firstname} {user_lastname}, Нажмите <b>Отправить мой контакт</b> чтобы отправить свой номер телефона""", parse_mode="html", reply_markup=send_contact())
        bot.register_next_step_handler(
            message, get_user_contact, user_firstname, user_lastname, lang, referrer_id)

    elif lang == "eng":
        bot.reply_to(message, f"""{user_firstname} {user_lastname}, Click <b>Send My Contact</b> to send your phone number""", parse_mode="html", reply_markup=send_contact())
        bot.register_next_step_handler(
            message, get_user_contact, user_firstname, user_lastname, lang, referrer_id)


def get_user_contact(message, user_firstname, user_lastname, lang, referrer_id):
    if message.text == "/start":
        bot.register_next_step_handler(message, start)
        return

    try:
        if not message.contact:
            if lang == 'uz':
                bot.reply_to(message, "Telefon raqam yuborish uchun tugmadan foydalaning")
            elif lang == 'ru':
                bot.reply_to(message, "Используйте кнопку ниже, чтобы отправить номер телефона")
            else:
                bot.reply_to(message, "Use the button below to send a phone number")
            return

        user_number = message.contact.phone_number

        # user must send HIS own number
        if message.from_user.id != message.contact.user_id:
            if lang == 'uz':
                bot.reply_to(message, "O'zingizni telefon raqamingizni yuboring", reply_markup=send_contact())
            elif lang == 'ru':
                bot.reply_to(message, "Отправьте боту свой номер телефона", reply_markup=send_contact())
            else:
                bot.reply_to(message, "Send your own phone number to the bot", reply_markup=send_contact())

            bot.register_next_step_handler(
                message, get_user_contact, user_firstname, user_lastname, lang, referrer_id
            )
            return

        # COUNTRY CHECK
        if not is_allowed_number(user_number):
            if lang == 'uz':
                bot.reply_to(
                    message,
                    "Botdan faqat O'zbekiston 🇺🇿 yoki Koreya 🇰🇷 raqami orqali foydalanish mumkin",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            elif lang == 'ru':
                bot.reply_to(
                    message,
                    "Ботом можно пользоваться только с номерами Узбекистана 🇺🇿 и Кореи 🇰🇷",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            else:
                bot.reply_to(
                    message,
                    "The bot can only be used with Uzbekistan 🇺🇿 or Korea 🇰🇷 numbers",
                    reply_markup=types.ReplyKeyboardRemove()
                )
            return

        # SUCCESS → ASK PASSWORD
        if lang == 'uz':
            bot.reply_to(
                message,
                "Deyarli tayyor😎! O'zingiz uchun parol o'ylab toping",
                reply_markup=types.ReplyKeyboardRemove()
            )
        elif lang == 'ru':
            bot.reply_to(
                message,
                "Почти готово😎! Придумайте себе пароль",
                reply_markup=types.ReplyKeyboardRemove()
            )
        else:
            bot.reply_to(
                message,
                "Almost ready😎! Create your password",
                reply_markup=types.ReplyKeyboardRemove()
            )

        bot.register_next_step_handler(
            message,
            get_user_password,
            user_firstname,
            user_lastname,
            user_number,
            lang,
            referrer_id
        )

    except Exception as err:
        if lang == 'uz':
            bot.reply_to(message, f"Kichik nosozlik. Adminga xabar bering! {err}")
        elif lang == 'ru':
            bot.reply_to(message, f"Небольшой сбой. Сообщите администратору! {err}")
        else:
            bot.reply_to(message, f"Minor bug. Notify administrator! {err}")


def get_user_password(message, user_firstname, user_lastname, user_number, lang, referrer_id):
    user_password = message.text

    if lang == 'uz':
        bot.reply_to(message, "Parolni qayta kiriting")

    elif lang == 'ru':
        bot.reply_to(message, "Введите пароль еще раз")

    elif lang == 'eng':
        bot.reply_to(message, "Enter the password again")

    bot.register_next_step_handler(
        message, get_user_accept, user_firstname, user_lastname, user_number, user_password, lang, referrer_id)


def get_user_accept(message, user_firstname, user_lastname, user_number, user_password, lang, referrer_id):
    if message.text == user_password:

        if lang == 'uz':
            markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button1 = types.KeyboardButton("✅")
            button2 = types.KeyboardButton("❌")
            markup.add(button1, button2)

            bot.send_message(message.chat.id, f"""❗️Ma'lumotlarni tekshiring
            Ismingiz: {user_firstname}
            Familiyangiz: {user_lastname}
            Telefon raqamingiz: {user_number}
            Parolingiz: {user_password}
            """, reply_markup=markup)

            bot.send_message(message.chat.id, "Pastdagi tugmani bosish orqali siz bizning [Foydalanuvchi huquqlar va Foydalanish shartlari](https://docs.google.com/document/d/e/2PACX-1vTDzZuA0OD3bqO22UvJQGnHbTp6RlNvEntOM46UvWM0lR1efPKPyw8P7UpnMOwc9xT2zTPjm0zN4SG-/pub)ga rozilik bildirasiz", parse_mode="Markdown")
        elif lang == 'ru':
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button1 = types.KeyboardButton("✅")
            button2 = types.KeyboardButton("❌")
            markup.add(button1, button2)

            bot.send_message(message.chat.id, f"""❗️Проверьте свои данные
            Имя: {user_firstname}
            Фамилия: {user_lastname}
            Номер телефона: {user_number}
            Пароль: {user_password}
            """, reply_markup=markup)
            bot.send_message(message.chat.id, "Нажимая кнопку ниже, вы соглашаетесь с нашими [Правами пользователя и Условиями использования](https://docs.google.com/document/d/e/2PACX-1vTDzZuA0OD3bqO22UvJQGnHbTp6RlNvEntOM46UvWM0lR1efPKPyw8P7UpnMOwc9xT2zTPjm0zN4SG-/pub).", parse_mode="Markdown")

        elif lang == 'eng':
            markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button1 = types.KeyboardButton("✅")
            button2 = types.KeyboardButton("❌")
            markup.add(button1, button2)

            bot.send_message(message.chat.id, f"""❗️Check your details
            Name: {user_firstname}
            Surname: {user_lastname}
            Phone number: {user_number}
            Password: {user_password}
            """, reply_markup=markup)
            bot.send_message(message.chat.id, "By clicking the button below, you agree to our [User Rights and Terms of Use](https://docs.google.com/document/d/e/2PACX-1vTDzZuA0OD3bqO22UvJQGnHbTp6RlNvEntOM46UvWM0lR1efPKPyw8P7UpnMOwc9xT2zTPjm0zN4SG-/pub)", parse_mode="Markdown")

        bot.register_next_step_handler(
            message, register_user_data, user_firstname, user_lastname, user_number, user_password, lang, referrer_id)
    else:
        if lang == 'uz':
            bot.send_message(
                message.chat.id, "Parolni xato kiritdingiz☹️! Yangi parol o'ylab toping")

        elif lang == 'ru':
            bot.send_message(
                message.chat.id, "Вы ввели неправильный пароль☹️. Введите новый пароль")

        elif lang == 'eng':
            bot.send_message(
                message.chat.id, "You entered wrong password☹️. Enter a new one")


        bot.register_next_step_handler(
            message, get_user_password, user_firstname, user_lastname, user_number, lang, referrer_id)


def register_user_data(message, user_firstname, user_lastname, user_number, user_password, lang, referrer_id):
    telegram_id = message.chat.id
    username = message.from_user.username
    if username != None:
        data = {
            "first_name": user_firstname,
            "last_name": user_lastname,
            "password": user_password,
            "phone": user_number,
            "telegram_id": telegram_id,
            'username': username
        }
        if message.text == "✅":
            try:
                response = requests.post(register_url, data=data)
                print(response.status_code)
                print(response.text)
                if response.status_code == 201:
                    if lang == "uz":
                        bot.send_message(
                            telegram_id, "Muvaffaqiyatli ro'yhatdan o'tdingiz🫡! Botdan to'liq foydalanishingiz mumkin", reply_markup=get_home(lang=lang))

                    elif lang == "ru":
                        bot.send_message(
                            telegram_id, "Вы успешно зарегистрировались🫡! Вы можете полноценно использовать бота", reply_markup=get_home(lang=lang))

                    elif lang == "eng":
                        bot.send_message(
                            telegram_id, "You have successfully registered🫡! Feel free to use the bot.", reply_markup=get_home(lang=lang))

                    saveToken(username, user_password, telegram_id, lang)
                    ref_response = Add_referral(referrer_id=referrer_id)
                    if ref_response == 200:
                        lang = get_lang(referrer_id)
                        if lang == "uz":
                            bot.send_message(referrer_id, f"Siz {user_firstname} ismli foydalanuvchini taklif qildingiz🫡")
                        elif lang == "ru":
                            bot.send_message(referrer_id, f"Вы пригласили пользователя {user_firstname}🫡")
                        elif lang == "eng":
                            bot.send_message(referrer_id, f"You have invited {user_firstname}🫡")
                else:
                    if lang == "uz":
                        print(response.status_code)
                        print(response.text)
                        bot.send_message(
                            telegram_id, "Nimadir xato ketdi🥲! Adminstrator bilan bog'laning")

                    elif lang == "uz":
                        bot.send_message(
                            telegram_id, "Что-то пошло не так🥲! Свяжитесь с администратором")

                    elif lang == "uz":
                        bot.send_message(
                            telegram_id, "🇺🇸Something went wrong🥲! Contact the administrator")
            except Exception as err:
                print(err)

        else:
            if lang == 'uz':
                bot.send_message(message.chat.id, "So'rov bekor qilindi. Qaytadan /start yuboring", reply_markup=types.ReplyKeyboardRemove())

            elif lang == 'ru':
                bot.send_message(message.chat.id, "Запрос отменен. Введите команду /start еще раз", reply_markup=types.ReplyKeyboardRemove())

            elif lang == 'eng':
                bot.send_message(message.chat.id, "The request has been cancelled. Send the /start command again", reply_markup=types.ReplyKeyboardRemove())


    else:
        random_number = random.randint(100000, 999999)
        username = f"user{random_number}"

        username_check = username_exists(username)
        if username_check == True:

            data = {
                "first_name": user_firstname,
                "last_name": user_lastname,
                "password": user_password,
                "phone": user_number,
                "telegram_id": telegram_id,
                'username': username
            }
            if message.text == "✅":
                response = requests.post(register_url, data=data)
                if response.status_code == 201:
                    saveToken(username, user_password, telegram_id, lang)
                    lang = get_lang(message.chat.id)
                    bot.send_message(
                        telegram_id, "Muvaffaqiyatli ro'yhatdan o'tdingiz! Botdan to'liq foydalanishingiz mumkin.", reply_markup=get_home(lang))
                else:
                    bot.send_message(
                        telegram_id, "Nimadir xato ketdi! Adminstrator bilan bog'laning")
            else:
                bot.send_message(message.chat.id, "So'rov bekor qilindi. Qaytadan /start yuboring", reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "So'rov bekor qilindi. Qaytadan /start yuboring", reply_markup=types.ReplyKeyboardRemove())



@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    if call.data == 'add_payment':
        lang = get_lang(call.message.chat.id)
        if lang == "uz":
            keyboard = types.InlineKeyboardMarkup()

            button1 = types.InlineKeyboardButton(f"🔵 Click", callback_data='add_payment_click')
            button2 = types.InlineKeyboardButton(f"⚪️ Payme", callback_data='add_payment_payme')
            button3 = types.InlineKeyboardButton(f"🟢 Paynet ATM naqt pul(tez kunda⚡️)", callback_data='add_payment_paynet')
            keyboard.add(button1, button2)
            keyboard.add(button3)

            bot.send_message(call.message.chat.id, f"ID: `{call.message.chat.id}`\n\nKerakli to'lov tizimini tanlang👇", parse_mode="Markdown", reply_markup=keyboard)
        if lang == "ru":
            keyboard = types.InlineKeyboardMarkup()

            button1 = types.InlineKeyboardButton(f"🔵 Click", callback_data='add_payment_click')
            button2 = types.InlineKeyboardButton(f"⚪️ Payme", callback_data='add_payment_payme')
            button3 = types.InlineKeyboardButton(f"🟢 Paynet Банкомат наличные(скоро⚡️)", callback_data='add_payment_paynet')
            keyboard.add(button1, button2)
            keyboard.add(button3)

            bot.send_message(call.message.chat.id, f"ID: `{call.message.chat.id}`\n\nВыберите желаемую платежную систему", parse_mode="Markdown", reply_markup=keyboard)

        if lang == "eng":
            keyboard = types.InlineKeyboardMarkup()

            button1 = types.InlineKeyboardButton(f"🔵 Click", callback_data='add_payment_click')
            button2 = types.InlineKeyboardButton(f"⚪️ Payme", callback_data='add_payment_payme')
            button3 = types.InlineKeyboardButton(f"🟢 Paynet ATM in cash(soon⚡️)", callback_data='add_payment_paynet')
            keyboard.add(button1, button2)
            keyboard.add(button3)

            bot.send_message(call.message.chat.id, f"ID: `{call.message.chat.id}`\n\nSelect the payment system you want👇", parse_mode="Markdown", reply_markup=keyboard)

    elif call.data == "last_result":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)
        result1 = Check_Result(call.message.chat.id)
        result = json.loads(result1.text)

        if result1.status_code != 404:
            formatted_message = (
                f"Dear candidate, thank you for choosing us!\n\n"
                f"Exam date: {result['date_joined'].split('T')[0]}\n"
                f"Candidate: {result['user']['first_name']} {result['user']['last_name']} (fullname)\n"
                f"Candidate ID: {result['user']['telegram_id']} (telegram_id)\n"
                f"Phone: {result['user']['phone']}\n"
                f"Overall band: {result['band_score']}\n"
                f"Listening: {result['listening']['band_score']}\n"
                f"Reading: {result['reading']['band_score']}\n"
                f"Writing: {result['writing']['band_score']}\n"
                f"Speaking: {result['speaking']['band_score']}"
                "\n\nWe wish you good luck in your real exam. Try your best⚡️"
            )
            bot.send_message(call.message.chat.id, formatted_message)
        else:
            lang = get_lang(call.message.chat.id)
            if lang == "eng":
                bot.send_message(call.message.chat.id, "Your result has not been released yet☹️")
            if lang == "ru":
                bot.send_message(call.message.chat.id, "Ваш результат еще не опубликован☹️")
            if lang == "uz":
                bot.send_message(call.message.chat.id, "Sizning imtixon natijangiz hozircha chiqmagan☹️")

    elif call.data == "guidelines":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)
        if lang == "uz":
            keyboard = InlineKeyboardMarkup()
            url_button = InlineKeyboardButton(text="Kanalga kirish🔔", url="ieltsplus_guide.t.me")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, "Botdan foydalanish bo'yicha barcha ko'rsatmalar quyidagi kanalda berilgan. Undan foydalanish va videolarni tarqatish bo'yicha cheklovlar yo'q", reply_markup=keyboard)

        if lang == "ru":
            keyboard = InlineKeyboardMarkup()
            url_button = InlineKeyboardButton(text="Посмотреть канал🔔", url="ieltsplus_guide.t.me")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, "Все инструкции по использованию бота приведены в канале ниже. Ограничений на использование и распространение видеороликов нет.", reply_markup=keyboard)

        if lang == "eng":
            keyboard = InlineKeyboardMarkup()
            url_button = InlineKeyboardButton(text="View channel🔔", url="ieltsplus_guide.t.me")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, "All instructions for using the bot are given in the channel below. There are no restrictions on the use and distribution of videos.", reply_markup=keyboard)

    elif call.data == "send_requests":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)
        if lang == "uz":
            bot.send_message(call.message.chat.id, "Marhamat, o'z so'rovingizni yozib qoldiring", reply_markup=types.ReplyKeyboardRemove())
        elif lang == "ru":
            bot.send_message(call.message.chat.id, "Пожалуйста, напишите Ваш запрос", reply_markup=types.ReplyKeyboardRemove())
        elif lang == "eng":
            bot.send_message(call.message.chat.id, "Please, write your request", reply_markup=types.ReplyKeyboardRemove())

        bot.register_next_step_handler(call.message, send_request)

    elif call.data == "operator":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)
        if lang == "uz":
            keyboard = InlineKeyboardMarkup()

            url_button = InlineKeyboardButton(text="Mutaxasis bilan bog'lanish🗯", url="django_programmer.t.me/")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, home_support, reply_markup=keyboard)
        elif lang == "ru":
            keyboard = InlineKeyboardMarkup()

            url_button = InlineKeyboardButton(text="Свяжитесь со специалистом🗯", url="django_programmer.t.me/")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, home_support_ru, reply_markup=keyboard)
        elif lang == "eng":
            keyboard = InlineKeyboardMarkup()

            url_button = InlineKeyboardButton(text="Contact a specialist🗯", url="django_programmer.t.me/")
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, home_support_eng, reply_markup=keyboard)

    elif call.data == "rules":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            bot.send_message(call.message.chat.id, rules_uz, reply_markup=get_home(lang))
        elif lang == "ru":
            bot.send_message(call.message.chat.id, rules_ru, reply_markup=get_home(lang))
        elif lang == "eng":
            bot.send_message(call.message.chat.id, rules_eng, reply_markup=get_home(lang))

    elif call.data == "faq":
        bot.delete_message(call.message.chat.id, call.message.id)
        lang = get_lang(call.message.chat.id)
        if lang == "uz":
            bot.send_message(call.message.chat.id, "Bu bo'lim ta'mirda. Agar qandaydir savol bo'lsa operatorga muroojat qiling")
        elif lang == "ru":
            bot.send_message(call.message.chat.id, "Этот раздел находится на обслуживании. Если у вас есть вопросы, пожалуйста, свяжитесь с оператором")
        elif lang == "eng":
            bot.send_message(call.message.chat.id, "This section is under maintenance. If you have any questions, please contact the operator")

    elif call.data == "referral_link":
        lang = get_lang(call.message.chat.id)
        prices = get_prices()
        bot.delete_message(call.message.chat.id, call.message.id)
        user_data = get_user_data(call.message.chat.id)
        user_data_json = json.loads(user_data)
        try:
            if lang == "uz":
                bot.send_message(call.message.chat.id, f"Sizning referralaringiz soni:{user_data_json['referrals']}ta\n\nDo'stlaringizga sizning havolangizni yuborish orqali hisobingizni {prices['ref_price']} so'mga to'ldiring. \nLink: https://t.me/{BOT_USERNAME}?start={call.message.chat.id}")
            if lang == "ru":
                bot.send_message(call.message.chat.id,f"Количество ваших рефералов:{user_data_json['referrals']}\n\nПополните свой счет на сумму {prices['ref_price']}, отправив ссылку своим друзьям. \nЛинк: https://t.me/{BOT_USERNAME}?start={call.message.chat.id}")
            if lang == "eng":
                bot.send_message(call.message.chat.id,f"Number of your referrals:{user_data_json['referrals']}\n\nTop up your account for {prices['ref_price']} by sending your friends your link. \nLink: https://t.me/{BOT_USERNAME}?start={call.message.chat.id}")
        except Exception as err:
            if lang == "uz":
                bot.send_message(call.message.chat.id, text=error_uz+f"\n{err}")
            elif lang == "ru":
                bot.send_message(call.message.chat.id, text=error_ru+f"\n{err}")
            elif lang == "eng":
                bot.send_message(call.message.chat.id, text=error_eng+f"\n{err}")
    elif call.data == "add_payment_click":
        lang = get_lang(call.message.chat.id)
        prices = get_prices()

        bot.delete_message(call.message.chat.id, call.message.id)
        if prices is not None:
            price1 = f"{prices['price1']: ,}"
            price2 = f"{prices['price2']: ,}"
            price4 = f"{prices['price4']: ,}"
            price10 = f"{prices['price10']: ,}"
            if lang == "uz":
                keyboard = types.InlineKeyboardMarkup()

                button1 = types.InlineKeyboardButton(f"1ta - {price1} so'm⚡️", callback_data='payment_1test_click')
                button2 = types.InlineKeyboardButton(f"2ta - {price2} so'm(-10%)⚡️", callback_data='payment_2test_click')
                button3 = types.InlineKeyboardButton(f"4ta - {price4} so'm(-15%)⚡️", callback_data='payment_4test_click')
                button4 = types.InlineKeyboardButton(f"10ta - {price10} so'm(-25%)⚡️", callback_data='payment_10test_click')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "Nechta test uchun to'lov qilmoqchisiz😊? \n\nLayfhak😉: Agar siz ko'proq test sotib olsangiz ko'proq chegirmaga ega bo'lasiz😎!",
                                 parse_mode="Markdown", reply_markup=keyboard)

            elif lang == "ru":
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(f"За 1 тест - {price1} сум⚡️", callback_data='payment_1test_click')
                button2 = types.InlineKeyboardButton(f"За 2 теста - {price2} сум(-10%)⚡️",
                                                     callback_data='payment_2test_click')
                button3 = types.InlineKeyboardButton(f"За 4 теста - {price4} сум(-15%)⚡️",
                                                     callback_data='payment_4test_click')
                button4 = types.InlineKeyboardButton(f"За 10 тестов - {price10} сум(-25%)⚡️",
                                                     callback_data='payment_10test_click')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "За сколько тестов вы готовы заплатить😊? \n\nЛайфхак😉: Если вы купите больше тестов, скидка будет больше😎!",
                                 parse_mode="Markdown", reply_markup=keyboard)

            elif lang == "eng":
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text=f"Single test - {price1} sum⚡️",
                                                     callback_data='payment_1test_click')
                button2 = types.InlineKeyboardButton(text=f"Double tests - {price2} sum(-10%)⚡️",
                                                     callback_data='payment_2test_click')
                button3 = types.InlineKeyboardButton(text=f"Quadruple tests - {price4} sum(-15%)⚡️",
                                                     callback_data='payment_4test_click')
                button4 = types.InlineKeyboardButton(text=f"Ten tests - {price10} sum(-25%)⚡️",
                                                     callback_data='payment_10test_click')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "How many tests do you want to purchase😊? \n\n*Lifehack*😉:__The more you buy, the greater the discount you achieve😎__",
                                 parse_mode="Markdown", reply_markup=keyboard)

    elif call.data == "payment_1test_click":
        prices = get_prices()
        link1 = GenerateLink_Click(amount=prices['price1'], telegram_id=call.message.chat.id)
        link = json.loads(link1)['url']

        lang = get_lang(call.message.chat.id)


        if lang == 'uz':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 To'lov qilish", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click to'lov ma'lumotlari\n\n🆔:{call.message.chat.id}\n📑Testlar soni: 1\n💸Narxi: {prices['price1']}so'm\n\nBarcha ma'lumotlar to'g'ri bo'lsa pastdagi tugma orqali to'lov qiling👇", reply_markup=keyboard)

        if lang == 'ru':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Платить", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click Платежная информация\n\n🆔:{call.message.chat.id}\n📑Количество тестов: 1\n💸Цена: {prices['price1']}сум\n\nЕсли вся информация верна, произведите оплату, используя кнопку ниже👇", reply_markup=keyboard)

        if lang == 'eng':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Pay", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click payment details\n\n🆔:{call.message.chat.id}\n📑Amount of tests: 1\n💸Price: {prices['price1']}sum\n\nIf all the information is correct, pay for an invoice using the button below👇", reply_markup=keyboard)

    elif call.data == "payment_2test_click":
        prices = get_prices()
        link1 = GenerateLink_Click(amount=prices['price2'], telegram_id=call.message.chat.id)
        link = json.loads(link1)['url']

        lang = get_lang(call.message.chat.id)


        if lang == 'uz':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 To'lov qilish", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click to'lov ma'lumotlari\n\n🆔:{call.message.chat.id}\n📑Testlar soni: 2\n💸Narxi: {prices['price2']}so'm\n\nBarcha ma'lumotlar to'g'ri bo'lsa pastdagi tugma orqali to'lov qiling👇", reply_markup=keyboard)

        if lang == 'ru':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Платить", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click Платежная информация\n\n🆔:{call.message.chat.id}\n📑Количество тестов: 2\n💸Цена: {prices['price2']}сум\n\nЕсли вся информация верна, произведите оплату, используя кнопку ниже👇", reply_markup=keyboard)

        if lang == 'eng':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Pay", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click payment details\n\n🆔:{call.message.chat.id}\n📑Amount of tests: 2\n💸Price: {prices['price2']}sum\n\nIf all the information is correct, pay for an invoice using the button below👇", reply_markup=keyboard)

    elif call.data == "payment_4test_click":
        prices = get_prices()
        link1 = GenerateLink_Click(amount=prices['price4'], telegram_id=call.message.chat.id)
        link = json.loads(link1)['url']

        lang = get_lang(call.message.chat.id)


        if lang == 'uz':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 To'lov qilish", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click to'lov ma'lumotlari\n\n🆔:{call.message.chat.id}\n📑Testlar soni: 4\n💸Narxi: {prices['price4']}so'm\n\nBarcha ma'lumotlar to'g'ri bo'lsa pastdagi tugma orqali to'lov qiling👇", reply_markup=keyboard)

        if lang == 'ru':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Платить", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click Платежная информация\n\n🆔:{call.message.chat.id}\n📑Количество тестов: 4\n💸Цена: {prices['price4']}сум\n\nЕсли вся информация верна, произведите оплату, используя кнопку ниже👇", reply_markup=keyboard)

        if lang == 'eng':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Pay", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click payment details\n\n🆔:{call.message.chat.id}\n📑Amount of tests: 4\n💸Price: {prices['price4']}sum\n\nIf all the information is correct, pay for an invoice using the button below👇", reply_markup=keyboard)

    elif call.data == "payment_10test_click":
        prices = get_prices()
        link1 = GenerateLink_Click(amount=prices['price10'], telegram_id=call.message.chat.id)
        link = json.loads(link1)['url']

        lang = get_lang(call.message.chat.id)


        if lang == 'uz':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 To'lov qilish", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click to'lov ma'lumotlari\n\n🆔:{call.message.chat.id}\n📑Testlar soni: 10\n💸Narxi: {prices['price10']}so'm\n\nBarcha ma'lumotlar to'g'ri bo'lsa pastdagi tugma orqali to'lov qiling👇", reply_markup=keyboard)

        if lang == 'ru':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Платить", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click Платежная информация\n\n🆔:{call.message.chat.id}\n📑Количество тестов: 10\n💸Цена: {prices['price10']}сум\n\nЕсли вся информация верна, произведите оплату, используя кнопку ниже👇", reply_markup=keyboard)

        if lang == 'eng':
            keyboard = types.InlineKeyboardMarkup()

            # Add an inline URL button
            url_button = types.InlineKeyboardButton(text="💳 Pay", url=link)
            keyboard.add(url_button)
            bot.send_message(call.message.chat.id, f"#invoice\n\nℹ️Click payment details\n\n🆔:{call.message.chat.id}\n📑Amount of tests: 10\n💸Price: {prices['price10']}sum\n\nIf all the information is correct, pay for an invoice using the button below👇", reply_markup=keyboard)

    elif call.data == "add_payment_payme":
        lang = get_lang(call.message.chat.id)
        prices = get_prices()

        bot.delete_message(call.message.chat.id, call.message.id)
        if prices is not None:
            price1 = f"{prices['price1']: ,}"
            price2 = f"{prices['price2']: ,}"
            price4 = f"{prices['price4']: ,}"
            price10 = f"{prices['price10']: ,}"
            if lang == "uz":
                keyboard = types.InlineKeyboardMarkup()

                button1 = types.InlineKeyboardButton(f"1ta - {price1} so'm⚡️", callback_data='payment_1test')
                button2 = types.InlineKeyboardButton(f"2ta - {price2} so'm(-10%)⚡️", callback_data='payment_2test')
                button3 = types.InlineKeyboardButton(f"4ta - {price4} so'm(-15%)⚡️", callback_data='payment_4test')
                button4 = types.InlineKeyboardButton(f"10ta - {price10} so'm(-25%)⚡️", callback_data='payment_10test')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "Nechta test uchun to'lov qilmoqchisiz😊? \n\nLayfhak😉: Agar siz ko'proq test sotib olsangiz ko'proq chegirmaga ega bo'lasiz😎!",
                                 parse_mode="Markdown", reply_markup=keyboard)

            elif lang == "ru":
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(f"За 1 тест - {price1} сум⚡️", callback_data='payment_1test')
                button2 = types.InlineKeyboardButton(f"За 2 теста - {price2} сум(-10%)⚡️",
                                                     callback_data='payment_2test')
                button3 = types.InlineKeyboardButton(f"За 4 теста - {price4} сум(-15%)⚡️",
                                                     callback_data='payment_4test')
                button4 = types.InlineKeyboardButton(f"За 10 тестов - {price10} сум(-25%)⚡️",
                                                     callback_data='payment_10test')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "За сколько тестов вы готовы заплатить😊? \n\nЛайфхак😉: Если вы купите больше тестов, скидка будет больше😎!",
                                 parse_mode="Markdown", reply_markup=keyboard)

            elif lang == "eng":
                keyboard = types.InlineKeyboardMarkup()
                button1 = types.InlineKeyboardButton(text=f"Single test - {price1} sum⚡️",
                                                     callback_data='payment_1test')
                button2 = types.InlineKeyboardButton(text=f"Double tests - {price2} sum(-10%)⚡️",
                                                     callback_data='payment_2test')
                button3 = types.InlineKeyboardButton(text=f"Quadruple tests - {price4} sum(-15%)⚡️",
                                                     callback_data='payment_4test')
                button4 = types.InlineKeyboardButton(text=f"Ten tests - {price10} sum(-25%)⚡️",
                                                     callback_data='payment_10test')
                keyboard.add(button1)
                keyboard.add(button2)
                keyboard.add(button3)
                keyboard.add(button4)

                bot.send_message(call.message.chat.id,
                                 "How many tests do you want to purchase😊? \n\n*Lifehack*😉:__The more you buy, the greater the discount you achieve😎__",
                                 parse_mode="Markdown", reply_markup=keyboard)
    elif call.data == "payment_1test":

        bot.delete_message(call.message.chat.id, call.message.id)

        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            price = get_prices()['price1']
            PRICE = types.LabeledPrice(label="1ta test narxi", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nTest to'lovi uchun invoys", description="Testni to'lov amalga oshirilgandan keyin istalgan paytda ishlash imkoniga egasiz!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "ru":
            price = get_prices()['price1']
            PRICE = types.LabeledPrice(label="Цена за 1 тест", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nСчет на оплату теста", description="Вы можете запустить тест в любое время после оплаты!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "eng":
            price = get_prices()['price1']
            PRICE = types.LabeledPrice(label="Price for single test", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nInvoice for test fee", description="You can take the test at any time after payment!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )


    elif call.data == "payment_2test":

        bot.delete_message(call.message.chat.id, call.message.id)

        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            price = get_prices()['price2']
            PRICE = types.LabeledPrice(label="2ta test narxi", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nTest to'lovi uchun invoys", description="Testni to'lov amalga oshirilgandan keyin istalgan paytda ishlash imkoniga egasiz!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "ru":
            price = get_prices()['price2']
            PRICE = types.LabeledPrice(label="Цена за 2 теста", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nСчет на оплату теста", description="Вы можете запустить тест в любое время после оплаты!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "eng":
            price = get_prices()['price1']
            PRICE = types.LabeledPrice(label="Price for double tests", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nInvoice for test fee", description="You can take the test at any time after payment!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

    elif call.data == "payment_4test":

        bot.delete_message(call.message.chat.id, call.message.id)

        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            price = get_prices()['price4']
            PRICE = types.LabeledPrice(label="4ta test narxi", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nTest to'lovi uchun invoys", description="Testni to'lov amalga oshirilgandan keyin istalgan paytda ishlash imkoniga egasiz!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "ru":
            price = get_prices()['price4']
            PRICE = types.LabeledPrice(label="Цена за 4 теста", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nСчет на оплату теста", description="Вы можете запустить тест в любое время после оплаты!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "eng":
            price = get_prices()['price4']
            PRICE = types.LabeledPrice(label="Price for quadruple tests", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nInvoice for test fee", description="You can take the test at any time after payment!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

    elif call.data == "payment_10test":

        bot.delete_message(call.message.chat.id, call.message.id)

        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            price = get_prices()['price10']
            PRICE = types.LabeledPrice(label="10ta test narxi", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nTest to'lovi uchun invoys", description="Testni to'lov amalga oshirilgandan keyin istalgan paytda ishlash imkoniga egasiz!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "ru":
            price = get_prices()['price10']
            PRICE = types.LabeledPrice(label="Цена за 10 тестов", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nСчет на оплату теста", description="Вы можете запустить тест в любое время после оплаты!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

        elif lang == "eng":
            price = get_prices()['price10']
            PRICE = types.LabeledPrice(label="Price for ten tests", amount=price * 100)
            bot.send_invoice(call.message.chat.id, title="#invoice\n\nInvoice for test fee", description="You can take the test at any time after payment!",
                             provider_token=provider_token, currency="UZS", prices=[PRICE],
                             start_parameter="one-month-subscription",
                             invoice_payload="test-invoice-payload",
                             photo_url="https://media.istockphoto.com/id/1423208293/vector/3d-vector-realistic-render-secure-protected-pay-online-with-smartphone-design-illustration.jpg?s=612x612&w=0&k=20&c=qAUHU8cQejTA0oTtA0ncT3avAGrjvOEYNzkJxTMppZA=",
                             photo_height=512,  # !=0/None or picture won't be shown
                             photo_width=512,
                             photo_size=512,
                             is_flexible=False
                             )

    elif call.data =='update_lang':
        keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = telebot.types.KeyboardButton(text="O'zbekcha🇺🇿")
        button2 = telebot.types.KeyboardButton(text="Русский🇷🇺")
        button3 = telebot.types.KeyboardButton(text="English🇺🇸")

        keyboard.add(button1, button2, button3)
        bot.send_message(call.message.chat.id, '🇺🇿Tilni tanlang\n🇷🇺Выберите язык\n🇺🇸Select your language', reply_markup=keyboard)
        bot.register_next_step_handler(call.message, update_lang_user)

    elif call.data == 'refresh_stats':
        bot.delete_message(call.message.chat.id, call.message.id)
        stats = get_statistics()
        stats_json = json.loads(stats)
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("Yangilash🔄", callback_data='refresh_stats')
        keyboard.add(button)
        bot.send_message(call.message.chat.id, f"Statistik ma'lumotlar📊\n\n⚡️Botdagi barcha foydalanuvchilar: {stats_json['users']}\n🗓Bugun qo'shilganlar: {stats_json['users_today']}\n⚡️Umumiy sotilgan testlar: {stats_json['tests']}\n🗓Bugun sotilgan testlar: {stats_json['tests_today']}", reply_markup=keyboard)



    elif call.data == 'rate_essay':
        bot.send_message(call.message.chat.id, "Inshoni baxolang")
        bot.register_next_step_handler(call.message, rate_essay_band)


    if call.data == 'edit_cabinet':
        lang = get_lang(call.message.chat.id)

        if lang == "uz":
            bot.send_message(chat_id=call.message.chat.id,
                             text=home_cabinet_edit, reply_markup=types.ReplyKeyboardRemove())
        if lang == "ru":
            bot.send_message(chat_id=call.message.chat.id,
                             text="Введите новое имя📝\n\nНапример: Тешавой", reply_markup=types.ReplyKeyboardRemove())
        if lang == "eng":
            bot.send_message(chat_id=call.message.chat.id,
                             text="Enter your new firstname📝\n\nFor example: Teshavoy", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(call.message, edit_cabinet)
    if call.data == 'start_test':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the test. Break a leg!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/listening_section/1/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#listening #section1\nTest has started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_l1')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)

        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing section 1, click the button below!",
            reply_markup=markup2, disable_notification=False
        )

    if call.data == 'finished_l1':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/listening_section/2/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#listening #section2\nListening section 2 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_l2')
        markup2.add(button1)
        # Send the follow-up message
        try:
            bot.delete_message(call.message.chat.id, message_to_delete.id)
        except Exception as err:
            print(err)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing Section 2, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_l2':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/listening_section/3/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#listening #section3\nListening section 3 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_l3')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completinng listening Section 3, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_l3':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/listening_section/4/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#listening #section4\nListening section 4 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_l4')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing Listening Section 4, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_l4':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/reading_section/1/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#reading #section1\nReading section 1 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_r1')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing reading Section 1, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_r1':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/reading_section/2/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#reading #section2\nReading section 2 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_r2')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing reading Section 2, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_r2':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/reading_section/3/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#reading #section3\nReading section 3 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_r3')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing reading Section 3, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_r3':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/writing_section/1/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#writing #section1\nWriting section 1 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_w1')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing section 1, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_w1':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(
            callback_query_id=call.id, text="Start the next one. I wish you luck!"
        )

        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
            f'{api}/main/writing_section/2/')))
        message_to_delete = bot.send_message(
            chat_id=call.message.chat.id,
            text="#writing #section2\nWriting section 2 has been started👍🏻! \n\n We wish you luck😊",
            reply_markup=markup
        )

        time.sleep(30)

        markup2 = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(
            'Finished👍', callback_data='finished_w2')
        markup2.add(button1)
        # Send the follow-up message
        bot.delete_message(call.message.chat.id, message_to_delete.id)
        bot.send_message(
            chat_id=call.message.chat.id,
            text="After completing writing Section 2, click the button below!",
            reply_markup=markup2
        )

    if call.data == 'finished_w2':
        print(True)
        bot.delete_message(call.message.chat.id, call.message.message_id)
        a = edit_user_status(call.message.chat.id, status=3)

        if a == True:
            bot.send_message(call.message.chat.id, "You have completed the main test👏🏻. Speaking examiners 🧑‍💻 will contact you✅\n\nFeel free to contact a support💬 if you have any questions")

    if call.data == 'users_free':
        users = filter_candidates(1)
        users_json = json.loads(users)
        users_list = "Ularning ro'yhati📝:\n"

        users_count = 0
        for user in users_json:
            users_count +=1
            user_info = f"{users_count}){user['last_name']} {user['first_name']} @{user['username']} {user['phone']}\n"
            users_list += user_info


        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"👋Bo'sh foydalanuvchilar {users_count}ta\n\n{users_list}")

    if call.data == 'users_testing':
        users = filter_candidates(2)
        users_json = json.loads(users)
        users_list = "Ularning ro'yhati📝:\n"

        users_count = 0
        for user in users_json:
            users_count +=1
            user_info = f"{users_count}){user['last_name']} {user['first_name']} @{user['username']} {user['phone']}\n"
            users_list += user_info

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"🤌Testdagi foydalanuvchilar {users_count}ta\n\n{users_list}")

    if call.data == 'users_speaking':
        users = filter_candidates(3)
        users_json = json.loads(users)
        users_list = "Ularning ro'yhati📝:\n"

        users_count = 0
        for user in users_json:
            users_count +=1
            user_info = f"{users_count}){user['last_name']} {user['first_name']} @{user['username']} {user['phone']}\n"
            users_list += user_info

        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, f"🥸Speakingdagi foydalanuvchilar {users_count}ta\n\n{users_list}")


    if call.data == 'create_speakingtest':
        bot.send_message(call.message.chat.id, "Fayllarni yuklashdan oldin iltimos foydalanuvchining telegram ID raqamini qayta yuboring.")
        bot.register_next_step_handler(call.message, get_speakingtest_userid)


def send_request(message):
    request_text = message.text
    bot.send_message(-1002136238191, text=f"Yangi so'rov qoldirildi\n\nUser: {message.chat.id}\nXabar:{request_text}")

    lang = get_lang(message.chat.id)
    if lang == "uz":
        bot.send_message(message.chat.id, "So‘rov muvaffaqiyatli yuborildi!", reply_markup=get_home(lang))
    elif lang == "ru":
        bot.send_message(message.chat.id, "Запрос успешно отправлен!", reply_markup=get_home(lang))
    if lang == "eng":
        bot.send_message(message.chat.id, "Request sent successfully!", reply_markup=get_home(lang))

def update_lang_user(message):
    if message.text == "O'zbekcha🇺🇿":
        lang = 'uz'
        update_lang(message.chat.id, lang)
        bot.send_message(message.chat.id, "Til muvaffaqiyatli o'zgartirildi", reply_markup=get_home(lang))
    elif message.text == "Русский🇷🇺":
        lang = 'ru'
        update_lang(message.chat.id, lang)
        bot.send_message(message.chat.id, "Язык успешно изменен", reply_markup=get_home(lang))
    elif message.text == "English🇺🇸":
        lang = 'eng'
        update_lang(message.chat.id, lang)
        bot.send_message(message.chat.id, "Language changed successfully", reply_markup=get_home(lang))



@bot.shipping_query_handler(func=lambda query: True)
def shipping(shipping_query):
    print(shipping_query)
    bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                              error_message='Yetkazib berish xizmati mavjud emas')


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Aliens tried to steal your card's CVV, but we successfully protected your credentials,"
                                                " try to pay again in a few minutes, we need a small rest.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    prices = get_prices()
    if message.successful_payment.total_amount == prices['price2']:
        payment = Add_payment(telegram_id=message.chat.id, amount=19990*2)
        if payment.status_code == 201:
            lang = get_lang(message.chat.id)


            if lang == "eng":
                bot.send_message(message.chat.id,
                                 'Hoooooray! Thanks for payment! You have received  `{} {}` in your balance! '
                                 'Stay in touch.\n\nUse the balance button if you want to top up again'.format(
                                     message.successful_payment.total_amount / 100, message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "ru":
                bot.send_message(message.chat.id,
                                 'Ураааа! Спасибо за оплату! На ваш баланс поступило `{} {}`! '
                                 'Оставайтесь на связи.\n\nИспользуйте кнопку баланса, если хотите снова пополнить счет.'.format(
                                     message.successful_payment.total_amount / 100, message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "uz":
                bot.send_message(message.chat.id,
                                 'Urree! Tolovingiz uchun rahmat! Siz balansingizga `{} {}` qabul qildingiz! '
                                 'Faol boling.\n\nAgar yana hisobni toldirmoqchi bolsangiz balans tugmasidan foydalaning'.format(
                                     message.successful_payment.total_amount / 100, message.successful_payment.currency),
                                 parse_mode='Markdown')
    elif message.successful_payment.total_amount == prices['price4']:
        payment = Add_payment(telegram_id=message.chat.id, amount=19990 * 4)
        if payment.status_code == 201:
            lang = get_lang(message.chat.id)

            if lang == "eng":
                bot.send_message(message.chat.id,
                                 'Hoooooray! Thanks for payment! You have received  `{} {}` in your balance! '
                                 'Stay in touch.\n\nUse the balance button if you want to top up again'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "ru":
                bot.send_message(message.chat.id,
                                 'Ураааа! Спасибо за оплату! На ваш баланс поступило `{} {}`! '
                                 'Оставайтесь на связи.\n\nИспользуйте кнопку баланса, если хотите снова пополнить счет.'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "uz":
                bot.send_message(message.chat.id,
                                 'Urree! Tolovingiz uchun rahmat! Siz balansingizga `{} {}` qabul qildingiz! '
                                 'Faol boling.\n\nAgar yana hisobni toldirmoqchi bolsangiz balans tugmasidan foydalaning'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')

    elif message.successful_payment.total_amount == prices['price10']:
        payment = Add_payment(telegram_id=message.chat.id, amount=19990 * 10)
        if payment.status_code == 201:
            lang = get_lang(message.chat.id)

            if lang == "eng":
                bot.send_message(message.chat.id,
                                 'Hoooooray! Thanks for payment! You have received  `{} {}` in your balance! '
                                 'Stay in touch.\n\nUse the balance button if you want to top up again'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "ru":
                bot.send_message(message.chat.id,
                                 'Ураааа! Спасибо за оплату! На ваш баланс поступило `{} {}`! '
                                 'Оставайтесь на связи.\n\nИспользуйте кнопку баланса, если хотите снова пополнить счет.'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')
            elif lang == "uz":
                bot.send_message(message.chat.id,
                                 'Urree! Tolovingiz uchun rahmat! Siz balansingizga `{} {}` qabul qildingiz! '
                                 'Faol boling.\n\nAgar yana hisobni toldirmoqchi bolsangiz balans tugmasidan foydalaning'.format(
                                     message.successful_payment.total_amount / 100,
                                     message.successful_payment.currency),
                                 parse_mode='Markdown')

def rate_essay_band(message):
    band_score = message.text

    bot.send_message(message.chat.id, "Foydalanuvchi baxosini oshirish uchun feedback yuboring.")
    bot.register_next_step_handler(message, rate_essay_comment, band_score)


def rate_essay_comment(message, band_score):
    comment = message.text

    bot.send_message(message.chat.id, "Task 1 savolning ID raqamini yuboring")
    bot.register_next_step_handler(message, rate_essay_section1, band_score, comment)


def rate_essay_section1(message, band_score, comment):
    section1_id = message.text

    bot.send_message(message.chat.id, "Endi task 2 savolning ID raqamini yuboring")
    bot.register_next_step_handler(message, rate_essay_section2, band_score, comment, section1_id)


def rate_essay_section2(message, band_score, comment, section1_id):
    section2_id = message.text

    bot.send_message(message.chat.id, "Foydalanuvchining ID raqamini yuboring")
    bot.register_next_step_handler(message, rate_essay_userid, band_score, comment, section1_id, section2_id)

def rate_essay_userid(message, band_score, comment, section1_id, section2_id):
    user_id = message.text

    
    bot.send_message(message.chat.id, "Task1 uchun yuborilgan javobni ID ramini kiriting")
    bot.register_next_step_handler(message, rate_essay_answer1, band_score, comment, section1_id, section2_id, user_id)
    


def rate_essay_answer1(message, band_score, comment, section1_id, section2_id, user_id):
    answer1_id = message.text

    
    bot.send_message(message.chat.id, "Task2 uchun yuborilgan javobni ID ramini kiriting")
    bot.register_next_step_handler(message, rate_essay_answer2, band_score, comment, section1_id, section2_id, user_id, answer1_id)

def rate_essay_answer2(message, band_score, comment, section1_id, section2_id, user_id, answer1_id):
    answer2_id = message.text

    writing = create_writing(band_score, comment, section1_id, section2_id, user_id, answer1_id, answer2_id)
    if writing == True:
        bot.send_message(message.chat.id, f"Muvaffaqiyatli baxolandi! Bosh menyuga qaytish uchun /admin buyrug'idan foydalaning.")
    else:
        bot.send_message(message.chat.id, "Nimadir xato ketdi! Texnik adminga muroojat qiling")


    

def get_speakingtest_userid(message):
    userid = message.text

    bot.send_message(message.chat.id, "Tayyor! Endi yozib olingan audio faylni yuboring.")
    bot.register_next_step_handler(message, get_speakingtest_audio, userid)


@bot.message_handler(content_types=['document', 'audio', 'voice'])
def get_speakingtest_audio(message, userid):
    if message.content_type == 'audio':
        file_name = os.path.splitext(message.audio.file_name)[0]
        file_info = bot.get_file(message.audio.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(f"{file_name}.mp3", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        audio = open(f"{file_name}.mp3", 'rb')

        bot.send_message(message.chat.id, "Audio fayl qabul qilindi. Foydalanuvchini baxolang.")
        bot.register_next_step_handler(message, get_speakingtest_score, userid, audio)


def get_speakingtest_score(message, userid, audio):
    band_score = message.text

    bot.send_message(message.chat.id, "Foydalanuvchi baxosini ko'tarish uchun feedback yuboring")
    bot.register_next_step_handler(message, get_speakingtest_comment, userid, audio, band_score)


def get_speakingtest_comment(message, userid, audio, band_score):
    comment = message.text
    
    a = create_speakingtest(userid, comment, audio, band_score)
    audio.close()

    os.remove(audio.name)
    edit_user_status(userid, 1)
    bot.send_message(message.chat.id, "Ma'lumotlar saqlandi. Bosh meyuga qaytish uchun /admin buyrug'ini yuboring")





def edit_cabinet(message):
    lang = get_lang(message.chat.id)

    first_name = message.text

    if lang == "uz":
        bot.send_message(message.chat.id, "Yangi familiyangizni kiriting")
        bot.register_next_step_handler(message, edit_cabinet_lastname, first_name)
    elif lang == "ru":
        bot.send_message(message.chat.id, "Введите свою новую фамилию")
        bot.register_next_step_handler(message, edit_cabinet_lastname, first_name)
    elif lang == "eng":
        bot.send_message(message.chat.id, "Enter your new surname")
        bot.register_next_step_handler(message, edit_cabinet_lastname, first_name)

def edit_cabinet_lastname(message, first_name):
    lang = get_lang(message.chat.id)
    last_name = message.text

    username = message.from_user.username

    a = edit_user_cabinet(first_name, last_name, username, message.chat.id)

    if a == True:
        lang = get_lang(message.chat.id)
        if lang == "uz":
            bot.send_message(message.chat.id, "Muvaffaqiyatli o'zgartirildi", reply_markup=get_home(lang))
        elif lang == "ru":
            bot.send_message(message.chat.id, "Изменено успешно", reply_markup=get_home(lang))
        elif lang == "eng":
            bot.send_message(message.chat.id, "Changed successfully", reply_markup=get_home(lang))
    else:
        if lang == "uz":
            bot.send_message(message.chat.id, "Bu amaliyotni bajarish uchun username o'rnating", reply_markup=get_home(lang))
        elif lang == "ru":
            bot.send_message(message.chat.id, "Установите имя пользователя для выполнения этой операции", reply_markup=get_home(lang))
        elif lang == "eng":
            bot.send_message(message.chat.id, "Set the username to perform this operation", reply_markup=get_home(lang))










bot.polling()
