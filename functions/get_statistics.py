import requests
from elements.urls import api


def get_statistics():
    url = f"{api}/api/statistics/"

    response = requests.get(url)

    return response.text