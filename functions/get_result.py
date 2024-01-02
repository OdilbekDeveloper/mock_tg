import requests
from elements.urls import api
from functions.token import getToken
def Check_Result(telegram_id):
    url = f"{api}/api/check-all-answers/"
    token = getToken(telegram_id)

    headers = {
        'Authorization': f'Token {token}',
    }

    response = requests.get(url, headers=headers)

    return response
