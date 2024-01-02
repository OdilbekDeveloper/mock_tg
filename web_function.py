@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('view', web_app=types.WebAppInfo(
        'https://odilbek.pythonanywhere.com/main/listening_section/1/')))
    bot.send_message(chat_id=message.chat.id,
                     text="Press the button to open a web page", reply_markup=markup)
