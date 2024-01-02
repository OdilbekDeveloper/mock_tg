import requests
from elements.urls import mysite


def get_user_result(telegram_id):
    user_result_url = f'{mysite}/api/get_results/{telegram_id}/'
    response = requests.get(user_result_url)

    return response
