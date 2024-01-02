import requests
from elements.urls import api
from elements.urls import edit_url
from functions.token import getToken

def edit_user(username, first_name, last_name, phone, balance, telegram_id):
    
    token = getToken(telegram_id)

    
    # Sending data to backend
    payload_data = {
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'balance': balance,
        'username': username
    }

    headers = {
        'Authorization': f'Token {token}',
    }

    # Use the 'data' parameter to send form data
    response = requests.post(edit_url, data=payload_data, headers=headers)

    return response


def edit_user_status(telegram_id, status):
    token = getToken(telegram_id)


    payload_data = {
        'status': status,
    }

    headers = {
        'Authorization': f'Token {token}',
    }

    response = requests.post(edit_url, data=payload_data, headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False
    



def edit_user_cabinet(first_name, last_name, username, telegram_id):
    token = getToken(telegram_id)
    

    payload_data = {
        'first_name': first_name,
        'last_name': last_name,
        'username': username
    }
    headers = {
        'Authorization': f'Token {token}',
    }
    # Use the 'data' parameter to send form data
    response = requests.post(edit_url, data=payload_data, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False
    