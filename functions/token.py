import requests
from elements.urls import mysite
import sqlite3

def saveToken(username, password, telegram_id, lang):
    token_url = f"{mysite}/api/token/"
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    data = {
        'username': username,
        'password': password
    }
    res = requests.post(url=token_url, data=data)
    token = res.json()['token']

    user_data = (token, telegram_id, lang)
    c.execute('''INSERT INTO user (token, telegram_id, lang)
              VALUES (?, ?, ?)''', user_data)
    
    conn.commit()

    conn.close()


def getToken(telegram_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM user WHERE telegram_id=?", (telegram_id,))
    user = c.fetchone()  

    conn.commit()
    conn.close()
    return user[1]


def delete_token(telegram_id):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("DELETE FROM user WHERE telegram_id=?", (telegram_id,))

    if c.rowcount == 0:
        print(f"No user found with Telegram ID: {telegram_id}")
        return False
    else:
        print(f"User with Telegram ID {telegram_id} deleted successfully.")
        return True
    conn.commit()
    conn.close()

