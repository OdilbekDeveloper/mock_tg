import requests
from elements.urls import api
from functions.token import getToken

def Add_payment(telegram_id, amount):
    payment_url = f"{api}/api/payment/add/"

    token = getToken(telegram_id)

    payload_data = {
        'amount': amount/100,
    }

    headers = {
        'Authorization': f'Token {token}',
    }

    # Use the 'data' parameter to send form data
    response = requests.post(payment_url, data=payload_data, headers=headers)

    return response


def GenerateLink_Click(amount, telegram_id):
    url = f"{api}/"

    data = {
        'amount': amount,
        'telegram_id': telegram_id
    }

    response = requests.post(url=url, data=data)

    return response.text
