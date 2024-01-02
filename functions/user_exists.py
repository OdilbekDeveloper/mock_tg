import sqlite3
import requests
from elements.urls import mysite


def user_exists(telegram_id):
    user_data_url = f'{mysite}/api/get_user_data/{telegram_id}/'
    response = requests.get(user_data_url)

    if response.status_code == 404:
        return False
    else:
        return True
    


def username_exists(username):
    url = f'{mysite}/api/check/username/exists/{username}/'

    response = requests.get(url)

    if response.status_code == 404:
        return True
    else:
        return False


