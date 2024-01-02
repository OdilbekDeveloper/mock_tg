import requests
from elements.urls import mysite


def get_user_data(telegram_id):
    user_data_url = f'{mysite}/api/get_user_data/{telegram_id}/'
    response = requests.get(user_data_url)

    return response.text
