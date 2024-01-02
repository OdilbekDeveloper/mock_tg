import requests
from elements.urls import mysite

def filter_candidates(status):
    filter_url = f'{mysite}/api/filter_candidates/{status}/'
    response = requests.get(filter_url).text

    return response