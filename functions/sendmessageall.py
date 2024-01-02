import requests
from elements.urls import api

def SendMessageAll(message):
    url = f"{api}/api/send-message/"

    data = {
        'text': message
    }

    response = requests.post(url, data=data)

    return response