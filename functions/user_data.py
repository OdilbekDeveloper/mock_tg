import requests
from elements.urls import mysite


def get_user_data(telegram_id):
    user_data_url = f'{mysite}/api/get_user_data/{telegram_id}/'
    response = requests.get(user_data_url)

    return response.text

def is_allowed_number(phone):
    phone = phone.replace(" ", "")
    return phone.startswith("+998") or phone.startswith("998") or phone.startswith("+82") or phone.startswith("82")
