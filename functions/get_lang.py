import sqlite3




def get_lang(telegram_id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE telegram_id=?", (telegram_id,))
    user = cursor.fetchone()



    conn.close()
    return user[-1]


def update_lang(telegram_id, new_lang):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET lang=? WHERE telegram_id=?", (new_lang, telegram_id))

    conn.commit() 
    conn.close()
